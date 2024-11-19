import random
import tkinter as tk
from contextlib import nullcontext
from tkinter import PhotoImage, messagebox

import BBDD

# Crear la ventana principal (ventana inicial)
inicio = tk.Tk()
inicio.title("El Ahorcado. By Daniel Navarro")
inicio.geometry("500x500")
inicio.config(bg="black")
inicio.resizable(False, False)

# Crear la ventana del juego (que estará oculta inicialmente)
juego = tk.Toplevel(inicio)
juego.title("El Ahorcado")
juego.geometry("1010x515")
juego.config(bg="black")
juego.resizable(False, False)
juego.withdraw()  # Inicialmente ocultamos la ventana del juego

db = BBDD.BBDD()
botones_letras = []
tema = ""
nombre = ""  # Esta variable se usará para el nombre del jugador
palabra = ""
L_usadas = []
palabra_mostrada = ""
intentos = 7


def mostrarEstadisticas():
    nombre = entrada_nombre.get().capitalize()
    jugador = db.getJugador(nombre)  # Llamar a db para obtener estadísticas
    if jugador:
        # Crear una nueva ventana emergente
        ventana_estadisticas = tk.Toplevel(inicio)
        ventana_estadisticas.title(f"Estadísticas de {jugador['nombre']}")
        ventana_estadisticas.geometry("300x200")
        ventana_estadisticas.config(bg="black")

        # Mostrar las estadísticas del jugador en esta ventana
        lblNombre = tk.Label(ventana_estadisticas, text=f"Jugador: {jugador['nombre']}", fg="white", bg="black", font=("Helvetica", 12))
        lblNombre.pack(pady=10)

        lblGanadas = tk.Label(ventana_estadisticas, text=f"Partidas ganadas: {jugador['ganadas']}", fg="white", bg="black", font=("Helvetica", 12))
        lblGanadas.pack(pady=5)

        lblPerdidas = tk.Label(ventana_estadisticas, text=f"Partidas perdidas: {jugador['perdidas']}", fg="white", bg="black", font=("Helvetica", 12))
        lblPerdidas.pack(pady=5)

        # Botón para cerrar la ventana
        btnCerrar = tk.Button(ventana_estadisticas, text="Cerrar", command=ventana_estadisticas.destroy, bg="blue", fg="white", font=("Helvetica", 10, "bold"))
        btnCerrar.pack(pady=10)

    else:
        # Si no hay estadísticas para el jugador
        print(f"No se encontraron estadísticas para el jugador {nombre}.")


def iniciar_juego():
    global nombre, tema, db, palabra  # Añadimos db como variable global

    #db.borrar_jugadores()

    nombre = entrada_nombre.get()  # Obtener nombre del campo de texto
    if not nombre or nombre.startswith(" "):  # Validar que el nombre no esté vacío
        print("Por favor ingresa un nombre valido.")
        return  # No iniciar el juego si no hay nombre

    if not tema:  # Validar que se haya elegido un tema
        print("Por favor elige un tema.")
        return  # No iniciar el juego si no se ha elegido tema

    # Obtener la palabra aleatoria del tema elegido
    palabra = db.getPalabraAleatoria(tema).upper()  # Llamamos al metodo de la clase BBDD

    # Proceder con el resto de la lógica del juego
    actualizar_palabra()
    inicio.withdraw()  # Ocultamos la ventana principal
    juego.deiconify()  # Mostramos la ventana del juego
    crear_botones_abecedario()  # Creamos los botones del abecedario
    actualizar_imagen()  # Actualizamos la imagen inicial

