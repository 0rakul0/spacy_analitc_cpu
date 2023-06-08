import pt_core_news_lg

nlp = pt_core_news_lg.load()
doc = nlp("Esta é uma frase.")
print([(w.text, w.pos_) for w in doc])