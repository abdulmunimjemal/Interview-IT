from fastapi import FastAPI 
from app.api import auth, token_validation
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION
)

# include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(token_validation.router, prefix="/validate", tags=["validation"])