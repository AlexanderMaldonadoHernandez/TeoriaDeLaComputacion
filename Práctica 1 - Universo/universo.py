import random
import os
import math

def generar_universo(n):
    #datos.txt sera el archivo con el que graficaremos los datos
    with open("universo.txt", "w") as f, open("datos.txt","w") as d:

        tamano_f = 0
        unos = 0
        d.write("tamano,unos,log_unos\n")

        for i in range(n + 1):
            f.write(f"Σ^{i} = {{")
            for numero in range(2 ** i):
                cadena = bin(numero)[2:].zfill(i) if i > 0 else "ε"  #Cadena vacía para Σ^0
                
                if numero < (2 ** i) - 1:
                    f.write(f"{cadena}" + ",")
                else:
                    f.write(f"{cadena}")

                f.flush()
                tamano_f = os.path.getsize("universo.txt") / (1024 ** 2)
                
                unos = cadena.count("1")
                log_unos = math.log(unos) if unos > 0 else unos
                d.write(f"{tamano_f:.2f},{unos},{log_unos}\n")
                
            f.write("}\n")
            print(f"Σ^{i} completado ({2**i} cadenas generadas)")  #Mostrar progreso

def main():
    while True:
        entrada = input("Introduce un valor para n (0-1000) o presiona Enter para elegir aleatoriamente: ")

        if entrada == "":
            n = random.randint(0, 10)
            print(f"Se ha elegido aleatoriamente n = {n}")
        else:
            try:
                n = int(entrada)
                if not (0 <= n <= 1000):
                    print("Por favor, introduce un número entre 0 y 1000.")
                    continue
            except ValueError:
                print("Entrada inválida. Introduce un número entero.")
                continue

        print(f"Generando Σ* hasta n = {n}...")
        generar_universo(n)
        print(f"Resultados guardados en 'universo.txt'.")

        while True:
            repetir = input("¿Quieres calcular otro valor de n? (s/n): ").strip().lower()
            if repetir in ["s","n"]:
                break
            else:
                print("Entrada inválida. Seleccione \"s\" o \"n\".")

        if repetir == "n":
            break

if __name__ == "__main__":
    main()
