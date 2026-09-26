import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from passlib.context import CryptContext

from lib.db import db
from models.capacity import DemoUser, LoginRequest


router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def public_user(document: dict) -> DemoUser:
    return DemoUser(
        id=document["id"],
        email=document["email"],
        name=document["name"],
        role=document["role"],
        title=document["title"],
        organization=document["organization"],
        initials=document["initials"],
    )


def create_access_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(hours=8),
    }
    return jwt.encode(payload, os.environ["JWT_SECRET"], algorithm=JWT_ALGORITHM)


async def get_current_user(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        authorization = request.headers.get("Authorization", "")
        if authorization.startswith("Bearer "):
            token = authorization[7:]
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = jwt.decode(token, os.environ["JWT_SECRET"], algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired") from exc
    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")
    user = await db.users.find_one({"id": payload.get("sub")})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


CurrentUser = Annotated[dict, Depends(get_current_user)]


@router.post("/login", response_model=DemoUser)
async def login(input: LoginRequest, response: Response):
    email = input.email.strip().lower()
    user = await db.users.find_one({"email": email})
    if not user or not verify_password(input.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    response.set_cookie(
        "access_token",
        create_access_token(user["id"]),
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=8 * 60 * 60,
        path="/",
    )
    return public_user(user)


@router.get("/me", response_model=DemoUser)
async def me(user: CurrentUser):
    return public_user(user)


@router.post("/logout", response_model=dict[str, str])
async def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    return {"status": "ok"}