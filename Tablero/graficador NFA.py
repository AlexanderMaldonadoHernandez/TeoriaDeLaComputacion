import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Diccionario de transiciones del AFND
transiciones = {
    'q0': {'r': {'q1','q4'}, 'b': {'q5'}},
    'q1': {'r': {'q4','q6'}, 'b': {'q0','q2','q5'}},
    'q2': {'r': {'q1','q3','q6'}, 'b': {'q5','q7'}},
    'q3': {'r': {'q6'}, 'b': {'q2','q7'}},
    'q4': {'r': {'q1','q9'}, 'b': {'q0','q5','q8'}},
    'q5': {'r': {'q1','q4','q6','q9'}, 'b': {'q0','q2','q8','q10'}},
    'q6': {'r': {'q1','q3','q9','q11'}, 'b': {'q2','q5','q7','q10'}},
    'q7': {'r': {'q3','q6','q11'}, 'b': {'q2','q10'}},
    'q8': {'r': {'q4','q9','q12'}, 'b': {'q5','q13'}},
    'q9': {'r': {'q4','q6','q12','q14'}, 'b': {'q5','q8','q10','q13'}},
    'q10': {'r': {'q6','q9','q11','q14'}, 'b': {'q5','q7','q13','q15'}},
    'q11': {'r': {'q6','q14'}, 'b': {'q7','q10','q15'}},
    'q12': {'r': {'q9'}, 'b': {'q8','q13'}},
    'q13': {'r': {'q9','q12','q14'}, 'b': {'q8','q10'}},
    'q14': {'r': {'q9','q11'}, 'b': {'q10','q13','q15'}},
    'q15': {'r': {'q11','q14'}, 'b': {'q10'}}
}

# Crear grafo dirigido
grafo = nx.MultiDiGraph()

# Colores por tipo de transición
color_map = {'r': 'blue', 'b': 'green'}

# Agregar nodos y transiciones
for estado, trans in transiciones.items():
    for simbolo, destinos in trans.items():
        for destino in destinos:
            grafo.add_edge(estado, destino, label=simbolo, color=color_map[simbolo])

# Posición de nodos
pos = nx.spring_layout(grafo, seed=42)

# Dibujar nodos
plt.figure(figsize=(16, 12))
nx.draw_networkx_nodes(grafo, pos, node_color='lightblue', node_size=600, edgecolors='black')

# Dibujar aristas con colores según símbolo
for simbolo in ['r', 'b']:
    edges = [(u, v) for u, v, d in grafo.edges(data=True) if d['label'] == simbolo]
    nx.draw_networkx_edges(grafo, pos, edgelist=edges, edge_color=color_map[simbolo], arrowstyle='-|>', arrowsize=20, connectionstyle='arc3,rad=0.2', width=2)

# Etiquetas de nodos
nx.draw_networkx_labels(grafo, pos, font_size=10, font_weight='bold')

# Leyenda de colores
legend_elements = [
    Line2D([0], [0], color='blue', lw=2, label="r"),
    Line2D([0], [0], color='green', lw=2, label="b")
]
plt.legend(handles=legend_elements, title="Símbolos de transición", loc="upper left", fontsize = 12, title_fontsize = 14)

# Mostrar título
plt.title("AFND", fontsize=16)
plt.axis('off')
plt.tight_layout()
plt.show()
