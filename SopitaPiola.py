from random import *
from sys import argv


"""
    IDEAS GENERALES
    La idea del programa es representar la sopa de letras como una matriz nxn, 
     cuyo dominio que llameremos Posiciones son los pares ordenado (x,y) pertenecientes 
     al conjunto [|0, n - 1|] x [|0, n - 1|], (ej. (4,5))
     Los x complen el rol de fila de la sopa de letra y los y el rol de columna.
     Y el  codomininio ({'a','b','c',...,'y','z'} x [|1, p]]) U {('-',0)} . 
     donde p es la cantidad de palabras contenidas el la sopa de letras (ej. ('a', 3)).
    El par (String, entero) indica una letra y en segundo plano la catidad de palabras
    que relacionadas con el elemento del dominio.
    El elemento ('-', 0) del codominio cumple el rol de "nulo", es decir, 
    no hay ninguna (letra,contador) asignada al elemento del dominio.
    Para esta representacion utilizaremo un diccionario Posiciones, donde cada clave del diccionario
     representa una tupla (x,y) y es mapeada con una tupla (letra,contador). Ej. {(0,0) : ('g', 1)}
    Una Palabra (String) es representada como vector dentro de la matriz, ya que esta tienen módulo
     (Longitud del String) dirección (pares ordenados alineados) y sentido
     ID y DI (palabras escritas de izquierda a derecha ('hola') y viceversa ('aloh')).
    La Longitud y el sentido estan dados por el String y la direccion está dada por un
     subconjuntos del domínio de la matriz que complen con las siguientes condiciones:
        Sea k la longitud de alguna palabra y (i,j) el orígen de su vector asociado
        - Dirección horizontal H = {(i,j),(i, j+1), ... , (i, j+(k-1))}, con  0 <= j+(k-1) <= n-1
        - Dirección vertical V = {(i,j),(i+1,j),...,(i+(k-1),j)}, con 0 <= i+(k-1) <= n-1
        - Dirección Diagonal de esquina sup. izq a Esquina inf der Dsi = {(i,j),(i+1,j+1),...,(i+(k-1),j+(k-1))},
          con con 0 <= i+(k-1) <= n-1 y 0 <= j+(k-1) <= n-1
        - Dirección Diagonal de esquina sup. der a Esquina inf izq Dsd = {(i,j),(i+1,j-1),...,(i+(k-1),j-(k-1))},
          con con 0 <= i+(k-1) <= n-1 y 0 <= j-(k-1) <= n-1
    La Complejidad de la sopa de letra nos ponen ciertas condiciones extras a los vectores:
        - Facil : Vectores de tipo H o V sentido ID tales que sus respectivas posiciones
                  sean disjuntas (no coparten posicion, por lo tanto, las palabras no se cruzan).
        - Medio : Vectores de tipo H, V o Dsi con sentid ID tales que sus respectivas posiciones sean disjuntas.
        - Dificil : Vectores de todo tipo, tales que sus respectivas posiciones sean disjuntas.
        - Muy dificil: Vectores de todo tipo, tales que sus respectivas posiciones sean disjuntas
                       o cada elemento de su intersección este mapeado a la misma letra
    Como no todo combinacion de vectores es válida, y la elección de un vector condiciona la elección de 
        otros vectores, llamaremos Candidatos al conjunto de vectores que
        cumplen con las condiciones dadas por el tipo de complejidad y los candidatos elegidos previeamente.
        La idea es elejir un cadidato por palabra y armar los candidatos para la proxima
        palabra en función de los candidatos ya elejidos. 
        Si al generar los candidatos para una palabra el resultado es el conjunto vacío,
        se vuelve la palabra anterior y se prueba con otro candidato.
        El proceso termina cuando se obtiene un candidato por palabra (se puede generar la sopa de letras)
        o cuando el conjunto de candidatos es vacío para todas las palabras, lo cual implica que no 
        es posible generar una sopa de letras con las palabras dadas y la complejidad.
    Para poder generar Candidatos en funcion de las palabras ya elegidas se utiliza el diccionario
    MatrizSopa para guardar información de los vectores ya elegidos y en paralelo
    un diccionario infoPalabras, que guarda información de los candidatos en cada una de las palabras.
    Una vez terminado el proceso de elección de Candidatos de forma satisfactoria, se completan las posiciones
    mapeadas al elemento nulo con una letra al azar de forma que no se 
        generen palabras repetidas y se obtiene una sopa de letras válidas para el enunciado.

    REPRESENTACIÓN DE DATOS

    Complejidad es un Int que representa la complejidad de la sopa de letras.

    Dimension es un Int que representa la dimensión de la sopa de letras.

    Palabra es un String que representa una palabra de la sopa de letras.

    Letra es un Char que representa una letra.

    Posicion es un una tupla (fila,columna) donde
        fila es un int que representa la fila de una casilla en la sopa de letras.
        columna es un int que representa la columna de una casilla en la sopa de letras.

    Posiciones es una Lista donde cada elemento de esta es de tipo Posición que representa la
        ubicación de una palabra en la sopa de letras,

    Candidato es una Lista donde cada elemento es una tupla (Posicion, Letra) que representa
        una ubicación válida de una palabra en la sopa de letras.

    Candidatos en una Lista donde cada elemento es de tipo Candidato 

    dicPalabra es un Diccionario {"Candidatos" : Candidatos,
                                  "Candidato"  : Candidato,
                                  "Longitud"   : Longitud,
                                  "Estado"     : Estado      } 
        Longitud es un Int que representa la longutud de la palabra.
        Estado es un Boolean que indica si los Candidatos deben ser generados.

    infoPalabras es un Diccionario {Palabra : dicPalabra, "Lista" : List(palabra)} donde
        Cada Palabra está asociada a su dicPalabras.
        El String "Lista" esta asociado con una Lista de Palabras, representa las palabras contenida como clave
        en el diccionario.
        
    dicMatrizSopa es un Diccionario {Posición : (Letra,Contador)} que representa la sopa de letras, donde
        Contador es un Int que representa la cantidad de palbras asociadas a la letra en la Posición.
"""
#validaPosicion: int tuple(int,int) -> Boolean
#Recibe la dimensión de la sopa de letras, una posición y devuelve True si
#los valores de la fila y columna están dentro del rango de la matriz.
#Caso contrario devuelve False.

