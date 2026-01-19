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


class UserProfileUpdateRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str

    @validator('name')
    def validate_name(cls, v):
        v = v.strip()
        if len(v) < 2:
            raise ValueError('Name is too short')
        return v

    @validator('email')
    def validate_email(cls, v):
        v = v.strip().lower()
        if not v.endswith('@gmail.com'):
            raise ValueError('Only Gmail addresses are allowed')
        return v

    @validator('phone')
    def validate_phone(cls, v):
        v = v.strip()
        if len(v) < 9 or len(v) > 15:
            raise ValueError('Phone number must be between 9-15 digits')
        if not v.isdigit():
            raise ValueError('Phone number must contain only digits')
        return v

    @validator('address')
    def validate_address(cls, v):
        v = v.strip()
        if len(v) < 6:
            raise ValueError('Address is too short')
        return v

    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    name: str
    email: str
    phone: str
    address: str

    class Config:
        from_attributes = True
    