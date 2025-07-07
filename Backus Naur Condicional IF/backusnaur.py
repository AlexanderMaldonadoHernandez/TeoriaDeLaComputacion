import random as rd

""" Gramática:
    S -> iCtSA
    A -> ;eS | ε """

MAX_DERIVACIONES = 10000

def limpiar_archivos():
    open("derivaciones.txt","w").close()
    open("codigo.txt","w").close()

def derivar_S(cadena):
    posicionesS = [i for i,c in enumerate(cadena) if c == 'S']
    pos = rd.choice(posicionesS)
    nuevaCadena = cadena[:pos] + "(iCtSA)" + cadena[pos+1:] if cadena != 'S' else "iCtSA"
    cadenaImpresa = nuevaCadena.replace('(','').replace(')','')

    with open("derivaciones.txt","a") as d:
        if cadena == 'S':
            d.write("S\n\n")
        d.write("Regla: S -> iCtSA\n")
        d.write(f"{cadenaImpresa}\n\n")

    return nuevaCadena

def derivar_A(cadena):
    posicionesA = [i for i,c in enumerate(cadena) if c == 'A']
    pos = rd.choice(posicionesA)
    decision = rd.choice([';eS',''])
    nuevaCadena = cadena[:pos] + decision + cadena[pos+1:]
    cadenaImpresa =  nuevaCadena.replace('(','').replace(')','')

    with open("derivaciones.txt","a") as d:
        d.write("Regla: A -> " + ("ε" if decision == '' else decision) + "\n")
        d.write(f"{cadenaImpresa}\n\n")

    return nuevaCadena

def eliminar_A(cadena):
    posicionesA = [i for i,c in enumerate(cadena) if c == 'A']
    pos = posicionesA[0]
    nuevaCadena = cadena[:pos] + cadena[pos+1:]
    cadenaImpresa =  nuevaCadena.replace('(','').replace(')','')

    with open("derivaciones.txt","a") as d:
        d.write("Regla: A -> ε\n")
        d.write(f"{cadenaImpresa}\n\n")
    
    return nuevaCadena

def generar_cadena(ifs_deseados):
    cadena = 'S'
    derivaciones = 0

    #Genera la cantidad de IFs deseada
    while ifs_deseados > 0 and derivaciones < MAX_DERIVACIONES:
        regla = rd.choice(['S','A'])

        if regla == 'A' and 'A' in cadena:
            cadena = derivar_A(cadena)
            derivaciones += 1
        else:
            cadena = derivar_S(cadena)
            ifs_deseados -= 1
            derivaciones += 1
    
    #La función para si se alcanza la cantidad de derivaciones máxima
    if derivaciones >= MAX_DERIVACIONES and ifs_deseados > 0:
        print("Se ha alcanzado la cantidad máxima de derivaciones sin lograr generar la cantidad de IFs deseados. Intente con un valor menor.")
        return None
    
    #Elimina las A restantes de la cadena
    while 'A' in cadena and derivaciones < MAX_DERIVACIONES:
        cadena = eliminar_A(cadena)
        derivaciones += 1

    #La cadena no es valida si se alcanza el máximo de derivaciones y sigue habiendo As en la cadena
    if derivaciones >= MAX_DERIVACIONES and 'A' in cadena:
        print("Se ha alcanzado la cantidad máxima de derivaciones. Intente con un valor menor.")
        return None

    cadenaImpresa =  cadena.replace('(','').replace(')','')
    print(f"Se ha generado la siguiente cadena: {cadenaImpresa}\nLas derivaciones han sido guardadas en 'derivaciones.txt'.")
    return cadena

def extraer_subcadena(subcadena):
        anidamiento = 1
        i = 1
        contenido = ""

        while i < len(subcadena) and anidamiento > 0:
            if subcadena[i] == '(':
                anidamiento += 1
            elif subcadena[i] == ')':
                anidamiento -= 1
            if anidamiento > 0:
                contenido += subcadena[i]
            i += 1
        return contenido, i  #Contenido interno y caracteres consumidos

def procesar_cadena(cadena, anidamiento=0):
    i = 0
    codigo = ""

    while i < len(cadena):
        #Encuentra una subcadena "iCt"
        if cadena[i] == 'i' and i+2 < len(cadena) and cadena[i+1] == 'C' and cadena[i+2] == 't':
            codigo += "    " * anidamiento + "if (condition) {\n"
            i += 3

            #Si se tiene un paréntesis, se procesa la subcadena entre paréntesis
            if i < len(cadena) and cadena[i] == '(':
                subcadena, salto = extraer_subcadena(cadena[i:])
                codigo += procesar_cadena(subcadena,anidamiento+1)
                i += salto
            elif i < len(cadena) and cadena[i] == 'S':
                codigo += "    " * (anidamiento+1) + "statement;\n"
                i += 1
            codigo += "    " * anidamiento + "}\n"

        #Encuentra una subcadena ";e"
        elif cadena[i] == ';' and i+1 < len(cadena) and cadena[i+1] == 'e':
            codigo += "    " * anidamiento + "else {\n"
            i += 2

            if i < len(cadena) and cadena[i] == '(':
                subcadena, salto = extraer_subcadena(cadena[i:])
                codigo += procesar_cadena(subcadena,anidamiento+1)
                i += salto
            elif i < len(cadena) and cadena[i] == 'S':
                codigo += "    " * (anidamiento+1) + "statement;\n"
                i += 1
            codigo += "    " * anidamiento + "}\n"

        #Encuentra una subcadena "S"
        elif cadena[i] == 'S':
            codigo += "    " * anidamiento + "statement;\n"
            i += 1

        else:
            i += 1

    return codigo

def generar_codigo(cadena):
    codigo_procesado = procesar_cadena(cadena)

    with open("codigo.txt","w") as c:
        c.write(codigo_procesado)

    print("El código ha sido generado exitosamente y ha sido guardado en 'codigo.txt'.\n") 

def main():
    #Menu inicial
    while True:
        entrada = input("1.Modo manual\n2.Modo automático\n3.Salir\n").strip()

        if entrada == '1':
            while True:
                try:
                    cantidad = int(input("\nIntroduzca la cantidad de IFs ha ser generados por el programa:\n"))
                    if cantidad > 0:
                        limpiar_archivos()
                        cadena = generar_cadena(cantidad)
                        if cadena == None:
                            continue
                        else:
                            generar_codigo(cadena)
                            break
                    else:
                        print("Por favor ingrese un número positivo.")
                        continue
                except ValueError:
                    print("Entrada invalida. Introduzca un número entero.\n")
                    continue
        elif entrada == '2':
            while True:
                limpiar_archivos()
                cantidad = rd.randint(1,1000)
                print(f"Se generara una cadena con {cantidad} IFs.")
                cadena = generar_cadena(cantidad)
                if cadena == None:
                    continue
                else:
                    generar_codigo(cadena)
                    break

        elif entrada == '3':
            break

        else:
            print("Entrada inválida. Elija una opción: 1, 2 o 3.\n")
            continue

if __name__ == "__main__":
    main()