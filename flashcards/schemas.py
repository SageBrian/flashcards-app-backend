from ninja import Schema, ModelSchema
from typing import List, Optional
from datetime import datetime
from .models import Deck, Flashcard


class FlashcardSchema(ModelSchema):
    """Schema for flashcard response"""
    class Meta:
        model = Flashcard
        fields = ['id', 'question', 'answer', 'mastered', 'order']


class FlashcardCreateSchema(Schema):
    """Schema for creating a flashcard"""
    question: str
    answer: str
    order: int = 0


class DeckSchema(ModelSchema):
    """Schema for deck response"""
    flashcards: List[FlashcardSchema] = []
    card_count: int = 0
    mastered_count: int = 0
    
    class Meta:
        model = Deck
        fields = ['id', 'title', 'description', 'pdf_filename', 'created_at', 'updated_at']
    
  


class DeckCreateSchema(Schema):
    """Schema for creating a deck"""
    title: str
    description: Optional[str] = ""


class PDFUploadResponse(Schema):
    """Schema for PDF upload response"""
    deck_id: int
    title: str
    card_count: int
    message: str


class FlashcardUpdateSchema(Schema):
    """Schema for updating flashcard mastered status"""
    mastered: bool


class ErrorResponse(Schema):
    """Schema for error responses"""
    error: str
    detail: Optional[str] = None
