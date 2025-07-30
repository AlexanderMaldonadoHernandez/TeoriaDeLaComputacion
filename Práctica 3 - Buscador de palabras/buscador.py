import csv
import networkx as nx
import matplotlib.pyplot as plt

def graficar_automata(alfabeto, transiciones, estado_inicial, estados_finales):
    G = nx.MultiDiGraph()

    #Agregar estados
    for estado in transiciones:
        G.add_node(estado)

    #Agregar transiciones
    for origen, caminos in transiciones.items():
        for simbolo in alfabeto:
            if simbolo in caminos:
                destino = caminos[simbolo]
                G.add_edge(origen, destino, label=simbolo)

    pos = nx.spring_layout(G, k=3, iterations=100)
    plt.figure(figsize=(18, 13.5))

    #Dibujar estados
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=700)

    #Estado inicial en verde
    nx.draw_networkx_nodes(G, pos, nodelist=[estado_inicial], node_color='lightgreen', node_size=900)

    #Estados finales en naranja
    nx.draw_networkx_nodes(G, pos, nodelist=estados_finales, node_color='orange', node_size=700)

    #Etiquetas estados
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

    #Dibujar aristas con curvas para mejor visibilidad
    nx.draw_networkx_edges(G, pos, arrows=True, connectionstyle='arc3,rad=0.2',alpha=0.5)

    # Etiquetas aristas
    etiquetas = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=etiquetas,
        font_color='black',
        font_size=7,
        bbox=dict(facecolor='white',edgecolor='none',boxstyle='round,pad=0.1')
        #bbox=dict(facecolor='none', edgecolor='none', pad=0)
    )

    plt.axis('off')
    plt.tight_layout()
    plt.savefig("DFA.png", dpi=300, bbox_inches='tight')  # Guardar PNG con buena calidad
    plt.show()

def formatear_subconjunto(subconjunto,est_ini,est_fin,es_estadoNFA=False):
    subconjunto_ordenado = sorted(subconjunto,key=lambda x: int(x[1:]))
    cadena = "{" + ",".join(subconjunto_ordenado) + "}"
    
    if es_estadoNFA == True and len(subconjunto) == 1 and subconjunto[0] == est_ini: #Marca el estado inicial en la tabla
        return f"->{cadena}"
    elif es_estadoNFA == True and any(estado in est_fin for estado in subconjunto):  #Marca subconjuntos con estados finales
        return f"*{cadena}"
    else:
        return cadena

def generar_tabla(alfabeto,NFA,est_ini,est_fin):
    encabezado = ['Estados NFA','Estado DFA'] + alfabeto
    
    with open("tabla.csv","w",newline='') as t:
        escritor = csv.writer(t,delimiter=';')
        escritor.writerow(encabezado)

        checados = set()            #Estados ya procesados
        pendientes = [[est_ini]]    #Subconjuntos por procesar
        fila = []                   #Texto a escribir en la fila
        contadorDFA = 0             #Mapeo de subconjunto NFA -> estado NFA
        
        while pendientes:
            subconjunto = pendientes.pop()
            fila = []

            if tuple(subconjunto) in checados:
                continue
            fila.append(formatear_subconjunto(subconjunto,est_ini,est_fin,True))
            checados.add(tuple(subconjunto))

            fila.append(f"q{contadorDFA}")
            contadorDFA += 1

            for simbolo in alfabeto:
                estados_siguientes = set()

                for estado in subconjunto:
                    if simbolo in NFA[estado]:
                        estados_siguientes.update(NFA[estado][simbolo])
                
                fila.append(formatear_subconjunto(estados_siguientes,est_ini,est_fin))
                estados_ordenados = tuple(sorted(estados_siguientes,key=lambda x: int(x[1:])))

                if estados_ordenados not in checados and estados_ordenados not in map(tuple,pendientes):
                    pendientes.append(list(estados_ordenados))

            escritor.writerow(fila)

