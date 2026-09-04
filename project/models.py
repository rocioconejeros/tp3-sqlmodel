from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Oficina(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    direccion: str

    personas: List["Persona"] = Relationship(back_populates="oficina")


class Persona(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    edad: Optional[int] = None
    puesto: Optional[str] = None

    oficina_id: Optional[int] = Field(default=None, foreign_key="oficina.id")
    oficina: Optional[Oficina] = Relationship(back_populates="personas")