def validaPosicion(n, Posicion):
    if 0 <= Posicion[0] < n:
        if 0 <= Posicion[1] < n:
            return True
        else:
            return False
    else:
        return False

#generaVectoresDiagonales: Int Int Int -> List(List(tuple(int,int)))
#Recibe la Dimension de la sopa de letras, la Longitud de una palabra y la complejidad
#de la sopa de letras. En caso de que la complejidad sea 1, devuelve una lista las diagonales (Posiciones)
#con dirección esquina superior izquierda a esquina inferior derecha..
#Caso contrario, agrega las diagonales con dirección esquina superior derecha a esquina inferior izquierda.
#La lista contiene diagonales con longitud mayor o igual a la longitud de la palabra correspondiente.

def generaDiagonales(n, Longitud, complejidad):
    listaPosiciones = []
    for i in range(-(n-1),n):
        Posiciones = [ (filacolumna + i , filacolumna) for filacolumna in range(n)]
        listaPosiciones.append([ Posicion for Posicion in Posiciones if validaPosicion(n, Posicion)])
    if complejidad != 1:
        for i in range(2*n - 1):
            Posiciones = [(filacolumna,-(filacolumna - i)) for filacolumna in range(n)]
            listaPosiciones.append([ Posicion for Posicion in Posiciones if validaPosicion(n, Posicion)])
    return [Posiciones for Posiciones in listaPosiciones if len(Posiciones) >= Longitud]

#generaFilas: int -> list(list(tuple(int,int)))
#Recibe la dimensión de la sopa de letras.
#Devuleve la lista de filas (Posiciones) de la sopa de letras.

