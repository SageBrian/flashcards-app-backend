"""
Services for PDF processing and flashcard generation using Groq LLM
"""
import PyPDF2
from groq import Groq
from django.conf import settings
from typing import List, Dict
import json
import re


class PDFProcessor:
    """Process PDF files and extract text"""
    
    @staticmethod
    def extract_text_from_pdf(pdf_file) -> str:
        """Extract text content from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")


class FlashcardGenerator:
    """Generate flashcards using Groq LLM"""
    
    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set in environment variables")
        
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"  # Fast and capable model
    
    def generate_flashcards(self, text: str, num_cards: int = 10) -> List[Dict[str, str]]:
        """
        Generate flashcards from text using Groq LLM
        
        Args:
            text: The text content to generate flashcards from
            num_cards: Number of flashcards to generate
            
        Returns:
            List of dictionaries with 'question' and 'answer' keys
        """
        try:
            prompt = self._create_prompt(text, num_cards)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educator who creates high-quality flashcards for studying. You extract key concepts and create clear, concise questions with accurate answers."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000,
            )
            
            flashcards_text = response.choices[0].message.content
            flashcards = self._parse_flashcards(flashcards_text)
            
            return flashcards
            
        except Exception as e:
            raise Exception(f"Error generating flashcards with Groq: {str(e)}")
    
    def _create_prompt(self, text: str, num_cards: int) -> str:
        """Create the prompt for Groq LLM"""
        return f"""Based on the following text, create {num_cards} high-quality flashcards for studying.

TEXT:
{text[:4000]}  # Limit text to avoid token limits

INSTRUCTIONS:
1. Extract the most important concepts, definitions, and facts
2. Create clear, specific questions
3. Provide accurate, concise answers
4. Format each flashcard as: Q: [question] | A: [answer]
5. Number each flashcard (1., 2., 3., etc.)
6. Focus on testable knowledge and key takeaways

Generate exactly {num_cards} flashcards now:"""
    
    def _parse_flashcards(self, text: str) -> List[Dict[str, str]]:
        """Parse the LLM response into structured flashcards"""
        flashcards = []
        
        # Try to parse numbered format: "1. Q: ... | A: ..."
        pattern = r'\d+\.\s*Q:\s*(.+?)\s*\|\s*A:\s*(.+?)(?=\d+\.\s*Q:|$)'
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
        
        if matches:
            for question, answer in matches:
                flashcards.append({
                    'question': question.strip(),
                    'answer': answer.strip()
                })
        else:
            # Fallback: try to split by double newlines
            sections = text.split('\n\n')
            for section in sections:
                if 'Q:' in section and 'A:' in section:
                    parts = section.split('|')
                    if len(parts) >= 2:
                        q_part = parts[0].split('Q:')[-1].strip()
                        a_part = parts[1].split('A:')[-1].strip()
                        if q_part and a_part:
                            flashcards.append({
                                'question': q_part,
                                'answer': a_part
                            })
        
        return flashcards


class FlashcardService:
    """Main service for handling flashcard operations"""
    
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.flashcard_generator = FlashcardGenerator()
    
    def process_pdf_and_create_deck(self, pdf_file, title: str = None) -> Dict:
        """
        Process PDF file and create a deck with flashcards
        
        Args:
            pdf_file: Uploaded PDF file
            title: Optional title for the deck
            
        Returns:
            Dictionary with deck information
        """
        from .models import Deck, Flashcard
        
        # Extract text from PDF
        text = self.pdf_processor.extract_text_from_pdf(pdf_file)
        
        if not text:
            raise ValueError("No text could be extracted from the PDF")
        
        # Generate title if not provided
        if not title:
            title = pdf_file.name.replace('.pdf', '').replace('_', ' ').title()
        
        # Generate flashcards using Groq
        flashcards_data = self.flashcard_generator.generate_flashcards(text)
        
        if not flashcards_data:
            raise ValueError("No flashcards could be generated from the content")
        
        # Create deck
        deck = Deck.objects.create(
            title=title,
            description=f"Generated from {pdf_file.name}",
            pdf_filename=pdf_file.name
        )
        
        # Create flashcards
        for idx, card_data in enumerate(flashcards_data):
            Flashcard.objects.create(
                deck=deck,
                question=card_data['question'],
                answer=card_data['answer'],
                order=idx
            )
        
        return {
            'deck_id': deck.id,
            'title': deck.title,
            'card_count': len(flashcards_data)
        }
