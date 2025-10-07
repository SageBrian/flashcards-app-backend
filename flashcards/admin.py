from django.contrib import admin
from .models import Deck, Flashcard


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    search_fields = ['title', 'description']


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ['deck', 'question', 'mastered', 'order', 'created_at']
    list_filter = ['mastered', 'deck']
    search_fields = ['question', 'answer']
