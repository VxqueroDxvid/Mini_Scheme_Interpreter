grammar scheme;

root 
    : (declaration | expr)* EOF 
    ;

// Declaraciones
declaration
    : LPAR DEF ID expr RPAR                    // Definición de constantes
    ;

func_declaration
    : LPAR ID (ID)* RPAR expr+    // Definición de funciones
    ;

func_invocation
    : ID expr*                                 // Invocación de funciones
    ;

// Expresiones
expr
    : literal                                       // Literales
    | LPAR READ RPAR                                // Uso de read
    | LPAR DEF func_declaration RPAR                // Funciones definidas por el usuario
    | LPAR func_invocation RPAR                     // Invocación de funciones definidas por el usuario
    | LPAR operator expr+ RPAR                      // Operadores aritméticos y relacionales
    | LPAR logical_operator expr+ RPAR              // Operadores lógicos
    | LPAR CAR expr RPAR                            // Operador car
    | LPAR CDR expr RPAR                            // Operador cdr
    | LPAR CONS expr expr RPAR                      // Operador cons
    | LPAR NULLP expr RPAR                          // Operador null?
    | LPAR IF if_clause RPAR                        // Condicional if
    | LPAR COND cond_clause+ RPAR                   // Condicional cond
    | LPAR LET LPAR let_binding+ RPAR expr+ RPAR    // Declaración let
    | LPAR DISPLAY expr RPAR                        // Invocación de display
    | LPAR NEWLINE RPAR                             // Salto de línea
    | ID                                            // Identificadores
    ;


// Literales
literal
    : NUMBER
    | BOOLEAN
    | STRING
    | quoted_list
    ;

// Lista entre apóstrofe y paréntesis
quoted_list
    : LISTA LPAR literal* RPAR                        
    ;

// Clausulas de condicional cond
cond_clause
    : LPAR expr expr+ RPAR
    | LPAR ELSE expr+ RPAR  // Clausula else                        
    ;

// Clausulas de condicional if
if_clause
    : expr expr expr                               
    ;

// Bindings de let
let_binding
    : LPAR ID expr RPAR                             
    ;

// Operadores aritméticos y relacionales
operator
    : SUM | SUB | MUL | DIV | MOD
    | LT | LE | GT | GE | EQ | NEQ
    ;

// Operadores lógicos
logical_operator
    : AND
    | OR
    | NOT
    ;

// Operadores de listas
CAR: 'car';
CDR: 'cdr';
CONS: 'cons';
NULLP: 'null?';

// Operadores lógicos
AND: 'and';
OR: 'or';
NOT: 'not';

// IMPORTANTES
DISPLAY: 'display';
NEWLINE: 'newline';
READ:  'read';
DEF: 'define';
IF: 'if';
COND: 'cond';
ELSE: 'else';
LET: 'let';

// Tokens
NUMBER: '-'? [0-9]+;
BOOLEAN: '#t' | '#f';
STRING: '"' (~["\\] | '\\' .)* '"';

// Operadores aritméticos y relacionales
SUM : '+';
SUB : '-';
MUL: '*';
DIV:  '/';
MOD: 'mod';
LT: '<';
LE: '<=';
GT: '>';
GE: '>='; 
EQ: '=';
NEQ: '<>';

// Paréntesis y apóstrofes
LPAR: '(';
RPAR: ')';
LISTA: '\''; // el símbolo \ permite que ANTLR reconozca el apóstrofe correctamente

// Espacios y comentarios
SPACE: [ \t\r\n]+ -> skip;
COMMENT: ';' ~[\r\n]* -> skip;
ID: [a-zA-Z_][a-zA-Z0-9_?]*;