def generaFilas(n):
    listaPosiciones = []
    for fila in range(n):
        Posiciones = [(fila,columna) for columna in range(n)]
        listaPosiciones.append(Posiciones)
    return listaPosiciones


#generaColumnas: int -> list(list(tuple(int,int)))
#Recibe la dimensión de la sopa de letras.
#Devuleve la lista de columnas (Posiciones) de la sopa de letras.

def generaColumnas(n):
    listaPosiciones = []
    for columna in range(n):
        Posiciones = [(fila,columna) for fila in range(n)]
        listaPosiciones.append(Posiciones)
    return listaPosiciones


#generaPosicionesPorPosicion: int tuple(int,int) -> list(list(tuple(int,int)))
#Recibe la dimensión de la sopa de letras y una elemento de tipo Posición.
#Devuelve todas la direcciones que contiene la posición ingresada.

def generaPosicionesPorPosicion(n, posicion):
    PosAux = []
    for posiciones in generaFilas(n):
        if posicion in posiciones:
            PosAux.append(posiciones)
    for posiciones in generaColumnas(n):
        if posicion in posiciones:
            PosAux.append(posiciones)
    for posiciones in generaDiagonales(n,1,0):
        if posicion in posiciones:
            PosAux.append(posiciones)
    return PosAux



#generaCombinaciones: List(list(tuple(int,int))) int -> List(list(tuple(int,int)))
#Recibe una lista de posiciones, la longitud de una palabra
#Devuelve una lista de posiciones con todas las combinaciones que se pueden armar
#con las posiciones de longitud mayor a la de palabra.

def generaCombinaciones(listPosiciones, longitud):
    listaPosiciones = []
    for Posiciones in listPosiciones:
        for i in range(len(Posiciones) - (longitud - 1)):
            listaPosiciones.append(Posiciones[i:longitud + i])
    return listaPosiciones



#generaPosiciones: int int int -> List(list(tuple(int,int)))
#Recibe la dimension, la longitud de una palabra y la complejidad de la sopa de letras.
#Devuleve una lista con todas las posibles posiciones que se pueden armar para una palabra.

def generaPosiciones(n, longitud, complejidad):
    listaPosiciones = []
    listaPosiciones = generaCombinaciones(generaFilas(n),longitud)
    listaPosiciones += generaCombinaciones(generaColumnas(n),longitud)
    if complejidad == 0:
        return listaPosiciones
    else:
        listaPosiciones += generaCombinaciones(generaDiagonales(n,longitud, complejidad),longitud)
        return listaPosiciones


#generaDicPalabra: String -> dict(dicPalabra)
#Recibe una palabra y devuleve un diccionario de tipo dicPalabra.

def generaDicPalabra(palabra):
    return {"Candidatos": [],
            "Longitud"  : len(palabra),
            "Candidato" : [],
            "Estado"    : True}

#generaDicMatirz: int -> dict(MatrizSopa)
#Recibe la dimensión de la sopa de letras.
#Devuelve un diccionario de tipo MatrizSopa donde cada componente esta mapeado al elemento Nulo ('-', 0).

def generaDicMatriz(n):
    matriz = dict()
    for fila in range(n):
        for columna in range(n):
            matriz[(fila,columna)] = ('-', 0)
    return matriz

#lecturaInfoArchivo: String -> Tuple(int,dict(infoPalabras),int)
#Recibe la ruta de un archivo.
#Devuelve una tupla (Dimension,infoPalabras,Complejidad) con la información obtenida en el archivo.

def lecturaInfoArchivo(archivo):
    infoArchivo = open(archivo,'r')
    linea = infoArchivo.readline()
    infoPalabras = {}
    while linea != '':
        if "DIMENSION" in linea:
            linea = infoArchivo.readline()
            dimension = int(linea[:-len('\n')])
            linea = infoArchivo.readline()
        elif "COMPLEJIDAD" in linea:
            linea = infoArchivo.readline()
            complejidad  = int(linea[:-len('\n')])
            linea = infoArchivo.readline()
        elif "PALABRAS" in linea:
            linea = infoArchivo.readline()
        else:
            palabra = linea[:-len('\n')]
            infoPalabras[palabra] = generaDicPalabra(palabra)
            linea = infoArchivo.readline()
    infoPalabras['Lista'] = sorted(list(infoPalabras), key = lambda x: len(x), reverse=True)
    infoArchivo.close()
    return (dimension, infoPalabras, complejidad)

