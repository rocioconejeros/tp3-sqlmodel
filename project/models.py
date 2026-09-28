from sqlmodel import Field, Relationship, SQLModel


class Oficina(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    direccion: str

    # Lado de la relación: lista de personas de esta oficina
    personas: list["Persona"] = Relationship(back_populates="oficina")


class Persona(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    edad: int | None = None
    puesto: str | None = None

    # Clave foránea. Es opcional (None) para que una persona pueda quedar sin oficina, por ejemplo si se borra la oficina a la que pertenecía.
    oficina_id: int | None = Field(default=None, foreign_key="oficina.id")

    # Lado "muchos" de la relación: la oficina de esta persona
    oficina: Oficina | None = Relationship(back_populates="personas")