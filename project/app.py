from sqlmodel import Session, select
from .database import engine, create_db_and_tables
from .models import Oficina, Persona


def create_oficinas():
    with Session(engine) as session:
        of1 = Oficina(nombre="Casa Central", direccion="San Martín 123")
        of2 = Oficina(nombre="Sucursal Norte", direccion="Av. Colón 321")
        session.add(of1)
        session.add(of2)
        session.commit()


def create_personas():
    with Session(engine) as session:
        oficina = session.exec(
            select(Oficina).where(Oficina.nombre == "Casa Central")
        ).first()

        p1 = Persona(nombre="Ana", edad=30, puesto="Secretaria", oficina=oficina)
        p2 = Persona(nombre="Jose", edad=32, puesto="Recepcionista", oficina=oficina)
        session.add(p1)
        session.add(p2)
        session.commit()


def listar_personas_de_oficina(nombre_oficina: str):
    with Session(engine) as session:
        oficina = session.exec(
            select(Oficina).where(Oficina.nombre == nombre_oficina)
        ).first()
        print(f"\nPersonas en {oficina.nombre}:")
        for p in oficina.personas:
            print(f"  - {p.nombre} ({p.puesto})")


def personas_con_oficina_join():
    with Session(engine) as session:
        resultados = session.exec(
            select(Persona, Oficina).join(Oficina)
        ).all()
        print("\nJOIN Persona-Oficina:")
        for persona, oficina in resultados:
            print(f"  {persona.nombre} -> {oficina.nombre}")


def buscar_persona_por_nombre(nombre: str):
    with Session(engine) as session:
        personas = session.exec(
            select(Persona).where(Persona.nombre == nombre)
        ).all()
        print(f"\nBúsqueda por nombre '{nombre}':")
        for p in personas:
            print(f"  - {p.nombre}, {p.edad} años")
        return personas


def reasignar_persona(persona_id: int, nueva_oficina_nombre: str):
    with Session(engine) as session:
        persona = session.get(Persona, persona_id)
        nueva_oficina = session.exec(
            select(Oficina).where(Oficina.nombre == nueva_oficina_nombre)
        ).first()
        persona.oficina = nueva_oficina
        session.add(persona)
        session.commit()
        session.refresh(persona)
        print(f"\n{persona.nombre} reasignada a {nueva_oficina_nombre}")


def eliminar_persona(persona_id: int):
    with Session(engine) as session:
        persona = session.get(Persona, persona_id)
        session.delete(persona)
        session.commit()
        print(f"\nPersona {persona_id} eliminada")


if __name__ == "__main__":
    create_db_and_tables()
    create_oficinas()
    create_personas()
    listar_personas_de_oficina("Casa Central")
    personas_con_oficina_join()
    buscar_persona_por_nombre("Ana")
    reasignar_persona(1, "Sucursal Norte")
    listar_personas_de_oficina("Sucursal Norte")
    eliminar_persona(2)