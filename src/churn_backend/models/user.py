from datetime import datetime


def create_user(

    username,

    full_name,

    email,

    hashed_password,

    role

):

    return {

        "username": username,

        "full_name": full_name,

        "email": email,

        "hashed_password": hashed_password,

        "role": role,

        "active": True,

        "created_at": datetime.utcnow(),

        "last_login": None

    }