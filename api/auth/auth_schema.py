from pydantic import BaseModel, EmailStr, validator
from typing import Optional

#bro did not put password in the signup 🗿

#thx you bro

# Schema for user registration (input)
class UserSignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserSignup(BaseModel):
    id: Optional[int] = None
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    