from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from schema.user_schema import UserSchema, DataUser
from config.db import engine
from model.users import users
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List
from fastapi import HTTPException

 

user = APIRouter()

@user.get("/")
def root():
    return {"message": "Hello :D"}

@user.get("/api/user", response_model=List[UserSchema])
def get_users():
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()
        
        user_objects = [UserSchema(
            id=row.id,
            nombre_usuario=row.nombre_usuario,
            numero_doc_usuario=row.numero_doc_usuario,
            usuario=row.usuario,
            contrasenia_usuario=row.contrasenia_usuario
        ) for row in result]
        
        return user_objects
    
@user.get("/api/user/{user_id}", response_model=UserSchema)
def get_user(user_id: str):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id == user_id)).first()

        if result:
            user_dict = {
                "id": result.id,
                "nombre_usuario": result.nombre_usuario,
                "numero_doc_usuario": result.numero_doc_usuario,
                "usuario": result.usuario,
                "contrasenia_usuario": result.contrasenia_usuario
            }
            return user_dict
        else:
            raise HTTPException(status_code=404, detail="User not found")


@user.post("/api/user", status_code=HTTP_201_CREATED)
def create_user(data_user: UserSchema):
 with engine.connect() as conn: #Es la conexión con la base de datos y solo está abierta cuando se usa
    new_user = data_user.dict()
    new_user["contrasenia_usuario"] = generate_password_hash(data_user.contrasenia_usuario, "pbkdf2:sha256:30", 15)

    conn.execute(users.insert().values(new_user))
    conn.commit()

    return Response(status_code=HTTP_201_CREATED)

@user.post("/api/user/login", status_code=200)
def login_user(data_user: DataUser):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.usuario == data_user.usuario)).first()
        
        if result != None:
            
            check_passw = check_password_hash(result[4], data_user.contrasenia_usuario)
            
            if check_passw:
                return {
                    "status" : 200,
                    "message": "Si perro, metiste bien los datos"
                }
        return {
            "status" : HTTP_401_UNAUTHORIZED,
            "message": "No perro, metiste mal los datos"
        }


@user.put("/api/user/{user_id}", response_model=UserSchema)
def update_user(data_update: UserSchema, user_id: str):
    with engine.connect() as conn:
        encryp_passw = generate_password_hash(data_update.contrasenia_usuario, "pbkdf2:sha256:30", 15)
        conn.execute(
            users.update()
            .values(
                nombre_usuario=data_update.nombre_usuario,
                numero_doc_usuario=data_update.numero_doc_usuario,
                usuario=data_update.usuario,
                contrasenia_usuario=encryp_passw
            )
            .where(users.c.id == user_id)
        )
        conn.commit()
        
        updated_user = conn.execute(users.select().where(users.c.id == user_id)).first()
        if updated_user:
            updated_user_dict = {
                "id": updated_user.id,
                "nombre_usuario": updated_user.nombre_usuario,
                "numero_doc_usuario": updated_user.numero_doc_usuario,
                "usuario": updated_user.usuario,
                "contrasenia_usuario": updated_user.contrasenia_usuario
            }
            return updated_user_dict
        else:
            raise HTTPException(status_code=404, detail="User not found")

@user.delete("/api/user/{user_id}", status_code=HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    with engine.connect() as conn:
        conn.execute(users.delete().where(users.c.id == user_id))
        conn.commit()
        return Response(status_code=HTTP_204_NO_CONTENT)
