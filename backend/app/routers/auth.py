from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.utils.auth import (
    verify_password, create_access_token, 
    ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user, get_password_hash
)
from app.schemas.schemas import Token, UserCreate, UserResponse
from app.services.database import get_user_by_username, create_user, get_all_users

router = APIRouter(tags=["authentication"])


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    if get_user_by_username(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    user = create_user(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role
    )
    
    return user


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@router.get("/debug/users")
async def debug_list_users():
    users = get_all_users()
    return [{"id": user.id, "username": user.username, "email": user.email, "role": user.role} for user in users]


@router.get("/debug/verify-password")
async def debug_verify_password(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return {"exists": False, "verified": False}
    
    is_verified = verify_password(password, user.hashed_password)
    return {
        "exists": True, 
        "verified": is_verified,
        "hashed_password": user.hashed_password
    }


@router.get("/debug/test-password-hash")
async def debug_test_password_hash():
    test_password = "password"
    test_hash = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
    
    is_verified = verify_password(test_password, test_hash)
    
    new_hash = get_password_hash(test_password)
    
    return {
        "test_password": test_password,
        "test_hash": test_hash,
        "is_verified": is_verified,
        "new_hash": new_hash
    }
