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

        palabra = Juego.getPalabraAleatoria(self, tematica).upper()
        intentos = 6
        L_usadas = []

        while intentos > 0:
            # Imprimir la palabra con las letras adivinadas y guiones bajos para las no adivinadas
            for letra in palabra:
                if letra in L_usadas:  # Si la letra ya ha sido adivinada, la mostramos
                    print(letra, end=" ")
                else:
                    print(" _ ", end=" ")
            print("")


            print("INTRODUCE UNA LETRA")
            letra = input("LETRA: ").upper()

            # Validar que la letra no haya sido ingresada antes
            if letra in L_usadas:
                print(f"LA {letra} YA FUE USADA. PRUEBA OTRA.")
                continue

            # Comprobar si la letra está en la palabra
            if letra in palabra:
                L_usadas.append(letra)
            else:
                print("ESA LETRA NO ESTÁ EN LA PALABRA")
                intentos -= 1
                print(f"TE QUEDAN {intentos} INTENTOS")

            if intentos == 0:
                print(f"HAS PERDIDO. LA PALABRA ERA {palabra}")
                self.db.actualizarJugador(ganadas=+0,perdidas=+1)


            if all(letra in L_usadas for letra in palabra):
                print(f"¡FELICIDADES! LA PALABRA ERA {palabra}")
                self.db.actualizarJugador(ganadas=+1,perdidas=+0)
                break