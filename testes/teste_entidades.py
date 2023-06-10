import spacy

def process_text(text):
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

# Texto de exemplo para validação
texto = "Foi concedido o agravo admitido, e posteriormente as partes firmaram um acordo judicial."

# Processar o texto e obter as tags
tags = process_text(texto)

# Imprimir as tags encontradas
tags_str = ", ".join(tags)
print( texto, "|", tags_str, "|")