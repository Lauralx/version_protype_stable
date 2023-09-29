from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: Optional[str]
    nombre_usuario: str
    numero_doc_usuario: int
    usuario: str
    contrasenia_usuario: str

class DataUser(BaseModel):
    usuario: str
    contrasenia_usuario: str
        