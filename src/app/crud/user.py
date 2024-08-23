from fastcrud import FastCRUD, crud_router
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.main import get_session

# Database session dependency
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# Create CRUD router
user_router = crud_router(
    schema=User,
    create_schema=UserCreate,
    update_schema=UserUpdate,
    db_model=User,
    db_session=get_session,
    prefix="/users",
    tags=["users"],
)