#validaPalabraCruzada: lista(tupla(int,int)) dicMatriz int -> Boolean
#Recibe un candidato, un diccionario de tipo dicMatriz y la complejidad de la sopa de letra.
#Devuleve True si la palabra asociadas al candidato puede ser cruzada, es decir,
#para cada elemento del candidato, la relacion coordenada/letra es equivalente a la matriz
#o la matriz no tiene asignada ninguna letra.
#Caso contrario devuleve False.

def validaPalabraCruzada(candidato,dicMatrizSopa,complejidad):
    if complejidad != 3:
        return False
    else:
        for Posicion in candidato:
            letra = dicMatrizSopa[Posicion[0]][0]
            if letra != Posicion[1] and letra != '-':
                return False
        return True

#validaPalabraDisjunta: lista(tupla(int,int)) dict(MatrizSopa) -> Boolean
#Recibe un candidato y un diccionario dicMatriz.
#Devuelve True si para toda posicion asociada al candidato, la matriz tiene asignado
#el elemento nulo.
#Caso contrario devuelve False.

def validaPalabraDisjunta(candidato, dicMatrizSopa):
    for coordenada in candidato:
        letra = dicMatrizSopa[coordenada[0]][0]
        if letra != '-':
            return False
    return True

#validaCandidato: lista(tupla(int,int)) dict(MatrizSopa) int -> Boolean
#Recibe un candiato, un diccionario de tipo MatrizSopa y la complejidad de la sopa de letras.
#Devuelve True si la palabra asociada al candidato puede disponerse dentro de la matriz.
#Caso contrario devuelve False.

def validaCandidato(candidato, dicMatrizSopa, complejidad):
    boleano1 = validaPalabraCruzada(candidato, dicMatrizSopa, complejidad)
    boleano2 = validaPalabraDisjunta(candidato, dicMatrizSopa)
    return boleano1 or boleano2

#actualizaDicPosiciones: String dict(MatrizSopa) dict(infoPalabras) -> dict(Matriz)
#Recibe una palabra, un diccionario de tipo MatrizSopa y un diccionario de tipo infoPalabras.
#Aplica la relacion posicion/letra del candidato asociado a la palabra a las posiciones
#de la Matriz.

def actualizaMatriz(palabra, dicMatrizSopa, infoPalabras):

    for posicion in infoPalabras[palabra]['Candidato']:
        contador = dicMatrizSopa[posicion[0]][1]
        dicMatrizSopa[posicion[0]] = (posicion[1], contador + 1)
    return dicMatrizSopa

#borraPalabraMatriz: String dict(MatrizSopa) dict(infoPalabras) -> dict(matriz)
#Recibe una palabra, un diccionario de tipo MatrizSopa y un diccionario de tipo infoPalabras
#Toma las Posiciones asociadas al candidato de la palabra, en caso de que una posición en la matriz
#tiene el contador = 1, le asigna el elemento nulo.
#Caso contrario le resta uno al contador.
#Devuleve el diccionario de tipo MatrizSopa.

def borraPalabraMatriz(palabra, dicMatrizSopa, infoPalabras):

    for posicion in infoPalabras[palabra]['Candidato']:
        contador = dicMatrizSopa[posicion[0]][1]
        letra = dicMatrizSopa[posicion[0]][0]
        if contador == 1:
            dicMatrizSopa[posicion[0]] = ('-', 0)
        else:
            dicMatrizSopa[posicion[0]] = (letra, contador - 1)
    return dicMatrizSopa

