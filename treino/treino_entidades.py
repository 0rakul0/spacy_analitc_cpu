import os
import random
import re
import spacy
from spacy.training import Example
from spacy.util import minibatch

os.environ['KMP_DUPLICATE_LIB_OK']='True'

try:
    load_modelo = spacy.load("../modelo_treinado")
    if load_modelo:
        nlp = spacy.load("../modelo_treinado")
except:
    # Comece com o modelo em branco de spaCy
    nlp = spacy.blank('pt')

# No exemplo, a string contém o texto e o dicionário contém as entidades
DETECT_NOTS = []
caminho_arquivo = '../src/corpus_modelos_frases.txt'

# Abre o arquivo em modo de leitura
with open(caminho_arquivo, "r", encoding='utf-8') as arquivo:
    # Lê cada linha do arquivo
    linhas = arquivo.readlines()
    for linha in linhas:
        # Remove espaços em branco e quebras de linha
        linha = linha.strip()
        if linha:
            # Adiciona a linha à lista DETECT_NOTS
            DETECT_NOTS.append(linha)

# Crie o pipeline 'ner'
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")
else:
    ner = nlp.get_pipe("ner")

# Adicione as frases que você está interessado como entidades
"""
etiqueta_nova = 'NOVO_ROTULO'
ner.add_label(etiqueta_nova)
"""
ner.add_label('AGRAVO_ADMITIDO')
ner.add_label('ACORDO')

# Inicie o treinamento
nlp.begin_training()

def find_tags(text):
    entities = []
    match_acordo = re.search(r'\bacordo(s|am|ram)?\b', text, re.I)
    if match_acordo:
        start, end = match_acordo.span()
        entities.append((start, end, 'ACORDO'))
    match_agravo_admitido = re.search(r'\bagrav[oa]\b|\bagrav[oa].*?admitid[oa]|\badmitid[oa].*?agrav[oa]\b|interpos.*?tempestiv[oa]', text, re.I)
    if match_agravo_admitido:
        start, end = match_agravo_admitido.span()
        entities.append((start, end, 'AGRAVO_ADMITIDO'))
    return entities

TRAIN_DATA = []
for texto in DETECT_NOTS:
    tags = find_tags(texto)
    annotations = {'entities': tags}
    example = (texto, annotations)
    TRAIN_DATA.append(example)

# Treine por 10 iterações
for itn in range(20):
    # Embaralhe os dados de treinamento
    random.shuffle(TRAIN_DATA)
    losses = {}

    examples = []
    for text, annot in TRAIN_DATA:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annot)
        examples.append(example)

    # Lote os exemplos usando spaCy's minibatch
    batches = minibatch(examples, size=8)
    for batch in batches:
        nlp.update(batch, losses=losses)

    print("Perdas:", losses)

nlp.to_disk("../modelo_treinado")
