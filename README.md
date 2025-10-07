# Flashcards Backend - Django Ninja + Groq LLM

This is the backend API for the flashcards application, built with Django Ninja and powered by Groq LLM for intelligent flashcard generation from PDF documents.

## Features

- 📄 PDF upload and text extraction
- 🤖 AI-powered flashcard generation using Groq LLM
- 📚 Deck management (create, read, update, delete)
- 🎯 Flashcard mastery tracking
- 🚀 Fast API with automatic OpenAPI documentation
- 🔄 CORS enabled for Next.js frontend

## Setup Instructions

### 1. Create Virtual Environment

\`\`\`bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
\`\`\`

### 2. Install Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Environment Variables

Create a `.env` file in the backend directory:

\`\`\`bash
cp .env.example .env
\`\`\`

Edit `.env` and add your Groq API key:

\`\`\`
GROQ_API_KEY=your-groq-api-key-here
\`\`\`

Get your Groq API key from: https://console.groq.com/keys

### 4. Run Migrations

\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

### 5. Create Superuser (Optional)

\`\`\`bash
python manage.py createsuperuser
\`\`\`

### 6. Run Development Server

\`\`\`bash
python manage.py runserver
\`\`\`

The API will be available at: `http://localhost:8000/api/`

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## API Endpoints

### Upload PDF
- **POST** `/api/flashcards/upload`
- Upload a PDF file and generate flashcards
- Form data: `file` (PDF file), `title` (optional)

### List Decks
- **GET** `/api/flashcards/decks`
- Get all flashcard decks with statistics

### Get Deck
- **GET** `/api/flashcards/decks/{deck_id}`
- Get a specific deck with all flashcards

### Create Deck
- **POST** `/api/flashcards/decks`
- Create a new empty deck

### Delete Deck
- **DELETE** `/api/flashcards/decks/{deck_id}`
- Delete a deck and all its flashcards

### Update Flashcard
- **PATCH** `/api/flashcards/flashcards/{card_id}`
- Update flashcard mastered status

### Add Flashcard
- **POST** `/api/flashcards/decks/{deck_id}/flashcards`
- Manually add a flashcard to a deck

## Connecting to Next.js Frontend

Update your Next.js API routes to point to the Django backend:

\`\`\`typescript
const API_URL = 'http://localhost:8000/api/flashcards';

// Example: Upload PDF
const formData = new FormData();
formData.append('file', pdfFile);
formData.append('title', 'My Study Notes');

const response = await fetch(`${API_URL}/upload`, {
  method: 'POST',
  body: formData,
});
\`\`\`

## Project Structure

\`\`\`
backend/
├── flashcards_backend/     # Django project settings
│   ├── settings.py         # Main settings
│   ├── urls.py            # URL configuration with NinjaAPI
│   └── wsgi.py            # WSGI application
├── flashcards/            # Main app
│   ├── models.py          # Deck and Flashcard models
│   ├── schemas.py         # Pydantic schemas for API
│   ├── api.py             # Django Ninja API endpoints
│   ├── services.py        # Business logic (PDF processing, Groq integration)
│   └── admin.py           # Django admin configuration
├── requirements.txt       # Python dependencies
├── manage.py             # Django management script
└── .env                  # Environment variables
\`\`\`

## Technologies Used

- **Django 5.0**: Web framework
- **Django Ninja**: Fast API framework with automatic docs
- **Groq**: LLM API for flashcard generation
- **PyPDF2**: PDF text extraction
- **Pydantic**: Data validation and serialization
- **SQLite**: Default database (easily switchable to PostgreSQL)

## Development Tips

1. **Admin Panel**: Access at http://localhost:8000/admin (after creating superuser)
2. **API Docs**: Always check http://localhost:8000/api/docs for interactive testing
3. **CORS**: Already configured for localhost:3000 (Next.js default)
4. **Database**: Using SQLite by default, but you can switch to PostgreSQL in settings.py

## Troubleshooting

### Groq API Errors
- Ensure your `GROQ_API_KEY` is set correctly in `.env`
- Check your API quota at https://console.groq.com

### PDF Processing Issues
- Ensure the PDF contains extractable text (not scanned images)
- Large PDFs may take longer to process

### CORS Issues
- Check that `CORS_ALLOWED_ORIGINS` in settings.py includes your frontend URL
- Ensure `django-cors-headers` is installed and configured

## Next Steps

1. Add user authentication (Django's built-in auth or JWT)
2. Implement rate limiting for API endpoints
3. Add caching for frequently accessed decks
4. Deploy to production (Heroku, Railway, or DigitalOcean)
