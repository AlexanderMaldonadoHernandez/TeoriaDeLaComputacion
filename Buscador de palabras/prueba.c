#include <stdio.h>

// Uso de struct, int, float, return, if, else, for, typedef, void, const

typedef struct {
    int id;
    float promedio;
    const char* nombre;
} Alumno;

void imprimirAlumno(const Alumno* a) {
    printf("ID: %d\n", a->id);
    printf("Nombre: %s\n", a->nombre);
    printf("Promedio: %.2f\n", a->promedio);
}

int main() {
    Alumno grupo[] = {
        {1, 8.5, "Ana"},
        {2, 9.2, "Luis"},
        {3, 7.8, "Marta"}
    };

    int total = sizeof(grupo) / sizeof(Alumno);  // sizeof
    float suma = 0;

    for (int i = 0; i < total; ++i) {  // for, int
        imprimirAlumno(&grupo[i]);
        suma += grupo[i].promedio;
    }

    float promedioGrupo = suma / total;

    if (promedioGrupo > 8.0) {  // if
        printf("Grupo destacado\n");
    } else {  // else
        printf("Grupo promedio\n");
    }

    return 0;  // return
}
