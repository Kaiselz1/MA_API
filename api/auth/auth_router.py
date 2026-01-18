from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from config.database import get_db
from config.security import hash
from config import token, oauth2
from ..auth import auth_schema
from ..user import user_model, user_schema
from ..auth import token_model
from datetime import datetime

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

# Register User
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=auth_schema.UserSignup)
def register(request: auth_schema.UserSignupRequest, db: Session = Depends(get_db)):
    existing_user = db.query(user_model.User).filter(user_model.User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    new_user = user_model.User(
        username=request.username,
        email=request.email,
        password=hash.hash_password(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Login User
@router.post("/login", status_code=status.HTTP_200_OK)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):       
    user = db.query(user_model.User).filter(user_model.User.email == request.username).first()
    if not user:
        print("User not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )
    if not hash.verify(user.password, request.password):
        print("Incorrect password")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )
    access_token = token.create_access_token(
        data={"sub": user.email}
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

# Validate Token
@router.get("/validate-token", status_code=status.HTTP_200_OK)
def validate_token(current_user: user_model.User = Depends(oauth2.get_current_user)):
    return {"valid": True, "email": current_user.email}

# Get Current User Info
@router.get("/me", status_code=status.HTTP_200_OK, response_model=user_schema.User)
def get_current_user_info(current_user: user_model.User = Depends(oauth2.get_current_user)):
    return current_user

# Logout User    
@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(token_data: str = Depends(oauth2.oauth2_scheme), db: Session = Depends(get_db), current_user: user_model.User = Depends(oauth2.get_current_user)):
    # Extract expiration from JWT payload
    payload = token.verify_token(token_data, HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid token"
    ))
    exp_timestamp = payload.get("exp")
    expires_at = datetime.utcfromtimestamp(exp_timestamp) if exp_timestamp else None

    # Add token to blacklist
    blacklisted_token = token_model.BlacklistedToken(
        token=token_data,
        user_email=current_user.email,
        expires_at=expires_at
    )
    db.add(blacklisted_token)
    db.commit()
    return {"msg": "Logout successful. Please delete the token on the client side."}