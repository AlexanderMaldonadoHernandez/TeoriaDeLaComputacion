import time
import random as rd
from tkinter import *

MAXIMO_TAMANO = 1000
LIMITE_ANIMACION = 10

def obtener_cadena():
    while True:
        modo = input("Seleccione un modo: \n1) Manual  \n2) Automático\n3) Salir\n")
        if modo == "1":
            while True:
                cadena = input("Ingrese la cadena binaria (0s y 1s): ").strip()
                if len(cadena) > MAXIMO_TAMANO:
                    print("Elija una cadena menor a 1000 caracteres.\n")
                    continue
                elif len(cadena) == 0:
                    print("Cadena vacía. Intente con otra cadena.\n")
                elif not set(cadena).issubset({'0','1'}):
                    print("La cadena debe contener solo ceros y unos.\n")
                else:
                    break
            break
        elif modo == "2":
            ceros = rd.randint(1, 1000)
            unos = rd.randint(0, MAXIMO_TAMANO - ceros)
            cadena = "0" * ceros + "1" * unos
            print("Se ha generado la siguiente cadena automáticamente:", cadena)
            break
        elif modo == "3":
            exit()
        else:
            print("Entrada inválida. Presione 1, 2, o 3.\n")
            continue
    return list(cadena) + ["B"]  # Espacio en blanco al final

def configurar_interfaz(cinta):
    ventana = Tk()
    ventana.title("Máquina de Turing")
    ventana.geometry("1600x800")

    mostrarCadena = Label(ventana,text="Cadena inicial: " + "".join(cinta[:-1]),font=("Arial", 24))
    mostrarCadena.pack(ipady=20)

    canvas = Canvas(ventana, width=1600, height=632)
    canvas.pack()
    canvas.update_idletasks()
    
    return ventana,canvas

def dibujar_cinta(canvas, cinta, puntero, ventana):
    canvas.delete("all")
    ancho_celda = 120
    alto_celda = 120

    centroX = canvas.winfo_width() / 2
    x_inicial = centroX - (len(cinta) * ancho_celda) / 2
    centroY = canvas.winfo_height() / 2

    for idx, simbolo in enumerate(cinta):
        color = "red" if idx == puntero else "green"
        x = x_inicial + idx * ancho_celda
        canvas.create_rectangle(x, centroY - alto_celda / 2, x + ancho_celda, centroY + alto_celda / 2, fill=color)
        canvas.create_text(x + ancho_celda / 2, centroY, text=simbolo, fill="white",font=("Arial", 24))

    ventana.update()
    time.sleep(1.2)

def mostrar_mensaje(mensaje, ventana):
    print(mensaje)
    mostrarMensaje = Label(ventana,text=mensaje,font=("Arial", 24))
    mostrarMensaje.pack(ipady=20)

def procesar_maquina(cinta, ventana, canvas, archivo_log, animar=True):
    estado = "q0"
    puntero = 0

    transiciones = {
        "q0": {"0": ("q1", "X", 1), "Y": ("q3", "Y", 1)},
        "q1": {"0": ("q1", "0", 1), "1": ("q2", "Y", -1), "Y": ("q1", "Y", 1)},
        "q2": {"0": ("q2", "0", -1), "X": ("q0", "X", 1), "Y": ("q2", "Y", -1)},
        "q3": {"Y": ("q3", "Y", 1), "B": ("q4", "B", 1)},
    }

    try:
        while estado != "q4":
            if animar and ventana is not None:
                dibujar_cinta(canvas, cinta, puntero, ventana)

            actual = cinta[puntero]

            #Obtener transición
            if estado in transiciones and actual in transiciones[estado]:
                nuevo_estado, nuevo_simbolo, movimiento = transiciones[estado][actual]

                direccion = "R" if movimiento == 1 else "L"
                archivo_log.write(f"({estado},{actual})->({nuevo_estado},{nuevo_simbolo},{direccion})\n")

                cinta[puntero] = nuevo_simbolo
                estado = nuevo_estado
                puntero += movimiento
            else:
                mensaje = f"Cadena rechazada en el estado {estado} con símbolo '{actual}'"
                if animar:
                    mostrar_mensaje(mensaje, ventana)
                else:
                    print(mensaje)
                return

            #Extender cinta si es necesario
            if puntero >= len(cinta):
                cinta.append("B")
            elif puntero < 0:
                cinta.insert(0, "B")
                puntero = 0

        #Si se llega a q4
        if animar:
            mostrar_mensaje("Cadena aceptada", ventana)
        else:
            print("Cadena aceptada")

    except Exception as e:
        if animar:
            mostrar_mensaje(f"Error en la ejecución: {str(e)}", ventana)
        else:
            print(f"Error en la ejecución: {str(e)}")

def main():
    while True:
        cinta = obtener_cadena()
        longitud = len(cinta) - 1 #Para que el símbolo 'B' no afecte

        try:
            with open("registro_transiciones.txt", "w") as archivo_log:
                if longitud > LIMITE_ANIMACION:
                    print(f"La cadena tiene {longitud} símbolos. Animación omitida.")
                    procesar_maquina(cinta, None, None, archivo_log, animar=False)
                else:
                    ventana, canvas = configurar_interfaz(cinta)
                    procesar_maquina(cinta, ventana, canvas, archivo_log, animar=True)
                    ventana.mainloop()
        except Exception as e:
            print(f"Error inesperado: {str(e)}")

        repetir = input("¿Desea probar otra cadena? (s/n): ").strip().lower()
        if repetir != "s":
            break

if __name__ == "__main__":
    main()
