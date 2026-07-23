from pydantic import BaseModel, EmailStr
from typing import Optional


# ======================================
# Registro de usuario
# ======================================

class UserRegister(BaseModel):

    username: str

    full_name: str

    email: EmailStr

    password: str

    role: str = "viewer"


# ======================================
# Login
# ======================================

class UserLogin(BaseModel):

    username: str

    password: str


# ======================================
# Usuario devuelto por la API
# ======================================

class UserResponse(BaseModel):

    username: str

    full_name: str

    email: EmailStr

    role: str

    active: bool


# ======================================
# Token JWT
# ======================================

class Token(BaseModel):

    access_token: str

    token_type: str


# ======================================
# Datos contenidos en el JWT
# ======================================

class TokenData(BaseModel):

    username: Optional[str] = None

    role: Optional[str] = None