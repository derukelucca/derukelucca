import os

def obter_caminhos_arquivos(diretorio):
    caminhos_arquivos = []
    
    for root, dirs, files in os.walk(diretorio):
        for file in files:
            caminho_arquivo = os.path.join(root, file)
            caminhos_arquivos.append(caminho_arquivo)
    
    return caminhos_arquivos

diretorio = '/caminho/do/seu/diretorio'
caminhos = obter_caminhos_arquivos(diretorio)

for caminho in caminhos:
    print(caminho)
