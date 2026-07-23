from datetime import datetime

from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status
)

from fastapi.security import OAuth2PasswordRequestForm

from database import (
    users_collection,
    logs_collection
)

from security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

from models.user import create_user

from schemas.auth import (
    UserRegister,
    UserResponse,
    Token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =====================================================
# Registrar usuario
# =====================================================
@router.post(
    "/register",
    response_model=UserResponse
)
def register(user: UserRegister):

    username = users_collection.find_one(
        {
            "username": user.username
        }
    )

    if username:

        raise HTTPException(
            status_code=400,
            detail="El usuario ya existe."
        )

    email = users_collection.find_one(
        {
            "email": user.email
        }
    )

    if email:

        raise HTTPException(
            status_code=400,
            detail="El correo ya existe."
        )

    new_user = create_user(

        username=user.username,

        full_name=user.full_name,

        email=user.email,

        hashed_password=hash_password(
            user.password
        ),

        role=user.role

    )

    users_collection.insert_one(new_user)

    return UserResponse(

        username=new_user["username"],

        full_name=new_user["full_name"],

        email=new_user["email"],

        role=new_user["role"],

        active=new_user["active"]

    )


# =====================================================
# Login
# =====================================================
@router.post(
    "/login",
    response_model=Token
)
def login(

    form_data: OAuth2PasswordRequestForm = Depends()

):

    user = users_collection.find_one(

        {

            "username": form_data.username

        }

    )

    if user is None:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Usuario o contraseña incorrectos"

        )

    if not verify_password(

        form_data.password,

        user["hashed_password"]

    ):

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Usuario o contraseña incorrectos"

        )

    users_collection.update_one(

        {

            "username": user["username"]

        },

        {

            "$set": {

                "last_login": datetime.utcnow()

            }

        }

    )

    logs_collection.insert_one(

        {

            "username": user["username"],

            "action": "LOGIN",

            "date": datetime.utcnow()

        }

    )

    token = create_access_token(

        {

            "sub": user["username"],

            "role": user["role"]

        }

    )

    return {

        "access_token": token,

        "token_type": "bearer"

    }


# =====================================================
# Usuario autenticado
# =====================================================
@router.get("/me")
def me(

    current_user=Depends(

        get_current_user

    )

):

    current_user["_id"] = str(

        current_user["_id"]

    )

    current_user.pop(

        "hashed_password"

    )

    return current_user


# =====================================================
# Todos los usuarios
# =====================================================
@router.get("/users")
def users(

    current_user=Depends(

        get_current_user

    )

):

    if current_user["role"] != "admin":

        raise HTTPException(

            status_code=403,

            detail="Acceso denegado"

        )

    users = []

    cursor = users_collection.find()

    for user in cursor:

        user["_id"] = str(

            user["_id"]

        )

        user.pop(

            "hashed_password"

        )

        users.append(

            user

        )

    return users


# =====================================================
# Desactivar usuario
# =====================================================
@router.delete("/users/{username}")
def delete_user(

    username: str,

    current_user=Depends(

        get_current_user

    )

):

    if current_user["role"] != "admin":

        raise HTTPException(

            status_code=403,

            detail="Acceso denegado"

        )

    result = users_collection.update_one(

        {

            "username": username

        },

        {

            "$set": {

                "active": False

            }

        }

    )

    if result.modified_count == 0:

        raise HTTPException(

            status_code=404,

            detail="Usuario no encontrado"

        )

    return {

        "message": "Usuario desactivado"

    }


# =====================================================
# Cambiar rol
# =====================================================
@router.put("/users/{username}/role")
def change_role(

    username: str,

    role: str,

    current_user=Depends(

        get_current_user

    )

):

    if current_user["role"] != "admin":

        raise HTTPException(

            status_code=403,

            detail="Acceso denegado"

        )

    users_collection.update_one(

        {

            "username": username

        },

        {

            "$set": {

                "role": role

            }

        }

    )

    return {

        "message": "Rol actualizado"

    }