def tabla_a_dfa():
    DFA = {}
    mapeoDFA = {} #Relaciona los subconjuntos del NFA con estados del DFA
    
    with open("tabla.csv",newline='') as t:
        lector = csv.reader(t,delimiter=';')
        encabezado = next(lector)
        alfabeto = encabezado[2:]
        filas = list(lector)

    inicial = ''
    finales = set()

    #Construcción de diccionario subconjunto NFA -> estado DFA
    for fila in filas:
        subconjuntoNFA = fila[0]
        estadoDFA = fila[1]
        if '->' in subconjuntoNFA:
            mapeoDFA[subconjuntoNFA[2:]] = estadoDFA
            inicial = mapeoDFA[subconjuntoNFA[2:]]
        elif '*' in subconjuntoNFA:
            mapeoDFA[subconjuntoNFA[1:]] = estadoDFA
            finales.add(mapeoDFA[subconjuntoNFA[1:]])
        else:
            mapeoDFA[subconjuntoNFA] = estadoDFA

    #Transiciones
    for fila in filas:
        estadoDFA = fila[1]
        DFA[estadoDFA] = {}
        for i,simbolo in enumerate(alfabeto):
            subconjunto = fila[i+2]
            estado = mapeoDFA[subconjunto]
            DFA[estadoDFA][simbolo] = estado
        
    return DFA,inicial,finales

def validar_palabra(palabra):
    validas = [
    "auto", "else", "long", "switch",
    "break", "enum", "register", "typedef",
    "case", "extern", "return", "union",
    "char", "float", "short", "unsigned",
    "const", "for", "signed", "void",
    "continue", "goto", "sizeof", "volatile",
    "default", "if", "static", "while",
    "do", "int", "struct", "_Packed",
    "double"]

    for palabraValida in validas:
        if palabraValida in palabra:
            ajustarPos = len(palabra) - len(palabraValida)
            return palabraValida,ajustarPos
        
    return palabra,len(palabra)

def analizar_texto(archivo, DFA, est_ini, est_fin, alfabeto):
    resultados = {}
    
    try:
        with open(archivo, "r") as a, open("evaluacion.txt", "w") as e:
            y = 0  #Número de línea

            for linea in a:
                y += 1
                linea = linea.rstrip('\n')
                longitud = len(linea)
                x = 0 #Número de columna
                estado_actual = est_ini
                palabra = ""
                inicio_palabra = 0

                while x < longitud:
                    simbolo = linea[x]

                    if simbolo not in alfabeto:
                        e.write(f"Símbolo: '{simbolo}'\n")
                        e.write(f"{estado_actual} -> {est_ini}\n\n")
                        estado_actual = est_ini
                        palabra = ""
                        x += 1
                        continue

                    if simbolo not in DFA[estado_actual]:
                        e.write(f"Símbolo: '{simbolo}'\n")
                        e.write(f"{estado_actual} -> {est_ini}\n\n")
                        estado_actual = est_ini
                        palabra = ""
                        x += 1
                        continue

                    if not palabra:
                        inicio_palabra = x

                    estado_siguiente = DFA[estado_actual][simbolo]
                    e.write(f"Símbolo: '{simbolo}'\n{estado_actual} -> {estado_siguiente}\n\n")
                    palabra += simbolo
                    estado_actual = estado_siguiente

                    if estado_actual in est_fin:
                        palabra,ajustarPos = validar_palabra(palabra)
                        e.write(f"Palabra aceptada: '{palabra}' en línea {y},columna {inicio_palabra+ajustarPos+1}\n\n")
                        if palabra not in resultados:
                            resultados[palabra] = [0, []]
                        resultados[palabra][0] += 1
                        resultados[palabra][1].append((inicio_palabra+ajustarPos+1, y))
                        palabra = ""
                    x += 1
                
        with open("resultados.txt","w") as r:
            r.write("===== RESUMEN DE PALABRAS ACEPTADAS =====\n")
            r.write("Nota: Las posiciones se expresan en coordenadas (x,y) donde 'x' es el número de columna y 'y' el número de fila\n\n")
            for palabra, (conteo, posiciones) in resultados.items():
                posiciones = ", ".join(f"({x},{y})" for x, y in posiciones)
                r.write(f"Palabra: '{palabra}' | Apariciones: {conteo} | Posiciones: {posiciones}\n")
        
        print("Archivo analizado correctamente.")
        print("Las evaluaciones del DFA han sido guardadas en 'evaluacion.txt'.")
        print("Las palabras reservadas detectadas han sido guardadas en 'resultados.txt'.")

    except FileNotFoundError:
        print("El archivo no existe.")
        exit()

