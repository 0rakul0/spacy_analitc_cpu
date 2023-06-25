import spacy

nlp = spacy.load('pt_core_news_lg')

print(nlp.pipe_names)

corpus = nlp("as ações da Magazine Luisa S.A., França e Brasil, acumulam baixa de 70%")

print(len(corpus))

print(type(corpus))

"""
Propriedades, dessa forma de verdadeiro e falso, podemos remover itens que não queremos na nossa mineração
"""
print("Tokens: ",[token.text for token in corpus])
print("stop word: ",[token.is_stop for token in corpus])
print("Alfanumerico: ",[token.is_alpha for token in corpus])
print("Maiusculo: ",[token.is_upper for token in corpus])
print("Pontuação: ",[token.is_punct for token in corpus])
print("numero: ",[token.like_num for token in corpus])
print("Sentença Inicial: ",[token.is_sent_start for token in corpus])
print("Sentença final: ",[token.is_sent_end for token in corpus])

"""
para vizualizar o Formato
"""
print("\n\n")
print("Tokens: ",[token.text for token in corpus])
print("Formato: ",[token.shape_ for token in corpus])

