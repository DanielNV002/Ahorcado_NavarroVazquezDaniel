import sqlite3

conn = sqlite3.connect("listaObjetosAhorcado.db")

cursor  = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS frutas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    )
    """
)

cursor.execute(
    """INSERT INTO frutas (nombre) VALUES (?)""",
    ("Manzana",)
)

cursor.execute("SELECT * FROM frutas")

resultado = cursor.fetchall()
for fila in resultado:
    print(fila)