# Prácticas de Teoría de la Computación - ESCOM IPN - Genaro Juárez Martínez 

Este repositorio contiene cinco prácticas desarrolladas en el contexto de la teoría de autómatas y lenguajes formales.  
Cada práctica incluye su respectiva implementación, reporte de práctica y, en algunos casos, visualizaciones gráficas.

---

## Práctica 1 - Universo de Cadenas Binarias
Genera el universo de cadenas binarias Σⁿ para un valor entre 0 y 1000, definido por el usuario o automáticamente.  
El programa permite ejecución manual o automática, guarda el resultado en un archivo de texto y grafica la cantidad de unos y ceros por cadena.  
El reporte incluye visualizaciones con escala normal y logarítmica para n = 29.

---

## Práctica 2 - Tablero de Juego 4x4
Simulación de movimientos ortogonales y diagonales en un tablero de ajedrez 4x4 con dos jugadores, cada uno con posiciones iniciales y finales definidas.  
El programa puede ejecutarse en modo automático o manual, generar rutas y rutas ganadoras, graficar el tablero y mostrar la red NFA de los posibles estados y transiciones.  
Soporta entre **3 y 100 movimientos** por partida.

---

## Práctica 3 - Buscador de Palabras Reservadas en C
Implementa un autómata que detecta palabras reservadas del lenguaje C.  
Incluye el diseño del NFA y su conversión a DFA paso a paso.  
El programa analiza archivos fuente, cuenta las palabras reservadas encontradas, indica su posición (x, y) y registra el historial de cambios de estado.  
Se incluye una visualización gráfica del DFA en ejecución.

---

## Práctica 4 - Derivación de Condicional IF con Backus-Naur
Programa que deriva la gramática Backus-Naur para estructuras `if` usando las reglas:  
`S → iCtSA`  
`A → ;eS | ε`  
Genera derivaciones aleatorias hasta un número de `if`s especificado por el usuario o automáticamente (máximo 10,000).  
Guarda cada paso de derivación en un archivo, junto con el pseudocódigo resultante.

---

## Práctica 5 - Máquina de Turing para {0ⁿ1ⁿ}
Implementación de una máquina de Turing que reconoce el lenguaje:
`{0^n1^n | n >= 1}`  
Basada en el ejercicio 8.2 del libro de John Hopcroft.  
El programa acepta cadenas de hasta 1000 caracteres y registra las descripciones instantáneas paso a paso en un archivo de texto.  
Para cadenas de longitud ≤ 10, muestra una animación visual de la computación.

---

### Contenido del Repositorio
- Código fuente de cada práctica.
- Archivos de salida generados por los programas.
- Visualizaciones gráficas y animaciones (cuando corresponda).
- Documentación en **LaTeX** con explicación de cada implementación.





