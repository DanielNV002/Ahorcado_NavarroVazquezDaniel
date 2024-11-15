import os
import random

import BBDD


class Juego:

    db = BBDD.BBDD

    def get_palabra_aleatoria(self, tematica, db):
        if tematica == "frutas":
            lista_palabras = db.get_frutas()
        elif tematica == "componentes":
            lista_palabras = db.get_componentes()
        elif tematica == "nombres":
            lista_palabras = db.get_nombres()
        else:
            raise ValueError("Temática no válida. Debe ser 'frutas', 'componentes' o 'nombres'.")

        if not lista_palabras:  # Verificar si la lista está vacía
            print(f"Advertencia: La lista de palabras para la temática '{tematica}' está vacía.")
        return random.choice(lista_palabras) if lista_palabras else None  # Si la lista está vacía, devuelve None

    def juego_ahorcado(jugador, tematica, db):
        palabra = db.get_palabra_aleatoria(tematica).upper()
        letras_adivinadas = ["_"] * len(palabra)
        intentos = 6  # Número de intentos antes de que el monigote sea ahorcado
        letras_erradas = []

        while intentos > 0:
            print(f"\nPalabra: {' '.join(letras_adivinadas)}")
            print(f"Letras erradas: {', '.join(letras_erradas)}")
            print(f"Intentos restantes: {intentos}")

            letra = input("Adivina una letra: ").upper()

            if len(letra) != 1 or not letra.isalpha():
                print("Por favor, ingresa una sola letra válida.")
                continue

            if letra in letras_adivinadas or letra in letras_erradas:
                print("Ya has adivinado o errando esta letra.")
                continue

            if letra in palabra:
                for i in range(len(palabra)):
                    if palabra[i] == letra:
                        letras_adivinadas[i] = letra
                if "_" not in letras_adivinadas:
                    print(f"\n¡Felicidades! Has adivinado la palabra: {palabra}")
                    jugador['ganadas'] += 1
                    return
            else:
                letras_erradas.append(letra)
                intentos -= 1

        print(f"\n¡Perdiste! La palabra era: {palabra}")
        jugador['perdidas'] += 1


    # Mostrar estadísticas del jugador
    def mostrar_estadisticas(jugadores, nombre):
        if nombre in jugadores:
            print(f"{nombre} ha ganado {jugadores[nombre]['ganadas']} partidas y perdido {jugadores[nombre]['perdidas']} partidas.")
        else:
            print("Jugador no encontrado.")