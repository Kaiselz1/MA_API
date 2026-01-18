from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone: str | None = ''
    address: str | None = ''

class ShowUser(BaseModel):
    username: str
    email: EmailStr

    class Config: {
        "from_attributes": True
    }