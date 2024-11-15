import BBDD
import logicaJuego


def main():
    db = BBDD.BBDD()
    Juego = logicaJuego.Juego()
    jugadores = db.cargar_jugadores()

    nombre = input("Ingrese su nombre: ").capitalize()

    # Si el jugador no existe en el registro, se añade
    if nombre not in jugadores:
        jugadores[nombre] = {'ganadas': 0, 'perdidas': 0}

    while True:
        print("\n¡Bienvenido al juego del Ahorcado!")
        print("1. Jugar")
        print("2. Ver estadísticas")
        print("3. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            print("\nElige una temática:")
            print("1. Frutas")
            print("2. Conceptos Informáticos")
            print("3. Nombres de Personas")
            tematica_opcion = input("Elige una opción: ")

            if tematica_opcion == "1":
                tematica = "frutas"
            elif tematica_opcion == "2":
                tematica = "componentes"
            elif tematica_opcion == "3":
                tematica = "nombres"
            else:
                print("Opción inválida, eligiendo 'Frutas'.")
                tematica = "frutas"

            Juego.juegoAhorcado(nombre, tematica)

        elif opcion == "2":
            #Juego.mostrar_estadisticas(jugadores, nombre)
            print("hola")

        elif opcion == "3":
            print("\n¡Gracias por jugar!")
            break

        else:
            print("Opción inválida, elige nuevamente.")

if __name__ == "__main__":
    main()