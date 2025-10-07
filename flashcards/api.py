"""
Django Ninja API endpoints for flashcards
"""
from ninja import Router, File
from ninja.files import UploadedFile
from typing import List
from django.shortcuts import get_object_or_404

from .models import Deck, Flashcard
from .schemas import (
    DeckSchema,
    DeckCreateSchema,
    FlashcardSchema,
    FlashcardCreateSchema,
    FlashcardUpdateSchema,
    PDFUploadResponse,
    ErrorResponse
)
from .services import FlashcardService

router = Router()
flashcard_service = FlashcardService()


@router.post("/upload", response={200: PDFUploadResponse, 400: ErrorResponse})
def upload_pdf(request, file: UploadedFile = File(...), title: str = None):
    """
    Upload a PDF file and generate flashcards using Groq LLM
    """
    try:
        # Validate file type
        if not file.name.endswith('.pdf'):
            return 400, {"error": "Invalid file type", "detail": "Only PDF files are allowed"}
        
        # Process PDF and create deck
        result = flashcard_service.process_pdf_and_create_deck(file, title)
        
        return 200, {
            "deck_id": result['deck_id'],
            "title": result['title'],
            "card_count": result['card_count'],
            "message": f"Successfully generated {result['card_count']} flashcards"
        }
    
    except Exception as e:
        return 400, {"error": "Failed to process PDF", "detail": str(e)}


@router.get("/decks", response=List[DeckSchema])
def list_decks(request):
    """
    Get all flashcard decks
    """
    decks = Deck.objects.prefetch_related('flashcards').all()
    
    result = []
    for deck in decks:
        deck_data = DeckSchema.from_orm(deck)
        deck_data.flashcards = [FlashcardSchema.from_orm(card) for card in deck.flashcards.all()]
        deck_data.card_count = deck.flashcards.count()
        deck_data.mastered_count = deck.flashcards.filter(mastered=True).count()
        result.append(deck_data)
    
    return result


@router.get("/decks/{deck_id}", response={200: DeckSchema, 404: ErrorResponse})
def get_deck(request, deck_id: int):
    """
    Get a specific deck with all its flashcards
    """
    try:
        deck = get_object_or_404(Deck.objects.prefetch_related('flashcards'), id=deck_id)
        
        deck_data = DeckSchema.from_orm(deck)
        deck_data.flashcards = [FlashcardSchema.from_orm(card) for card in deck.flashcards.all()]
        deck_data.card_count = deck.flashcards.count()
        deck_data.mastered_count = deck.flashcards.filter(mastered=True).count()
        
        return 200, deck_data
    
    except Exception as e:
        return 404, {"error": "Deck not found", "detail": str(e)}


@router.post("/decks", response={201: DeckSchema, 400: ErrorResponse})
def create_deck(request, payload: DeckCreateSchema):
    """
    Create a new empty deck
    """
    try:
        deck = Deck.objects.create(
            title=payload.title,
            description=payload.description
        )
        
        deck_data = DeckSchema.from_orm(deck)
        deck_data.flashcards = []
        deck_data.card_count = 0
        deck_data.mastered_count = 0
        
        return 201, deck_data
    
    except Exception as e:
        return 400, {"error": "Failed to create deck", "detail": str(e)}


@router.delete("/decks/{deck_id}", response={200: dict, 404: ErrorResponse})
def delete_deck(request, deck_id: int):
    """
    Delete a deck and all its flashcards
    """
    try:
        deck = get_object_or_404(Deck, id=deck_id)
        deck.delete()
        return 200, {"message": "Deck deleted successfully"}
    
    except Exception as e:
        return 404, {"error": "Deck not found", "detail": str(e)}


@router.patch("/flashcards/{card_id}", response={200: FlashcardSchema, 404: ErrorResponse})
def update_flashcard(request, card_id: int, payload: FlashcardUpdateSchema):
    """
    Update a flashcard's mastered status
    """
    try:
        flashcard = get_object_or_404(Flashcard, id=card_id)
        flashcard.mastered = payload.mastered
        flashcard.save()
        
        return 200, FlashcardSchema.from_orm(flashcard)
    
    except Exception as e:
        return 404, {"error": "Flashcard not found", "detail": str(e)}


@router.post("/decks/{deck_id}/flashcards", response={201: FlashcardSchema, 400: ErrorResponse})
def add_flashcard(request, deck_id: int, payload: FlashcardCreateSchema):
    """
    Add a new flashcard to a deck
    """
    try:
        deck = get_object_or_404(Deck, id=deck_id)
        
        flashcard = Flashcard.objects.create(
            deck=deck,
            question=payload.question,
            answer=payload.answer,
            order=payload.order
        )
        
        return 201, FlashcardSchema.from_orm(flashcard)
    
    except Exception as e:
        return 400, {"error": "Failed to create flashcard", "detail": str(e)}
