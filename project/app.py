from sqlmodel import Session, select

from .database import create_db_and_tables, engine
from .models import Oficina, Persona


# ---------------------------------------------------------------- CREATE
def create_oficinas():
    with Session(engine) as session:
        oficina_central = Oficina(nombre="Casa Central", direccion="San Martín 123")
        oficina_norte = Oficina(nombre="Sucursal Norte", direccion="Av. Colón 456")
        session.add(oficina_central)
        session.add(oficina_norte)
        session.commit()
        print("Oficinas creadas: Casa Central y Sucursal Norte")


def create_personas():
    with Session(engine) as session:
        central = session.exec(
            select(Oficina).where(Oficina.nombre == "Casa Central")
        ).one()
        norte = session.exec(
            select(Oficina).where(Oficina.nombre == "Sucursal Norte")
        ).one()

        # La oficina se asigna con el atributo de relación, no con el id
        ana = Persona(nombre="Ana", edad=30, puesto="Secretaria", oficina=central)
        luis = Persona(nombre="Luis", edad=45, puesto="Gerente", oficina=norte)
        session.add(ana)
        session.add(luis)
        session.commit()
        print("Personas creadas: Ana (Casa Central) y Luis (Sucursal Norte)")


# ------------------------------------------------------------------ READ
def listar_personas_de_oficina(nombre_oficina: str):
    with Session(engine) as session:
        oficina = session.exec(
            select(Oficina).where(Oficina.nombre == nombre_oficina)
        ).one()
        print(f"Personas de {oficina.nombre}:")
        for persona in oficina.personas:  # navegación oficina -> personas
            print(f"  - {persona.nombre}, {persona.edad} años, {persona.puesto}")


def personas_con_oficina_join():
    with Session(engine) as session:
        # JOIN entre Persona y Oficina
        statement = select(Persona, Oficina).join(Oficina)
        resultados = session.exec(statement).all()
        print("Personas con su oficina (JOIN):")
        for persona, oficina in resultados:
            print(f"  - {persona.nombre} trabaja en {oficina.nombre} ({oficina.direccion})")


def buscar_persona_por_nombre(nombre: str):
    with Session(engine) as session:
        statement = select(Persona).where(Persona.nombre == nombre)
        personas = session.exec(statement).all()
        print(f"Búsqueda por nombre '{nombre}':")
        for persona in personas:
            # navegación persona -> oficina
            nombre_oficina = persona.oficina.nombre if persona.oficina else "sin oficina"
            print(f"  - {persona.nombre}, {persona.edad} años, oficina: {nombre_oficina}")


# ---------------------------------------------------------------- UPDATE
def reasignar_persona(nombre_persona: str, nombre_oficina_destino: str):
    with Session(engine) as session:
        persona = session.exec(
            select(Persona).where(Persona.nombre == nombre_persona)
        ).one()
        destino = session.exec(
            select(Oficina).where(Oficina.nombre == nombre_oficina_destino)
        ).one()

        persona.oficina = destino  # se reasigna con la relación
        session.add(persona)
        session.commit()
        print(f"{nombre_persona} fue reasignada/o a {nombre_oficina_destino}")


# ---------------------------------------------------------------- DELETE
def eliminar_persona(nombre_persona: str):
    with Session(engine) as session:
        persona = session.exec(
            select(Persona).where(Persona.nombre == nombre_persona)
        ).one()
        session.delete(persona)
        session.commit()
        print(f"Persona eliminada: {nombre_persona}")


def eliminar_oficina(nombre_oficina: str):
    with Session(engine) as session:
        oficina = session.exec(
            select(Oficina).where(Oficina.nombre == nombre_oficina)
        ).one()
        cantidad = len(oficina.personas)
        print(f"Eliminando {nombre_oficina}, que tiene {cantidad} persona(s)...")

        # La relación no tiene cascade: las personas NO se borran.
        # SQLAlchemy pone su oficina_id en NULL.
        session.delete(oficina)
        session.commit()

    with Session(engine) as session:
        print("Personas después de eliminar la oficina:")
        for persona in session.exec(select(Persona)).all():
            print(
                f"  - {persona.nombre}: oficina_id={persona.oficina_id}, "
                f"oficina={persona.oficina}"
            )


# ------------------------------------------------------------------ MAIN
def main():
    create_db_and_tables()

    print("\n=== CREATE ===")
    create_oficinas()
    create_personas()

    print("\n=== READ ===")
    listar_personas_de_oficina("Casa Central")
    personas_con_oficina_join()
    buscar_persona_por_nombre("Ana")

    print("\n=== UPDATE ===")
    reasignar_persona("Ana", "Sucursal Norte")
    listar_personas_de_oficina("Sucursal Norte")

    print("\n=== DELETE ===")
    eliminar_persona("Luis")
    eliminar_oficina("Sucursal Norte")


if __name__ == "__main__":
    main()