#generaCandidatos:int string dict(MatrizSopa) dict(infoPalabras) int -> Lista(lista(tupla(tupla(int,int),char)))
#Recibe la dimensión de la sopa de letras, una palabra, un diccionario de tipo MatrizSopa, un diccionario de tipo infoPalabra
#y la complejidad de la sopa de letras.
#Devuelve una Lista de candidatos válidos en función de la complejidad de la sopa de letras los candidatos
#ya asignados.

def generaCandidatos(n, palabra, dicMatrizSopa, infoPalabras, complejidad):
    candidatos = []
    for Posiciones in generaPosiciones(n,infoPalabras[palabra]['Longitud'],complejidad):
        candidato = list(zip(Posiciones,palabra))
        if validaCandidato(candidato, dicMatrizSopa, complejidad):
            candidatos.append(candidato)
        if complejidad == 2 or complejidad == 3:
            candidato2 = list(zip(Posiciones,palabra[::-1]))
            if validaCandidato(candidato2, dicMatrizSopa, complejidad):
                candidatos.append(candidato2)
    return candidatos

    
#armaSopa: int int dict(Matriz) dict(infoPalabras) int -> Boolean
#Recibe al dimensión y complejidad de la sopa de letras, un diccionario de tipo MatrizSopa y un diccionario infoPalabras
#Devuelve en función de la dimenensión, la complejidad y las palabras, si la matriz se puede armar devuelve True.
#Caso contrario devulev False.

def armaMatrizSopa(n, complejidad, dicMatrizSopa, infoPalabras, contador = 0):
    if contador == len(infoPalabras['Lista']):
        return True
    palabra = infoPalabras['Lista'][contador]
    if infoPalabras[palabra]['Estado'] == True:
        infoPalabras[palabra]['Candidatos'] = generaCandidatos(n, palabra, dicMatrizSopa, infoPalabras, complejidad)
        infoPalabras[palabra]['Estado'] = False
    if infoPalabras[palabra]['Candidatos'] == [] and contador == 0:
        return False
    if infoPalabras[palabra]['Candidatos'] == []:
        infoPalabras[palabra]['Estado'] = True
        contador -= 1
        palabra = infoPalabras['Lista'][contador]
        dicMatrizSopa = borraPalabraMatriz(palabra, dicMatrizSopa, infoPalabras)
        infoPalabras[palabra ]['Solucion?'] = []
        return armaMatrizSopa(n, complejidad, dicMatrizSopa, infoPalabras, contador)
    else:

        infoPalabras[palabra]['Candidato'] = choice(infoPalabras[palabra]['Candidatos'])
        infoPalabras[palabra]['Candidatos'].remove(infoPalabras[palabra]['Candidato'])
        contador += 1
        dicMatrizSopa = actualizaMatriz(palabra,dicMatrizSopa,infoPalabras)
        return armaMatrizSopa(n, complejidad, dicMatrizSopa, infoPalabras, contador)

#convierteListaLestraACadena: List(Char) -> String
#Recibe una lista de letras (Char).
#Devuelve un String que resulta de concatenar todas las letras de la lista.

def convierteListaLetrasACadena(listaLetras):
    cadena = ''
    for letra in listaLetras:
        cadena += letra
    return cadena

#generaListaCadenas: int tuple(int,int) dict(MatrizSopa) -> list(String)
#Recibe la dimensión de la sopa de letras, una posición y un diccionario MatrizSopa.
#Devuelve una lista de Strings, donde cada una de estas esta

def posicionesACadenas(posiciones, dicMatrizSopa):
    letras = []
    for pos in posiciones:
        letras.append(dicMatrizSopa[pos][0])
    return convierteListaLetrasACadena(letras)

#acotaPosiciones: tuple(int,int) String list(list(tuple(int,int))) -> list(list(tuple(int,int)))
#Recibe una Posición, una palabra y lista de posiciones.
#Devuleve una lista de posiciones donde cada una de estas es modificada de modo que, desde el início
#de la lista hasta la posición haya elementos como la longitud de la palabra o menos, lo mismo en el
#caso en la cantidad de elementos desde la posición hasta el fin de la lista.

