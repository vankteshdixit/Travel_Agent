from fastapi import APIRouter, HTTPException
from app.models.user_model import UserSignup, UserLogin
from app.auth import (
    hash_password,
    verify_password,
    create_access_token
)
from app.db import db
from datetime import datetime

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

users_collection = db["users"]


@router.post("/signup")
def signup(user: UserSignup):
    existing_user = users_collection.find_one(
        {"email": user.email.lower()}
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_pw = hash_password(user.password)

    user_data = {
        "name": user.name,
        "email": user.email.lower(),
        "hashed_password": hashed_pw,
        "created_at": datetime.utcnow()
    }

    result = users_collection.insert_one(
        user_data
    )

    token = create_access_token({
        "sub": str(result.inserted_id),
        "email": user.email.lower()
    })

    return {
        "message": "Signup successful",
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/login")
def login(user: UserLogin):
    db_user = users_collection.find_one(
        {"email": user.email.lower()}
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    valid_password = verify_password(
        user.password,
        db_user["hashed_password"]
    )

    if not valid_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token({
        "sub": str(db_user["_id"]),
        "email": db_user["email"]
    })

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }