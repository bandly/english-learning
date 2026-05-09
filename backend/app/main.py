from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes import auth, vocabulary, sentence, practice, review

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth, prefix="/api/auth", tags=["auth"])
app.include_router(vocabulary, prefix="/api/words", tags=["vocabulary"])
app.include_router(sentence, prefix="/api/sentences", tags=["sentences"])
app.include_router(practice, prefix="/api/practice", tags=["practice"])
app.include_router(review, prefix="/api/review", tags=["review"])


@app.get("/")
async def root():
    return {
        "message": "English Learning API",
        "version": settings.VERSION
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}