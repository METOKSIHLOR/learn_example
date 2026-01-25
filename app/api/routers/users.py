from fastapi import FastAPI, Depends, HTTPException, Response, Cookie, APIRouter, BackgroundTasks
import uuid

from sqlalchemy.exc import IntegrityError
from starlette import status

from app.api.autorization.hash import verify_password
from app.api.dependencies import get_session, get_current_user
from app.api.schemas import UserCreate, UserCreateResponse, UserCreds, UserInfoResponse
from app.api.storage import storage
from app.db.models import User
from app.db.repository import UserRepository
from app.nats.pub import nats_publish
import json

router = APIRouter(tags=["user"], prefix="/user")

@router.post("/registration", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse)
async def registration(schema: UserCreate,
                       background_tasks: BackgroundTasks,
                       session = Depends(get_session),
                       ):
    repo = UserRepository(session)
    try:
        user = await repo.create_user(schema)
        await session.commit()
        await session.refresh(user)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")

    data = {
        "id": user.id,
        "username": user.username,
        "role": user.role,
    }

    background_tasks.add_task(nats_publish, "user.create", data)
    return user

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(schema: UserCreds, response: Response, session = Depends(get_session)):
    repo = UserRepository(session)
    user = await repo.get_user_by_username(schema.username)

    if not user or not verify_password(schema.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session_id = str(uuid.uuid4())

    storage.set(session_id, user.id, ex=3600)

    response.set_cookie(key="session_id",
                        value=session_id,
                        max_age=3600,
                        httponly=True,
                        samesite="lax")

    return {"success": True}

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response, session_id = Cookie(None)):
    response.delete_cookie(key="session_id")

    if session_id:
        storage.delete(session_id)

    return {"success": True}

@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserInfoResponse)
async def get_me(user = Depends(get_current_user)):
    return user