"""
URL configuration for flashcards_backend project.
"""
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from flashcards.api import router as flashcards_router

api = NinjaAPI(
    title="Flashcards API",
    version="1.0.0",
    description="API for generating and managing flashcards from PDF documents using Groq LLM"
)

api.add_router("/flashcards/", flashcards_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
