# Intérprete de Mini Scheme

Esta documentación describe la práctica de compiladores del alumno de la materia LP David Vaquero Durán. En esta práctica, se implementa un intérprete para una versión simplificada del lenguaje **Scheme** utilizando **Python** y **ANTLR**.

## Descripción General

**Scheme** es un lenguaje de programación funcional derivado de **Lisp**, conocido por su simplicidad y estructura basada en expresiones. Este proyecto desarrolla un intérprete para un subconjunto de Scheme, denominado **Mini Scheme**.

### Ejemplos de Programas en Mini Scheme

```scheme
; Programas que calculan el factorial de un número y la suma de una lista, respectivamente

(define (factorial n)
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))

(define (suma_lista lista)
  (if (null? lista)
      0
      (+ (car lista) (suma_lista (cdr lista)))))

(define (main)
  (display "Factorial de 5: ")
  (display (factorial 5))
  (newline)
  (display "Suma de la lista '(1 2 3 4 5): ")
  (display (suma_lista '(1 2 3 4 5)))
  (newline))
```

## Características Implementadas

El intérprete soporta las siguientes características de Scheme:

### Sintaxis Básica

Las expresiones en Scheme son listas donde el primer elemento es una función y los siguientes son los argumentos. Ejemplo:

```scheme
(función argumento1 argumento2 ...)
```

### Operaciones Aritméticas Básicas

- Suma: `(+ 10 5)`  ; Resultado: 15
- Resta: `(- 10 5)` ; Resultado: 5
- Multiplicación: `(* 10 5)` ; Resultado: 50
- División: `(/ 10 5)` ; Resultado: 2
- Módulo: `(mod 6 4)` ; Resultado: 2

### Expresiones booleanas

- And: `(and #t #f)`  ; Resultado: #f
- Or: `(or #t #f)` ; Resultado: #t
- Not: `(not #t)` ; Resultado: #f

### Operadores relacionales básicos

Los operadores básicos que se pueden usar son: `>, <, >=, <=, =, <>`

### Condicionales

```scheme
(if (> 10 5)
    "x es mayor"
    "x es menor")  ; Resultado: "x es mayor"
```

```scheme
(cond
  ((< 10 5) "x es menor")
  ((= 10 5) "x es igual")
  (#t "x es mayor"))  ; Resultado: "x es mayor" (también se puede poner else en vez de #t)
```

### Listas

```scheme
(define lista '(1 2 3 4 5))
(display (car lista))  ; Resultado: 1
(display (cdr lista))  ; Resultado: (2 3 4 5)
(display (cons 0 lista))  ; Resultado: (0 1 2 3 4 5)
(display (null? '()))  ; Resultado: #t
(display (null? lista))  ; Resultado: #f
```

### Recursividad

```scheme
(define (factorial n)
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))
(factorial 5)  ; Resultado: 120
```

```scheme
(define (suma_lista lista)
  (if (null? lista)
      0
      (+ (car lista) (suma_lista (cdr lista)))))
(suma_lista '(1 2 3 4 5))  ; Resultado: 15
```

### Funciones de Orden Superior (como map y filter)

```scheme
(define (map func lista)
  (cond
    ((null? lista) '())
    (#t (cons (func (car lista)) (map func (cdr lista))))))

(define (filter predicado lista)
  (cond
    ((null? lista) '())
    ((predicado (car lista)) (cons (car lista) (filter predicado (cdr lista))))
    (#t (filter predicado (cdr lista)))))

(define lista '(1 2 3 4 5 6 7 8))
(display (map dobla (filter (lambda (x) (= (mod x 2) 0)) lista)))  ; Resultado: (4 8 12 16). (Función parecida a la del ejemplo)
```

### Entrada por parte del usuario

```scheme
(define (mult_dos_valores)
  (let ((val1 (read))
        (val2 (read)))
     (display "El producto es:")
     (display (* val1 val2))))
(mult_dos_valores) ; Resultado: El producto de los valores introducidos
```

## Estructura del Proyecto

```plaintext
mini-scheme/
├── antlr-4.13.2complete.jar          # Archivo Complete Antlr4
├── scheme.g4                         # Gramática de Mini Scheme
├── scheme.py                         # Código con la función principal (main)
├── interpreter.py                    # Archivo con todas las funciones, visitadores...
├── test.scm                          # Archivo de pruebas
├── input.inp                         # Documento de texto con la entrada
├── salida.out                        # Documento de texto donde se redirige la salida
├── README.md                         # Documentación del proyecto
└── Makefile                          # Script de construcción
```

## Uso del Intérprete

### Instalación

1. Descomprime la carpeta zip con el trabajo
   ```bash
   unzip david_vaquero_scheme.zip
   ```

2. Instala las dependencias de Python:
   ```bash
   pip install antlr4-python3-runtime
   ```

3. Genera el analizador con ANTLR:
   ```bash
   antlr4 -Dlanguage=Python3 scheme.g4
   ```

4. Compila el proyecto:
   ```bash
   make
   ```

5. Limpieza de archivos generados por ANTLR. No es necesario, pero existe la posibilidad de hacerlo usando:
   ```bash
   make clean
   ```

### Ejecución

- **Ejecución sin archivo de entrada ni archivo de salida**: No se redirige nada, habrá que introducir los valores manualmente y la salida será por terminal.

```bash
python3 scheme.py test.scm
```

- **Ejecución sin archivo de entrada**: La salida se redirige al archivo "salida.out", pero habrá que introducir los valores manualmente (en mi juego de pruebas hay que introducir primero un valor y luego el otro, son 2)

```bash
python3 scheme.py test.scm > salida.out
```

- **Ejecución con archivos de entrada/salida**: La salida se redirige al archivo "salida.out", y la entrada será la proporcionada en el archivo "input.inp".

Ejemplo:

```bash
python3 scheme.py test.scm < input.inp > salida.out
```

## Juego de pruebas

El archivo `test.scm` incluye un conjunto de pruebas que cubren y verifican todas las funcionalidades del intérprete. Todas las líneas de "Ejecución" mencionadas antes funcionan con este juego de prueba, el cual está en lenguaje Scheme, claro está (Mini Scheme).

Compara los resultados obtenidos con los esperados indicados en los comentarios del `test.scm`.

## Estilo del código

Los archivos .py (en Python) del proyecto siguen las reglas de estilo PEP8.

## Decisiones de diseño

### 1. Simplicidad del diseño

- Se ha priorizado un diseño modular y fácil de entender.
- Cada característica del intérprete (operadores, condicionales, listas, etc.) se implementa como una función separada.

### 2. Entorno Global

- Se utiliza un diccionario (self.global_env) para almacenar las variables y funciones definidas por el usuario.

### 3. Tratamiento de Errores

- Se incluyen mensajes claros y descriptivos para casos como variables no definidas o listas mal formadas ("Error: El apóstrofe debe ir seguido de una lista válida entre paréntesis.").

### 4. Soporte a funciones de orden superior

- El intérprete soporta funciones como map y filter (definidas por el usuario) que demuestran la capacidad de trabajar con funciones de orden superior.
  

## Limitaciones del programa

Este programa no trata los errores de ejecución (como podría ser una división por 0) o los errores de tipo (cuando se encuentran datos de un tipo inesperado en un contexto donde se esperaba un tipo específico).

Un pequeño apunte para finalizar, es que no se ha implementado la función `main` en el archivo del juego de pruebas, tiene que ser una función definida por el usuario.