TP 3 - SQLModel: Oficinas y Personas

Trabajo práctico de Práctica Profesionalizante I (Tecnicatura Superior en Desarrollo de Software, Instituto Técnico Superior Córdoba).

Estudiante: Rocio Conejeros

Es una app de consola hecha con SQLModel y SQLite. Tiene dos tablas: oficina y persona. Cada persona trabaja en una sola oficina, y una oficina puede tener varias personas. La relación está armada con Relationship(), puede ir de un lado al otro

python
persona.oficina -> la oficina de esa persona
oficina.personas -> la lista de personas de esa oficina

Al ejecutar el programa se van haciendo, una atrás de otra, todas las operaciones del CRUD y se muestra lo que pasa por consola.

Está organizado con la siguiente estructura

```
tp3-sqlmodel/
├── project/
│   ├── __init__.py
│   ├── models.py      # las clases Oficina y Persona
│   ├── database.py    # el engine y la creación de las tablas
│   └── app.py         # las operaciones y el punto de entrada
├── .gitignore
├── requirements.txt
└── README.md
```

Para correrlo

Necesitás tener Python instalado (yo usé la 3.12).

1. Clonar el repo y entrar a la carpeta:

   git clone https://github.com/rocioconejeros/tp3-sqlmodel
   cd tp3-sqlmodel
   

2. Crear el entorno virtual y activarlo:

   python -m venv venv
   venv\Scripts\Activate.ps1

   Esa es la forma para PowerShell en Windows. Si tira un error de permisos, primero se debe correr esto y probar de nuevo:

   Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

   En Linux se activa con `source venv/bin/activate`.

3. Instalar las dependencias:

   pip install -r requirements.txt

4. Ejecutar la app, parado en la carpeta tp3-sqlmodel (la que tiene adentro a project):

   python -m project.app

Al ejecutarlo se crea un archivo oficinas.db con la base de datos. Si querés volver a correr todo desde cero, borrá ese archivo antes, para que no se dupliquen los datos.

El programa realiza lo siguiente:

- **Create:** crea dos oficinas (create_oficinas) y dos personas (create_personas). A las personas se les asigna la oficina con el atributo oficina=, no con el id.
- **Read:** lista las personas de una oficina usando oficina.personas (listar_personas_de_oficina), muestra una consulta con JOIN entre las dos tablas (personas_con_oficina_join) y busca personas por nombre con un where (buscar_persona_por_nombre).
- **Update:** pasa una persona de una oficina a otra (reasignar_persona).
- **Delete:** elimina una persona (eliminar_persona) y elimina una oficina que todavía tiene gente (eliminar_oficina).

Al último: al borrar una oficina con personas, las personas no se borran. Como la relación no tiene cascade, quedan con oficina_id en NULL, o sea, sin oficina. Eso se ve al final de la salida del programa. El detalle está explicado en el informe.
