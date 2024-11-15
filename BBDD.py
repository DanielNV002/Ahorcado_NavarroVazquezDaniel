import sqlite3

class BBDD:

    def __init__(self):
        # Inicializamos la conexión y el cursor como atributos de la clase
        self.conn = sqlite3.connect("listaObjetosAhorcado.db")
        self.cursor = self.conn.cursor()

        # Crear las tablas si no existen
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS frutas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS componentes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS nombres(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS jugadores(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                ganadas INTEGER DEFAULT 0,
                perdidas INTEGER DEFAULT 0
            )
            """
        )

        # Lista de frutas que quieres insertar (solo si no existen ya)
        frutas = [
            "Manzana", "Pera", "Platano", "Naranja", "Fresa", "Uva", "Mango",
            "Cereza", "Piña", "Kiwi", "Melon", "Sandia", "Papaya", "Coco", "Granada",
            "Dragon", "Durian", "Tomate", "Frambuesa", "Mora"
        ]
        for fruta in frutas:
            self.cursor.execute("INSERT OR IGNORE INTO frutas (nombre) VALUES (?)", (fruta,))

        # Lista de componentes informáticos
        componentes = [
            "Procesador", "Placa Base", "Memoria RAM", "Disco Duro", "Tarjeta Grafica",
            "Fuente de Alimentacion", "Monitor", "Teclado", "Raton", "Cascos",
            "Caja", "SSD", "Tarjeta de Sonido", "Tarjeta de Red", "Refrigeracion",
            "Lector de CD", "Webcam", "Microfono", "Mando Xbox"
        ]
        for componente in componentes:
            self.cursor.execute("INSERT OR IGNORE INTO componentes (nombre) VALUES (?)", (componente,))

        # Lista de nombres
        nombres = [
            "Josema", "Victor", "Daniel", "Carla", "Andrea Rodriguez",
            "Patricia", "Andrea Catalan", "Ivan", "Alberto", "Nicolas",
            "Antonio", "Rafa", "Martin", "Raul", "Pablo",
            "Rodrigo", "Jose Ignacio", "Lucas", "Miguel", "Carmen"
        ]
        for nombre in nombres:
            self.cursor.execute("INSERT OR IGNORE INTO nombres (nombre) VALUES (?)", (nombre,))

        # Guardar los cambios
        self.conn.commit()

    def getJugadores(self):
        """Obtener todos los jugadores."""
        self.cursor.execute("SELECT * FROM jugadores")
        return self.cursor.fetchall()

    def getFrutas(self):
        """Obtener todas las frutas de la base de datos."""
        self.cursor.execute("SELECT nombre FROM frutas")
        return [fila[0] for fila in self.cursor.fetchall()]

    def getComponentes(self):
        """Obtener todos los componentes de la base de datos."""
        self.cursor.execute("SELECT nombre FROM componentes")
        return [fila[0] for fila in self.cursor.fetchall()]

    def getNombres(self):
        """Obtener todos los nombres de la base de datos."""
        self.cursor.execute("SELECT nombre FROM nombres")
        return [fila[0] for fila in self.cursor.fetchall()]

    def guardar_jugadores(self, jugadores):
        """Guardar los datos de los jugadores en la base de datos"""
        # Limpiar la tabla de jugadores (si es necesario)
        self.cursor.execute("DELETE FROM jugadores")

        # Insertar jugadores en la base de datos
        for jugador, stats in jugadores.items():
            self.cursor.execute(
                "INSERT INTO jugadores (nombre, ganadas, perdidas) VALUES (?, ?, ?)",
                (jugador, stats["ganadas"], stats["perdidas"])
            )

        # Guardar los cambios en la base de datos
        self.conn.commit()

    def cargar_jugadores(self):
        """Cargar los datos de los jugadores desde la base de datos"""
        self.cursor.execute("SELECT nombre, ganadas, perdidas FROM jugadores")
        jugadores = {}

        # Recorrer los resultados y almacenar los jugadores en un diccionario
        for nombre, ganadas, perdidas in self.cursor.fetchall():
            jugadores[nombre] = {"ganadas": ganadas, "perdidas": perdidas}

        return jugadores

    def close(self):
        """Cerrar la conexión a la base de datos."""
        self.conn.close()
