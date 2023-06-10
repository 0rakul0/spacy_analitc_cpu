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
ner.add_label('CONCILIACAO')
# ner.add_label('AGRAVO_ADMITIDO')
# ner.add_label('ACORDO')
ner.add_label('ALIMENTO')
ner.add_label('TUTELA')
ner.add_label('SENTENCA')
ner.add_label('SAIDA_DE_PRESO')

# Inicie o treinamento
nlp.begin_training()

def find_tags(text):
    entities = []
    match_acordo = re.search(r'\bacordo(s|am|ram)?\b', text, re.I)
    match_agravo_admitido = re.search(r'\bagrav[oa]\b|\bagrav[oa].*?admitid[oa]|\badmitid[oa].*?agrav[oa]\b|interpos.*?tempestiv[oa]', text, re.I)
    match_concilicacao = re.search(r'concilia..o|conciliaram', text, re.I)
    match_alimento = re.search(r'alimentos provis.rios|alimenta..o|fome', text, re.I)
    match_tutela = re.search(r'pedido de tutela', text, re.I)
    match_sentenca = re.search(r'senten.a|senten.a\scondenat.ria|execu..o\sda\spena|Execu..o\sPenal', text, re.I)
    match_saida_preso = re.search(r'\(Lei\s+7\.210\/84\)|SA.DA\s+TEMPOR.RIA', text, re.I)
    # if match_acordo:
    #     start, end = match_acordo.span()
    #     entities.append((start, end, 'ACORDO'))
    # if match_agravo_admitido:
    #     start, end = match_agravo_admitido.span()
    #     entities.append((start, end, 'AGRAVO_ADMITIDO'))
    if match_concilicacao:
        start, end = match_concilicacao.span()
        entities.append((start, end, 'CONCILIACAO'))
    if match_alimento:
        start, end = match_alimento.span()
        entities.append((start, end, 'ALIMENTO'))
    if match_tutela:
        start, end = match_tutela.span()
        entities.append((start, end, 'TUTELA'))
    if match_sentenca:
        start, end = match_sentenca.span()
        entities.append((start, end, 'SENTENCA'))
    if match_saida_preso:
        start, end = match_saida_preso.span()
        entities.append((start, end, 'SAIDA_DE_PRESO'))
    return entities

TRAIN_DATA = []
for texto in DETECT_NOTS:
    tags = find_tags(texto)
    annotations = {'entities': tags}
    example = (texto, annotations)
    TRAIN_DATA.append(example)

# Treine por 10 iterações
for itn in range(30):
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