# Función para crear los botones de las letras del abecedario
def crear_botones_abecedario():
    abecedario = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    for i, letra in enumerate(abecedario):
        boton = tk.Button(juego, text=letra, width=5, height=2, font=("Helvetica", 8, "bold"), command=lambda l=letra: boton_presionado(l, boton))
        botones_letras.append(boton)
        boton.grid(row=i // 9, column=i % 9, padx=5, pady=5)

def desactivar_botones():
    for boton in botones_letras:
        boton.config(state="disabled")

def boton_presionado(letra, boton):
    global intentos, L_usadas, palabra, nombre  # Aseguramos que usamos la variable global de la palabra y letras usadas
    if letra not in L_usadas:
        L_usadas.append(letra)  # Añadir la letra a la lista de letras usadas
        print(L_usadas)

    # Comprobar si la letra está en la palabra
    if letra in palabra:
        print(f"¡Bien! La letra {letra} está en la palabra.")
        L_usadas.append(letra)
    else:
        print(f"La letra {letra} no está en la palabra.")
        intentos -= 1
        print(f"Te quedan {intentos} intentos.")
        L_usadas.append(letra)
    # Actualizar la visualización de la palabra
    actualizar_palabra()
    actualizar_intentos()
    actualizar_imagen()

    # Comprobar si el jugador ha ganado
    if all(letra in L_usadas or letra == " " for letra in palabra):  # Verificamos si todas las letras han sido adivinadas
        print(f"¡Felicidades! Has adivinado la palabra: {palabra}")
        ganadas = db.getGanadas(nombre) + 1
        perdidas = db.getPerdidas(nombre)
        db.actualizarJugador(nombre, ganadas, perdidas)
        messagebox.showinfo("¡Felicidades!", f"Has adivinado la palabra: {palabra}")
        desactivar_botones()  # Desactivamos los botones después de ganar
        mostrarEstadisticas()
        reiniciar_juego()

    # Comprobar si el jugador ha perdido
    if intentos == 0:
        print(f"¡Has perdido! La palabra era {palabra}.")
        perdidas = db.getPerdidas(nombre) + 1
        ganadas = db.getGanadas(nombre)
        db.actualizarJugador(nombre, ganadas, perdidas)
        messagebox.showinfo("Perdiste", f"Has perdido. La palabra era: {palabra}")
        desactivar_botones()  # Desactivamos los botones después de perder
        mostrarEstadisticas()
        reiniciar_juego()


# Función para actualizar la visualización de la palabra
def actualizar_palabra():
    global palabra, palabra_mostrada
    if palabra == "":
        palabra = db.getPalabraAleatoria(tema).upper()
        palabra_mostrada = "".join(f"{char} " if char in L_usadas or char == " " else "_ " for char in palabra)

    else:
        palabra_mostrada = "".join(f"{char} " if char in L_usadas or char == " " else "_ " for char in palabra)

    etiqueta_palabra.config(text=palabra_mostrada)


# Función para actualizar los intentos restantes
def actualizar_intentos():
    etiqueta_intentos.config(text=f"Intentos restantes: {intentos}")

# Función para reiniciar el juego
def reiniciar_juego():
    global intentos, L_usadas, palabra, palabra_mostrada
    intentos = 7
    L_usadas = []
    palabra = ""

    palabra_mostrada = ""
    actualizar_palabra()
    actualizar_imagen()
    actualizar_intentos()

    # Rehabilitar los botones de las letras
    for boton in botones_letras:
        boton.config(state="normal")  # Reactivamos los botones

    # Si necesitas crear los botones nuevamente (en caso de que se hayan destruido al reiniciar)
    crear_botones_abecedario()

# Botón para guardar el nombre ingresado
def guardar_nombre():
    global nombre
    nombre = entrada_nombre.get().capitalize()  # Obtiene el nombre del campo de texto

    if db.getJugador(nombre) is None and not nombre.startswith(" "):  # Verificamos si el jugador no existe
        db.guardarJugador(nombre, ganadas=0, perdidas=0)
        messagebox.showinfo("Éxito", f"Jugador {nombre} guardado exitosamente.")
    else:
        messagebox.showwarning("ERROR", "NOMBRE NO VALIDO")

# Función para actualizar la imagen
def actualizar_imagen():
    # Definir el nombre del archivo de imagen según el valor de contador
    ruta = "resources\\"
    if 1 <= intentos <= 7:
        print(intentos)
        imagen = PhotoImage(file=f"{ruta}{7 - intentos}.png")
        etiqueta_imagen.config(image=imagen)
        etiqueta_imagen.image = imagen  # Mantener una referencia de la imagen para evitar que se borre
    else:
        print("Contador fuera de rango")


# Etiqueta para mostrar la imagen
etiqueta_imagen = tk.Label(juego)
etiqueta_imagen.place(x=500, y=5)

# Etiqueta para mostrar la palabra
etiqueta_palabra = tk.Label(juego, text="".join(palabra_mostrada), fg="white", bg="black", font=("Helvetica", 20))
etiqueta_palabra.place(x=120, y=200)

# Etiqueta para mostrar los intentos restantes
etiqueta_intentos = tk.Label(juego, text=f"Intentos restantes: {intentos}", fg="white", bg="black", font=("Helvetica", 12))
etiqueta_intentos.place(x=250, y=400)

# Nombre juego
lbTitulo = tk.Label(inicio, text="EL AHORCADO", fg="white", bg="black", font=("Helvetica", 30, "bold"))
lbTitulo.place(x=110, y=100)

# Botón para iniciar el juego
btnInicio = tk.Button(inicio, text="INICIAR", width=20, bg="blue", fg="white", font=("Helvetica", 15, "bold"), command=iniciar_juego)
btnInicio.place(x=130, y=400)

# Botón para mostrar las estadísticas
btnEstadisticas = tk.Button(inicio, text="ESTADISTICAS", width=13, bg="white", fg="black", font=("Helvetica", 7, "bold"), command=lambda: mostrarEstadisticas())
btnEstadisticas.place(x=210, y=450)

btnReinicio = tk.Button(juego, text="REINICIAR", width=13, bg="white", fg="black", font=("Helvetica", 12, "bold"), command=lambda: reiniciar_juego())
btnReinicio.place(x=20,y=460)

# Botón para cerrar la ventana
boton_salir = tk.Button(inicio, text="SALIR", bg="red", fg="white", command=inicio.quit)
boton_salir.place(x=450, y=10)

# Botones de las temáticas con "V" encima
def mostrar_vencima_de(boton):
    # Ocultar todas las etiquetas "V"
    v_fruta.place_forget()
    v_componentes.place_forget()
    v_nombres.place_forget()

    global tema

    # Mostrar la "V" correspondiente
    if boton == btnFruta:
        v_fruta.place(x=87, y=160)
        tema = "frutas"
    elif boton == btnComponentes:
        v_componentes.place(x=240, y=160)
        tema = "componentes"
    elif boton == btnNombres:
        v_nombres.place(x=410, y=160)
        tema = "nombres"

# Botones de las temáticas (esto parece estar mal configurado, debería estar dentro de un menú de selección)
btnFruta = tk.Button(inicio, text="FRUTA", font=("Helvetica", 10, "bold"), command=lambda: mostrar_vencima_de(btnFruta))
btnFruta.place(x=70, y=200)
btnComponentes = tk.Button(inicio, text="COMPONENTES INFORMATICOS", font=("Helvetica", 10, "bold"), command=lambda: mostrar_vencima_de(btnComponentes))
btnComponentes.place(x=145, y=200)
btnNombres = tk.Button(inicio, text="NOMBRES", font=("Helvetica", 10, "bold"), command=lambda: mostrar_vencima_de(btnNombres))
btnNombres.place(x=380, y=200)

# Etiqueta para el nombre del jugador
lbNombre = tk.Label(inicio, text="Ingresa tu nombre:", fg="white", bg="black", font=("Helvetica", 12))
lbNombre.place(x=185, y=250)

# Campo de texto para que el jugador ingrese su nombre
entrada_nombre = tk.Entry(inicio, font=("Helvetica", 12), width=22)
entrada_nombre.place(x=150, y=280)

btnGuardarNombre = tk.Button(inicio, text="GUARDAR", width=20, bg="blue", fg="white", font=("Helvetica", 10, "bold"), command=guardar_nombre)
btnGuardarNombre.place(x=170, y=320)

# Etiqueta "V" para cada tema, inicialmente no visible
v_fruta = tk.Label(inicio, text="v", fg="white", bg="black", font=("Helvetica", 20))
v_componentes = tk.Label(inicio, text="v", fg="white", bg="black", font=("Helvetica", 20))
v_nombres = tk.Label(inicio, text="v", fg="white", bg="black", font=("Helvetica", 20))


inicio.mainloop()
