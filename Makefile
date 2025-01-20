# Makefile para compilar archivos de ANTLR

# Variables
ANTLR_JAR=antlr-4.13.2-complete.jar
GRAMMAR=scheme.g4
TARGET=Python3

# Regla por defecto: generar archivos de ANTLR
all:
	java -jar $(ANTLR_JAR) -Dlanguage=$(TARGET) -visitor $(GRAMMAR)

# Regla para limpiar archivos generados por ANTLR
clean:
	rm -f schemeLexer.py schemeParser.py schemeVisitor.py schemeListener.py *.interp *.tokens