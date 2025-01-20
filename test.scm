; Declaración de constantes
(define x 10)
(define y 5)

; Mostrar un saludo
(display "Hola, mundo!")
(newline)

; Operaciones aritméticas
(display (+ x y))       ; Esperado: 15
(display (- x y))       ; Esperado: 5
(display (* x y))       ; Esperado: 50
(display (/ x y))       ; Esperado: 2
(display (mod 6 4))     ; Esto debería dar 2

; Expresiones booleanas
(display (and #t #f))   ; Esperado: #f
(display (or #t #f))    ; Esperado: #t
(display (not #t))      ; Esperado: #f

; Condicionales
(display (if (> x y) "x es mayor" "x es menor"))  ; Esperado: "x es mayor"

; Expresiones cond
(display (cond
            ((< x y)  "x es menor")
            ((= x y)  "x es igual")
            (#t "x es mayor")))                    ; Esperado: "x es mayor"

(display (cond
  ((> 5 10) "Mayor que 10")
  ((< 5 2) "Menor que 2")
  (else "Está entre 2 y 10"))) ; Esperado: "Está entre 2 y 10"

; Funciones
(define (sumar a b) (+ a b))
(display (sumar 3 4))                             ; Esperado: 7

; Uso de let
(display (let ((a 3)
                (b 7))
            (+ a b)))                              ; Esperado: 10

; Listas
(display '(1 2 3 4))                              ; Esperado: '(1 2 3 4)

; Operaciones con listas
(define lista '(1 2 3 4 5))
(display (car lista))                             ; Esperado: 1
(display (cdr lista))                             ; Esperado: '(2 3 4 5)
(display (cons 0 lista))                          ; Esperado: '(0 1 2 3 4 5)
(display (null? '()))                             ; Esperado: #t
(display (null? lista))                           ; Esperado: #f

; Factorial (recursividad)
(define (factorial n)
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))
(display (factorial 5))                           ; Esperado: 120

; Suma de elementos de una lista (recursividad)
(define (suma_lista lista)
  (if (null? lista)
      0
      (+ (car lista) (suma_lista (cdr lista)))))
(display (suma_lista '(1 2 3 4 5)))               ; Esperado: 15

; Funciones de orden superior
(define (dobla x) (* x 2))
(define (aplicadoscops f x) (f (f x)))
(display (aplicadoscops dobla 5))                 ; Esperado: 20

; Función map y filter
(define (parell? x) (= (mod x 2) 0))
(define (map func llista)
  (cond
    ((null? llista) '())
    (#t (cons (func (car llista)) (map func (cdr llista))))))
(define (filter predicat llista)
  (cond
    ((null? llista) '())
    ((predicat (car llista))
      (cons (car llista) (filter predicat (cdr llista))))
    (#t (filter predicat (cdr llista)))))
(define llista '(1 2 3 4 5 6 7 8))
(display (map dobla (filter parell? llista)))     ; Resultado: (4 8 12 16)

; Función que utiliza read y newline
(define (mult_dos_valores)
  (let ((val1 (read))
        (val2 (read)))
     (display "El producto es:")
     (display (* val1 val2))))
(mult_dos_valores)                                ; Resultado: El producto de los valores introducidos