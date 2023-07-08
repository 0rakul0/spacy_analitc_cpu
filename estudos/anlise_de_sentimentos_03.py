"""
Polarity Resultado

o Textblob
- polarity: valor real de -1 (ruim) a 1 (bom)
- Subjectivity: o quanto a sentença se refere a opinião, julgamento ou emoção. Valor real entre 0 e 1, quanto mais proximo de 1 mais sebjetivo

para o portugues
https://github.com/rafjaa/LeIA/blob/master/README.md

outra forma é tradução de ida e volta
pip install translate

"""

import nltk

# try:
#     nltk.download("vader_lexicon")
# except:
#     print("ja foi executado")
def en():
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    mas = SentimentIntensityAnalyzer()
    # função, lambda
    analisa = lambda x: mas.polarity_scores(x)
    lista = [":)"]
    for i in lista:
        print(analisa(i))
        print(analisa(i)['pos'])

    ### outro exemplo
    from textblob import TextBlob
    teste = TextBlob("i love Brazil")
    print(teste.sentiment)

def pt():
    from lexicon_setiment.leia import SentimentIntensityAnalyzer
    br_mas = SentimentIntensityAnalyzer()
    # função, lambda
    analisa = lambda x: br_mas.polarity_scores(x)
    lista = ["tem coisa que é legal de ver!"]
    for i in lista:
        print(analisa(i))
        print(analisa(i)['pos'])
def com_tradutor():
    from translate import Translator
    translator = Translator(from_lang="pt", to_lang="en")
    traducao = translator.translate("isto e uma caneta")
    print(traducao)

com_tradutor()