def main():
    #Definición del automata
    alfabeto = ['_','P','a','b','c','d','e','f','g','h','i','k','l','m','n','o','p','r','s','t','u','v','w','x','y','z']
    NFA = {
        'q0' : {'_' : {'q0','q142'},
                'P' : {'q0'},
                'a' : {'q0','q1'},
                'b' : {'q0','q5'},
                'c' : {'q0','q10'},
                'd' : {'q0','q21'},
                'e' : {'q0','q38'},
                'f' : {'q0','q50'},
                'g' : {'q0','q57'},
                'h' : {'q0'},
                'i' : {'q0','q61'},
                'k' : {'q0'},
                'l' : {'q0','q65'},
                'm' : {'q0'},
                'n' : {'q0'},
                'o' : {'q0'},
                'p' : {'q0'},
                'r' : {'q0','q69'},
                's' : {'q0','q81'},
                't' : {'q0','q109'},
                'u' : {'q0','q116'},
                'v' : {'q0','q127'},
                'w' : {'q0','q137'},
                'x' : {'q0'},
                'y' : {'q0'},
                'z' : {'q0'},},
        'q1' : {'u' : {'q2'}},
        'q2' : {'t' : {'q3'}},
        'q3' : {'o' : {'q4'}},
        'q4' : {},
        'q5' : {'r' : {'q6'}},
        'q6' : {'e' : {'q7'}},
        'q7' : {'a' : {'q8'}},
        'q8' : {'k' : {'q9'}},
        'q9' : {},
        'q10' : {'a' : {'q11'},
                 'h' : {'q14'},
                 'o' : {'q17'}},
        'q11' : {'s' : {'q12'}},
        'q12' : {'e' : {'q13'}},
        'q13' : {},
        'q14' : {'a' : {'q15'}},
        'q15' : {'r' : {'q16'}},
        'q16' : {},
        'q17' : {'n' : {'q18'}},
        'q18' : {'s' : {'q19'},
                 't' : {'q33'}},
        'q19' : {'t' : {'q20'}},
        'q20' : {},
        'q21' : {'e' : {'q22'},
                 'o' : {'q28'}},
        'q22' : {'f' : {'q23'}},
        'q23' : {'a' : {'q24'}},
        'q24' : {'u' : {'q25'}},
        'q25' : {'l' : {'q26'}},
        'q26' : {'t' : {'q27'}},
        'q27' : {},
        'q28' : {'u' : {'q29'}},
        'q29' : {'b' : {'q30'}},
        'q30' : {'l' : {'q31'}},
        'q31' : {'e' : {'q32'}},
        'q32' : {},
        'q33' : {'i' : {'q34'}},
        'q34' : {'n' : {'q35'}},
        'q35' : {'u' : {'q36'}},
        'q36' : {'e' : {'q37'}},
        'q37' : {},
        'q38' : {'l' : {'q39'},
                 'n' : {'q42'},
                 'x' : {'q45'}},
        'q39' : {'s' : {'q40'}},
        'q40' : {'e' : {'q41'}},
        'q41' : {},
        'q42' : {'u' : {'q43'}},
        'q43' : {'m' : {'q44'}},
        'q44' : {},
        'q45' : {'t' : {'q46'}},
        'q46' : {'e' : {'q47'}},
        'q47' : {'r' : {'q48'}},
        'q48' : {'n' : {'q49'}},
        'q49' : {},
        'q50' : {'l' : {'q51'},
                 'o' : {'q55'}},
        'q51' : {'o' : {'q52'}},
        'q52' : {'a' : {'q53'}},
        'q53' : {'t' : {'q54'}},
        'q54' : {},
        'q55' : {'r' : {'q56'}},
        'q56' : {},
        'q57' : {'o' : {'q58'}},
        'q58' : {'t' : {'q59'}},
        'q59' : {'o' : {'q60'}},
        'q60' : {},
        'q61' : {'f' : {'q62'},
                 'n' : {'q63'}},
        'q62' : {},
        'q63' : {'t' : {'q64'}},
        'q64' : {},
        'q65' : {'o' : {'q66'}},
        'q66' : {'n' : {'q67'}},
        'q67' : {'g' : {'q68'}},
        'q68' : {},
        'q69' : {'e' : {'q70'}},
        'q70' : {'g' : {'q71'},
                 't' : {'q77'}},
        'q71' : {'i' : {'q72'}},
        'q72' : {'s' : {'q73'}},
        'q73' : {'t' : {'q74'}},
        'q74' : {'e' : {'q75'}},
        'q75' : {'r' : {'q76'}},
        'q76' : {},
        'q77' : {'u' : {'q78'}},
        'q78' : {'r' : {'q79'}},
        'q79' : {'n' : {'q80'}},
        'q80' : {},
        'q81' : {'h' : {'q82'},
                 'i' : {'q86'},
                 't' : {'q95'},
                 'w' : {'q104'}},
        'q82' : {'o' : {'q83'}},
        'q83' : {'r' : {'q84'}},
        'q84' : {'t' : {'q85'}},
        'q85' : {},
        'q86' : {'g' : {'q87'},
                 'z' : {'q91'}},
        'q87' : {'n' : {'q88'}},
        'q88' : {'e' : {'q89'}},
        'q89' : {'d' : {'q90'}},
        'q90' : {},
        'q91' : {'e' : {'q92'}},
        'q92' : {'o' : {'q93'}},
        'q93' : {'f' : {'q94'}},
        'q94' : {},
        'q95' : {'a' : {'q96'},
                 'r' : {'q100'}},
        'q96' : {'t' : {'q97'}},
        'q97' : {'i' : {'q98'}},
        'q98' : {'c' : {'q99'}},
        'q99' : {},
        'q100' : {'u' : {'q101'}},
        'q101' : {'c' : {'q102'}},
        'q102' : {'t' : {'q103'}},
        'q103' : {},
        'q104' : {'i' : {'q105'}},
        'q105' : {'t' : {'q106'}},
        'q106' : {'c' : {'q107'}},
        'q107' : {'h' : {'q108'}},
        'q108' : {},
        'q109' : {'y' : {'q110'}},
        'q110' : {'p' : {'q111'}},
        'q111' : {'e' : {'q112'}},
        'q112' : {'d' : {'q113'}},
        'q113' : {'e' : {'q114'}},
        'q114' : {'f' : {'q115'}},
        'q115' : {},
        'q116' : {'n' : {'q117'}},
        'q117' : {'i' : {'q118'},
                  's' : {'q121'}},
        'q118' : {'o' : {'q119'}},
        'q119' : {'n' : {'q120'}},
        'q120' : {},
        'q121' : {'i' : {'q122'}},
        'q122' : {'g' : {'q123'}},
        'q123' : {'n' : {'q124'}},
        'q124' : {'e' : {'q125'}},
        'q125' : {'d' : {'q126'}},
        'q126' : {},
        'q127' : {'o' : {'q128'}},
        'q128' : {'i' : {'q129'},
                  'l' : {'q131'}},
        'q129' : {'d' : {'q130'}},
        'q130' : {},
        'q131' : {'a' : {'q132'}},
        'q132' : {'t' : {'q133'}},
        'q133' : {'i' : {'q134'}},
        'q134' : {'l' : {'q135'}},
        'q135' : {'e' : {'q136'}},
        'q136' : {},
        'q137' : {'h' : {'q138'}},
        'q138' : {'i' : {'q139'}},
        'q139' : {'l' : {'q140'}},
        'q140' : {'e' : {'q141'}},
        'q141' : {},
        'q142' : {'P' : {'q143'}},
        'q143' : {'a' : {'q144'}},
        'q144' : {'c' : {'q145'}},
        'q145' : {'k' : {'q146'}},
        'q146' : {'e' : {'q147'}},
        'q147' : {'d' : {'q148'}},
        'q148' : {},
    }
    inicial = 'q0'
    finales = {'q4','q9','q13','q16','q20','q37','q27','q32','q28','q41','q44','q49','q54','q56','q60','q62','q64','q68','q76','q80','q85','q90','q94','q99','q103','q108','q115','q120','q126','q130','q136','q141','q148'}
    
    generar_tabla(alfabeto,NFA,inicial,finales)
    DFA,inicialDFA,finalesDFA = tabla_a_dfa()
    archivo = input("Escriba el nombre del archivo de texto o código a ser analizado: ")

    analizar_texto(archivo,DFA,inicialDFA,finalesDFA,alfabeto)
    graficar_automata(alfabeto,DFA,inicialDFA,finalesDFA)
    

if __name__ == "__main__":
    main()