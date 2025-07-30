import vaex
import matplotlib.pyplot as plt
import numpy as np

def txt_a_hdf5():
    df = vaex.from_csv('datos.txt', sep=',', convert='datos.hdf5') 

def graficar_datos():
    df = vaex.open("datos.hdf5")

    #Grafica normal
    plt.figure()
    plt.title("Distribución de unos")
    df.viz.scatter(x='tamano', y='unos', length_check=False, xlabel='Tamaño del archivo(MB)', ylabel='Cantidad de unos')
    plt.savefig("grafica_1", dpi=300, bbox_inches='tight')
    
    #Grafica con logaritmo
    plt.figure()
    plt.title("Distribución de unos")
    df.viz.scatter(x='tamano', y='log_unos', length_check=False, xlabel='Tamaño del archivo(MB)', ylabel='Cantidad de unos')
    plt.savefig("graficaLog_1", dpi=300, bbox_inches='tight')    

def main():
    txt_a_hdf5()
    graficar_datos()

if __name__ == "__main__":
    main()