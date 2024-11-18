import tkinter as tk
from tkinter import messagebox, simpledialog

from PIL import Image, ImageTk

import BBDD
import logicaJuego


class JuegoGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Juego del Ahorcado")
        self.geometry("600x400")
        self.resizable(False, False)

        # Instancia de la clase Juego
        self.juego = logicaJuego.Juego()
        self.db = BBDD.BBDD()

        self.nombre_jugador = None
        self.tematica = None
        self.palabra = None
        self.intentos = 6
        self.L_usadas = []
        self.palabra_adivinada = []

        self.iniciar_menu()

    def iniciar_menu(self):
        """Pantalla principal del juego para elegir opciones"""
        self.clear_window()



        if self.nombre_jugador is None:
            self.nombre_jugador = simpledialog.askstring("Nombre del Jugador", "Ingresa tu nombre:").capitalize()
            if not self.nombre_jugador:
                messagebox.showwarning("Nombre inválido", "Debes ingresar un nombre.")
                return

        tk.Label(self, text="Bienvenido al Juego del Ahorcado", font=("Arial", 16), bg="#FFFFFF").pack(pady=20)

        tk.Button(self, text="Jugar", font=("Arial", 12), width=20, command=self.elegir_tematica, bg="#1278e5", foreground="#FFFFFF").pack(pady=10)
        tk.Button(self, text="Ver estadísticas", font=("Arial", 12), width=20, command=self.ver_estadisticas, bg="#1278e5", foreground="#FFFFFF").pack(pady=10)
        tk.Button(self, text="Salir", font=("Arial", 12), width=20, command=self.quit, bg="#1278e5", foreground="#FFFFFF").pack(pady=10)

    def elegir_tematica(self):
        """Pantalla para elegir la temática"""
        self.clear_window()

        tk.Label(self, text="Elige una temática", font=("Arial", 14), bg="#FFFFFF").pack(pady=10)

        tk.Button(self, text="Frutas", font=("Arial", 12), width=20, command=lambda: self.iniciar_juego("frutas"), bg="#1278e5", foreground="#FFFFFF").pack(pady=5)
        tk.Button(self, text="Conceptos Informáticos", font=("Arial", 12), width=20, command=lambda: self.iniciar_juego("componentes"), bg="#1278e5", foreground="#FFFFFF").pack(pady=5)
        tk.Button(self, text="Nombres de Personas", font=("Arial", 12), width=20, command=lambda: self.iniciar_juego("nombres"), bg="#1278e5", foreground="#FFFFFF").pack(pady=5)

    def iniciar_juego(self, tematica):
        """Inicia el juego con la temática seleccionada"""
        self.tematica = tematica
        self.palabra = self.juego.getPalabraAleatoria(tematica).upper()
        self.intentos = 6
        self.L_usadas = []
        self.palabra_adivinada = ["_"] * len(self.palabra)
        self.actualizar_palabra()

    def actualizar_palabra(self):
        """Actualiza la palabra mostrada y los intentos restantes en la UI"""
        self.clear_window()

        # Mostrar la palabra con las letras adivinadas y guiones bajos para las no adivinadas
        tk.Label(self, text="Palabra: " + " ".join(self.palabra_adivinada), font=("Arial", 16), bg="#FFFFFF").pack(pady=20)
        tk.Label(self, text=f"Te quedan {self.intentos} intentos", font=("Arial", 12), bg="#FFFFFF").pack(pady=10)

        # Entrada para la letra
        self.entry_letra = tk.Entry(self, font=("Arial", 12), bg="#000000", fg="#00ff13")
        self.entry_letra.pack(pady=10)

        # Botón para ingresar letra
        self.button_letra = tk.Button(self, text="Ingresar Letra", font=("Arial", 12), command=self.ingresar_letra, bg="#1278e5", foreground="#FFFFFF")
        self.button_letra.pack(pady=10)
        self.mostrar_imagen(self.intentos)

    def ingresar_letra(self):
        """Metodo que maneja la entrada de letras y actualiza el estado del juego"""
        letra = self.entry_letra.get().upper()

        # Validar si la letra ya fue usada
        if letra in self.L_usadas:
            messagebox.showwarning("Letra ya usada", f"La letra {letra} ya fue usada. ¡Prueba otra!")
            return

        self.L_usadas.append(letra)

        # Verificar si la letra está en la palabra
        if letra in self.palabra:
            for i, char in enumerate(self.palabra):
                if char == letra:
                    self.palabra_adivinada[i] = letra
        else:
            self.intentos -= 1

        self.entry_letra.delete(0, tk.END)  # Limpiar la entrada de la letra
        self.actualizar_palabra()

        # Comprobar si el jugador ha ganado
        if "_" not in self.palabra_adivinada:
            messagebox.showinfo("¡Felicidades!", f"¡Has adivinado la palabra: {self.palabra}!")
            self.guardar_estadisticas(True)
            self.iniciar_menu()

        # Comprobar si el jugador ha perdido
        if self.intentos == 0:
            messagebox.showinfo("¡Perdido!", f"¡Has perdido! La palabra era {self.palabra}.")
            self.guardar_estadisticas(False)
            self.iniciar_menu()

    def guardar_estadisticas(self, gano):
        """Guardar estadísticas del jugador"""
        jugador = self.db.getJugador(self.nombre_jugador)
        if jugador:
            ganadas = self.db.getGanadas(self.nombre_jugador) + 1 if gano else self.db.getGanadas(self.nombre_jugador)
            perdidas = self.db.getPerdidas(self.nombre_jugador) + 1 if not gano else self.db.getPerdidas(self.nombre_jugador)
            self.db.actualizarJugador(self.nombre_jugador, ganadas, perdidas)

    def ver_estadisticas(self):
        """Muestra las estadísticas del jugador"""
        jugador = self.db.getJugador(self.nombre_jugador)
        if jugador:
            stats = f"Ganadas: {jugador['ganadas']}\nPerdidas: {jugador['perdidas']}"
            messagebox.showinfo("Estadísticas", stats)
        else:
            messagebox.showwarning("Jugador no encontrado", "No se encontraron estadísticas para este jugador.")

    def clear_window(self):
        """Limpia la ventana de widgets anteriores"""
        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_imagen(self, contador):
        """Mostrar imágenes dependiendo de los intentos restantes"""
        global photo
        imagen = None  # Inicializar la imagen a None

        if contador == 6:
            image = Image.open("resources/1.png")
            photo = ImageTk.PhotoImage(image)
        elif contador == 5:
            image = Image.open("resources/2.png")
            photo = ImageTk.PhotoImage(image)
        elif contador == 4:
            image = Image.open("resources/3.png")
            photo = ImageTk.PhotoImage(image)
        elif contador == 3:
            image = Image.open("resources/4.png")
            photo = ImageTk.PhotoImage(image)
        elif contador == 2:
            image = Image.open("resources/5.png")
            photo = ImageTk.PhotoImage(image)
        elif contador == 1:
            image = Image.open("resources/6.png")
            photo = ImageTk.PhotoImage(image)

        # Mostrar la imagen en un Label si se ha cargado correctamente
        if imagen:
            label = tk.Label(self, image=photo)
            label.image = imagen  # Retener una referencia a la imagen
            label.place(x=100, y=100)


if __name__ == "__main__":
    app = JuegoGUI()
    app.config(bg="#FFFFFF")
    app.mainloop()
