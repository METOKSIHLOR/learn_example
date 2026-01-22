from fastapi import FastAPI, Depends, HTTPException, Response, Cookie
import uuid
from starlette import status

from app.api.dependencies import get_session, get_current_user
from app.api.routers.users import router as user_router
from app.api.routers.items import router as item_router
from app.api.schemas import UserCreate, UserCreateResponse, UserCreds, UserInfoResponse
from app.db.repository import UserRepository
from app.db.session import close_db, connect_db
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(item_router)

