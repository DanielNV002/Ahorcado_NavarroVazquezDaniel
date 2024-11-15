import BBDD
import logicaJuego


def main():
    db = BBDD.BBDD()
    Juego = logicaJuego.Juego()
    jugadores = db.cargar_jugadores()

    nombre = input("Ingrese su nombre: ").capitalize()

    jugador = db.getJugador(nombre)  # Metodo que obtiene al jugador de la base de datos

    if jugador is None:  # Si no existe el jugador en la base de datos
        db.guardarJugador(nombre, ganadas=0, perdidas=0)  # Guardamos al jugador con estadísticas iniciales
        print(f"Jugador {nombre} añadido a la base de datos.")
    else:
        print(f"Bienvenido de nuevo, {nombre}!")

    while True:
        print(f"\n¡Bienvenido al juego del Ahorcado {nombre}!")
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
            Juego.mostrarEstadisticas(nombre)

        elif opcion == "3":
            print("\n¡Gracias por jugar!")
            break

        else:
            print("Opción inválida, elige nuevamente.")

if __name__ == "__main__":
    main()