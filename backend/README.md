# English Learning Backend

FastAPI backend for English learning application.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy environment file:
```bash
cp .env.example .env
```

4. Initialize database:
```bash
python -m app.init_db
```

5. Start server:
```bash
python run_server.py
```

## API Endpoints

### Authentication
- POST /api/auth/register - Register user
- POST /api/auth/login - Login
- GET /api/auth/me - Get current user

### Vocabulary
- POST /api/words - Create word
- GET /api/words - Get word list
- GET /api/words/{id} - Get single word
- PUT /api/words/{id} - Update word
- DELETE /api/words/{id} - Delete word
- POST /api/words/batch - Batch create words

### Sentences
- POST /api/sentences - Create sentence
- GET /api/sentences - Get sentence list
- GET /api/sentences/{id} - Get single sentence
- PUT /api/sentences/{id} - Update sentence
- DELETE /api/sentences/{id} - Delete sentence

### Practice
- GET /api/practice/words - Get practice words
- POST /api/practice/listening - Submit listening practice
- POST /api/practice/reading - Submit reading practice
- POST /api/practice/writing - Submit writing practice

### Review
- GET /api/review/today - Get today's review items
- POST /api/review/submit - Submit review result
- GET /api/review/stats - Get review statistics

## Development

The server runs on http://localhost:8000
API docs available at http://localhost:8000/docs