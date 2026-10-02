from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    api_key: str

    model_config = {
        "from_attributes": True
    }
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"