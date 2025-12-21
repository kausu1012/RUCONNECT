from pydantic import BaseModel, EmailStr

class SignupSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    customer_type: str  # new / existing

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    customer_type: str

    class Config:
        from_attributes = True
