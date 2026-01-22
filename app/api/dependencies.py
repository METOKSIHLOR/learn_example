from fastapi import Cookie, HTTPException, Depends

from app.api.storage import storage
from app.db import session as sess
from app.db.repository import UserRepository


async def get_session():
    async with sess.SessionFactory() as session:
        yield session

async def get_current_user(session_id: str | None = Cookie(None), session = Depends(get_session)):
    if session_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user_id = storage.get(session_id)

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid session")

    repo = UserRepository(session)
    user = await repo.get_user_by_id(user_id)
    return user

async def check_user_role(user = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="User is not admin")

    return user