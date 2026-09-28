from sqlmodel import SQLModel, create_engine

sqlite_file_name = "oficinas.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# echo=False para que la consola muestre solo la salida del programa.
# Poné echo=True si querés ver el SQL que genera SQLModel.
engine = create_engine(sqlite_url, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)