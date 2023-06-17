import spacy

# Carregar o modelo pré-treinado
nlp = spacy.load("pt_core_news_lg")

# Texto de exemplo
texto = "Autor: Marineide Delgado Miranda, Réu: Alvaro Martins Horta =>Distribuição por Sorteio, Valor da Causa: R$ 1.090,00  Adv - Não consta registro de adv ogado.  JESP 2A CÍVEL  Juiz(íza): Erick Cavalcanti Linhares Lima"

# Aplicar o modelo no texto
doc = nlp(texto)

# Iterar pelas entidades encontradas no texto
for entidade in doc.ents:
    print("Texto da entidade:", entidade.text)
    print("Rótulo da entidade:", entidade.label_)
    print("---")
