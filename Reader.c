#include<stdio.h>
#include<assert.h>
#include<stdlib.h>
#include<string.h>
#include<time.h>

typedef struct
{
    char** arraypalabras;
    int cantidadPalabras;
    
} VecPalabras;

typedef struct 
{
    int dimension;
    int cantidadPalabras;
    int complejidad;
} Datos;



VecPalabras *cargaPalabras(char *nombreArchivo,int aumentoPalabras)
{
    FILE* archivo;
    archivo = fopen(nombreArchivo, "r");
    VecPalabras *VPalabras ;
    VPalabras = malloc(sizeof(VecPalabras));
    char **palabras;
    int contadorPalabras = 0;
    int espacioParaPalabras = 0;
    char buff[255];

    while (fgets(buff, 255, archivo))
    {
        if (contadorPalabras == espacioParaPalabras)
        { 
            espacioParaPalabras += aumentoPalabras;
            char **masPalabras = realloc(palabras, sizeof(char *) * (espacioParaPalabras));
            if (masPalabras == NULL)
            {
                fprintf(stderr, "Fallo en la reasignaciddon de memoria.\n");
                exit(1);
            }
            palabras = masPalabras;
        }
        char *palabra = malloc(sizeof(char) * (strlen(buff) + 1));
        if (palabra == NULL)
        {
            fprintf(stderr,"Fallo en la asignacion de memoria.\n");
            exit(1);
        }
        strcpy(palabra,buff);
        palabras[contadorPalabras] = palabra;
        contadorPalabras++;
    }
    fclose(archivo);
    VPalabras->arraypalabras = palabras;
    VPalabras->cantidadPalabras = contadorPalabras;
    return VPalabras;
}

int perteneceNum(long *arrnum, int num, long cota)
{
    int salida = 0;
    for (int i = 0; i < cota; i++)
    {
        if (arrnum[i] == num)
        {
            salida = 1;
        }
    }
    return salida;
}

long *numerosRandom(int cantPalabras,long rangPalabras)
{
    srand(time(NULL));
    long *arregloLong = malloc(sizeof(long) * cantPalabras);

    for (long i = 0; i < cantPalabras; i++)
    {
        long random = rand() % rangPalabras;
        while (perteneceNum(arregloLong, random, i))
        {
            random = rand() % rangPalabras;
        }
        arregloLong[i] = random;
    }
    return arregloLong;
}

int pedirCantidadDePalabras() {
    int cantidadPalabras;

    printf("Ingrese la cantidad de palabras para la sopa de letras: ");
    scanf("%d", &cantidadPalabras);
    while (cantidadPalabras > 0){
        printf("Ingrese un numero positivo: ");
        scanf("%d", &cantidadPalabras);
    }
    return cantidadPalabras;
}

int pedirDimension() {
    int dimension;

    printf("Ingrese la dimension de la sopa de letras: ");
    scanf("%d", &dimension);
    while (dimension > 0){
        printf("Ingrese un numero positivo: ");
        scanf("%d", &dimension);
    }
    return dimension;
}

int pedirComplejidad() {
    int complejidad;

    printf("Ingrese la complejidad de la sopa de letras: ");
    scanf("%d", &complejidad);
    while (0 <= complejidad <= 3){
        printf("Facil = 0, Medio = 1, Dificil = 2, Muy dificil = 3: ");
        scanf("%d", &complejidad);
    }
    return complejidad;
}




int main(int argc, char *argv[]) {
    int N, Dim, Comp;
    N = pedirCantidadDePalabras();
    Dim = pedirDimension();
    Comp = pedirComplejidad();

    VecPalabras *vecpalabras;
    vecpalabras = cargaPalabras(argv[1],100);

    int cantidadPalabras = vecpalabras->cantidadPalabras;
    char  **arrayPalabras = vecpalabras->arraypalabras;
    free(vecpalabras);

    long *numeros;
    numeros = numerosRandom(N,cantidadPalabras);

    FILE* salida;
    salida = fopen("salida.txt", "w+");

    fprintf(salida, "DIMENSION\n");
    fprintf(salida, "%d\n", Dim);
    fprintf(salida, "PALABRAS\n");
    for (int i = 0; i < N; i++)
    {
        fprintf(salida, "%s",arrayPalabras[numeros[i]]);
        //printf("%s",arrayPalabras[numeros[i]]);
    }
    fprintf(salida,"COMPLEJIDAD\n");
    fprintf(salida,"%d\n",Comp);
    fclose(salida);
    return 0;
}