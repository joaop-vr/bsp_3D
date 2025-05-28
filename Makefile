# Nome do executável final
EXEC = convex

# Alvo principal
all:
        cp convex.py $(EXEC)
        chmod +x $(EXEC)

# Limpa o executável gerado
clean:
        rm -f $(EXEC)


