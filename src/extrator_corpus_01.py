import re

# Função para extrair o texto antes do número do processo
def extrair_texto_depois(corpus):
    texto = []
    padrao_cabecalho = r"Diário do Poder Judiciário\s+ANO\s+\w{2}\s+-\s+EDIÇÃO\s+\d+\s+Boa Vista -RR, \d+ de [a-zA-Z]+ de \d+|'Boa\sVista.*RR.*\d+ de [a-zA-Z]+ de \d{4}\s+ANO\s+\w{2}\s+.\s+EDI..O\s+\d{4}}'"
    for linha in corpus:
        linha_sem_cabecalho = re.sub(padrao_cabecalho, "", linha)
        texto.append(linha_sem_cabecalho.strip())
    texto_formatado = []
    bloco = ""
    for linha in texto:
        if re.match(r"\d{4,5}\s+.\s+\d{11}\s.\d|\d{4,5}.*\d{6}\s\d{5}.*\d|\d{4,5}.\-.\d{10}\s\d\-\d|PROC.\:\s\d{2}.*\d{6}.*\d|EDITAL\s+DE ", linha):
            if bloco:
                texto_formatado.append(bloco.strip())
            bloco = linha
        else:
            bloco += " " + linha
    if bloco:
        texto_formatado.append(bloco.strip())
    texto_junto = "\nSEPARADOR_PROCESSO ".join(texto_formatado[1:-1])
    print(texto_junto)
    return texto_junto

# Corpus de exemplo
nome_arquivo = "D:/dados/RR/DJRR/txt/2003/01/DJRR_2003_01_10.txt"  # Substitua pelo caminho correto do arquivo
with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
    corpus = arquivo.readlines()

resultado = extrair_texto_depois(corpus)
with open("./filtrado.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write(resultado)