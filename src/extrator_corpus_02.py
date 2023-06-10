import re
import spacy

def classificador(text):
    # Carregar o modelo treinado
    modelo_treinado = "../modelo_treinado"
    nlp = spacy.load(modelo_treinado)
    # Aplicar o modelo no texto
    doc = nlp(text)
    tags = []
    # Iterar pelas entidades encontradas no texto
    for entidade in doc.ents:
        tags.append(entidade.label_)
    return tags

with open("filtrado.txt", "r", encoding="utf-8") as arquivo:
    conteudo = arquivo.readlines()

for linha in conteudo:
    linha = linha.strip('SEPARADOR_PROCESSO ').replace('\n','')
    # Processar o texto e obter as tags
    tags = classificador(linha)
    # Imprimir as tags encontradas
    tags_str = ", ".join(tags)
    processo_num = re.search('\d{4,5}\s+.\s+\d{11}\s.\d|\d{4,5}.*\d{6}\s\d{5}.*\d|\d{4,5}.\-.\d{10}\s\d\-\d|PROC.\:\s\d{2}.*\d{6}.*\d|Processo\sn\...\d{4}.\d{2}.\d{6}.\-\d.\–|Proc\..n.?\..*\s+\d{4}\s\-\d\/\d{2}\s\–', linha)

    print(tags_str, ' -> ', linha)


