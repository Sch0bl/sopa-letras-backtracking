#include "cargaLemario.h"

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