def acotaPosiciones(posicion, palabra, listPoss):
    posicionesAcotadas = []
    longitudPalabra = len(palabra) - 1
    for posiciones in listPoss:
        lenPosiciones = len(posiciones) - 1
        indicePosicion = posiciones.index(posicion)
        cotaInf = indicePosicion - longitudPalabra
        cotaSup = indicePosicion + longitudPalabra + 1
        if cotaInf < 0 and cotaSup > lenPosiciones:
            posicionesAcotadas.append(posiciones)
        elif cotaInf < 0:
            posicionesAcotadas.append(posiciones[:cotaSup])
        elif cotaSup > lenPosiciones:
            posicionesAcotadas.append(posiciones[cotaInf:])
        else:
            posicionesAcotadas.append(posiciones[cotaInf:cotaSup])
    return posicionesAcotadas

        
#verificaPalabraRepetida: int tuple(int,int) dict(MatrizSopa) dict(infoPalabras) -> Boolean
#Recibe la dimensión de la sopa de letras, una Posición, un diccionario MtrizSopa y un diccionario infoPalabras.
#Retorna True si no existe palabra que intersecte la posición ingresada.
#Caso contrario devuelve False.

def verificaPalabraRepetida(n, posicion, dicMatrizSopa, infoPalabras):
    listaPosiciones = generaPosicionesPorPosicion(n,posicion)
    for palabra in infoPalabras['Lista']:
        listaCadenas = [posicionesACadenas(posiciones, dicMatrizSopa)
                        for posiciones 
                        in acotaPosiciones(posicion, palabra, listaPosiciones)]
        for cadena in listaCadenas:
            if (palabra in cadena) or (palabra[::-1] in cadena):
                return False
    return True

#completaSopa: int dict(MatrizSopa) dict(infoPalabras) -> Boolean
#Recibe la dimension de la sopa de letras, un diccionario MatrizSopa y un diccionario infoPalabras.
#Devuelve True si se pudo remplazar todos las imagenes nulas de la matriz por una letra al azar sin
#que se repitan las palabras del diccionario infoPalabras.
#Caso contrario devuelve False.

def completaSopa(n, dicMatrizSopa, infoPalabras):
    for posicion, letra in dicMatrizSopa.items():
        letras = list('abcdefghijklmnñopqrstuvwxyz')
        if letra[0] == '-':
            bandera = True
            while bandera:
                if letras == []:
                    return False
                candidatoLetra = choice(letras)
                letras.remove(candidatoLetra)
                dicMatrizSopa[posicion] = (candidatoLetra, 0)
                if verificaPalabraRepetida(n, posicion, dicMatrizSopa, infoPalabras):
                    bandera = False
    return True

#escribeSopa: int dict(MatrizSopa) dict(infoPalabras) -> Nan
#Recibe un archivo de salida y escribe "Sopa De Letras" y la concatenación de letras que se forma con cada
#vector fila de la matriz MatrizSopa.

def escribeSopa(n, archivoSalida, dicMatrizSopa):
    salida = open(archivoSalida,'w')
    salida.write('Sopa De Letras\n')
    for fila in range(n):
        linea = ''
        for columna in range(n):
            linea += (dicMatrizSopa[(fila,columna)][0])
        linea += '\n'
        salida.write(linea)
    salida.close()

def sopaDeLetras():
    DatosDeEntrada = lecturaInfoArchivo(argv[1])
    archivoSalida = argv[2]
    Dimension = DatosDeEntrada[0]
    infoPalabras = DatosDeEntrada[1]
    Complejidad = DatosDeEntrada[2]
    MatrizSopa = generaDicMatriz(Dimension)
    if armaMatrizSopa(Dimension,Complejidad,MatrizSopa,infoPalabras):
        if completaSopa(Dimension,MatrizSopa,infoPalabras):
            escribeSopa(Dimension,archivoSalida,MatrizSopa)
            print('La sopa de letras se generó con éxito.')
        else:
            print('No se pudo completar la sopa de letras generada.')
    else:
        print('No se pudo generar la sopa de letras.')

#sopaDeLetras()
    



