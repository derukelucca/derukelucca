import unicodedata

def remover_acentos(texto):
    texto_sem_acentos = ''.join(
        caracter for caracter in unicodedata.normalize('NFD', texto)
        if unicodedata.category(caracter) != 'Mn'
    )
    return texto_sem_acentos

# Exemplo de uso:
texto_com_acentos = "Olá, como está você?"
texto_sem_acentos = remover_acentos(texto_com_acentos)
print(texto_sem_acentos)
