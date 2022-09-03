#ifndef CARGA_LEMARIO_H
#define CARGA_LEMARIO_H

#define AUMENTO 100

#include<stdio.h>                              // Lectura de archivos
#include<assert.h>                             // Testeos
#include<stdlib.h>                             // Generar números aleatorios, errores
#include<string.h>                             // Compiar un string (strcpy)
#include<time.h>                               // Seed para generar número aleatorio

typedef struct 
{
    char** arraypalabras;                      // Puntero para guardar las palabras en memoria
    int cantidadPalabras;                      // Contador de las palabras guardadas
    
} VecPalabras;



/*
 *
 *
 * 
 * 
 */


/*
 *cargaPalabras: String int -> *VecPalabras
 *Recibe la ruta de una archivo y la cantidad de memoria que se agrega al vector de
 *palabras cuando este se queda sin la misma.
 *Devuelve una dirección de memoria que apunta a una estructura VecPalabras
 */

VecPalabras *cargaPalabras(char *nombreArchivo,int aumentoPalabras);