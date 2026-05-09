from app.api.routes.auth import router as auth_router
from app.api.routes.vocabulary import router as vocabulary_router
from app.api.routes.sentence import router as sentence_router
from app.api.routes.practice import router as practice_router
from app.api.routes.review import router as review_router

# Export routers
auth = auth_router
vocabulary = vocabulary_router
sentence = sentence_router
practice = practice_router
review = review_router