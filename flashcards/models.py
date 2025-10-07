from django.db import models
from django.utils import timezone


class Deck(models.Model):
    """Flashcard deck model"""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    pdf_filename = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Flashcard(models.Model):
    """Individual flashcard model"""
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='flashcards')
    question = models.TextField()
    answer = models.TextField()
    mastered = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.deck.title} - Card {self.order}"
