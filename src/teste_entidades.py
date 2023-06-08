import spacy

# Carregar o modelo treinado
nlp = spacy.load("./modelo_treinado")

# Texto de exemplo para validação
texto = "As partes celebraram um acordo de conciliação para resolver a disputa de forma amigável."


# Aplicar o modelo no texto
doc = nlp(texto)

# Imprimir a frase completa
print("Frase:", doc.text)

# Iterar pelas entidades encontradas no texto
for entidade in doc.ents:
    print("Entidade:", entidade.text)
    print("Início:", entidade.start)
    print("Fim:", entidade.end)
    print("Rótulo:", entidade.label_)
    print("---")
