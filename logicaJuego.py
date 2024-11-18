import random
import BBDD

class Juego:
    def __init__(self):
        self.db = BBDD.BBDD()

    def mostrarEstadisticas(self, nombre):
        jugador = self.db.getJugador(nombre)
        if jugador:
            print(f"Estadísticas de {jugador['nombre']}:")
            print(f"Ganadas: {jugador['ganadas']}")
            print(f"Perdidas: {jugador['perdidas']}")
        else:
            print(f"No se encontraron estadísticas para el jugador {nombre}.")

    def getPalabraAleatoria(self, tematica):
        # Obtener palabras desde la base de datos
        if tematica == "frutas":
            lista_palabras = self.db.getFrutas()
        elif tematica == "componentes":
            lista_palabras = self.db.getComponentes()
        elif tematica == "nombres":
            lista_palabras = self.db.getNombres()
        else:
            raise ValueError("Temática no válida. Debe ser 'frutas', 'componentes' o 'nombres'.")

        if not lista_palabras:
            print(f"Advertencia: La lista de palabras para la temática '{tematica}' está vacía.")
        return random.choice(lista_palabras) if lista_palabras else None

    def juegoAhorcado(self, nombre, tematica):
        palabra = self.getPalabraAleatoria(tematica).upper()
        intentos = 6
        L_usadas = [" "]

        while intentos > 0:
            # Imprimir la palabra con las letras adivinadas y guiones bajos para las no adivinadas
            for letra in palabra:
                if letra == " ":
                    print("   ", end="")
                elif letra in L_usadas:
                    print(letra, end=" ")
                else:
                    print(" _ ", end=" ")
            print("")

            # Pedir una letra al jugador
            letra = input("Introduce una letra: ").upper()

            # Validar que la letra no haya sido ingresada antes
            if letra in L_usadas:
                print(f"La letra {letra} ya fue usada. ¡Prueba otra!")
                continue

            # Comprobar si la letra está en la palabra
            if letra in palabra:
                print(f"¡Bien! La letra {letra} está en la palabra.")
                L_usadas.append(letra)
            else:
                print(f"La letra {letra} no está en la palabra.")
                intentos -= 1
                print(f"Te quedan {intentos} intentos.")

            # Si se acaba el número de intentos
            if intentos == 0:
                print(f"¡Has perdido! La palabra era {palabra}.")
                perdidas = self.db.getPerdidas(nombre) + 1
                ganadas = self.db.getGanadas(nombre)
                self.db.actualizarJugador(nombre, ganadas, perdidas)

            # Si el jugador ha adivinado toda la palabra
            if all(letra in L_usadas for letra in palabra if letra != " "):
                print(f"¡Felicidades! Has adivinado la palabra: {palabra}")
                ganadas = self.db.getGanadas(nombre) + 1
                perdidas = self.db.getPerdidas(nombre)
                self.db.actualizarJugador(nombre, ganadas, perdidas)
                break
