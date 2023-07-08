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

from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D, Dropout, Reshape
from keras.preprocessing.text import Tokenizer
from keras.utils import np_utils, pad_sequences
from keras.models import model_from_json

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix, accuracy_score

import numpy as np
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import matplotlib.pyplot as plt

class por_regras():

    def __init__(self):
        ## import do dataset
        self.Tweets = pd.read_csv('../dados/voos/Tweets2.csv')
        self.exploracao()
    def run(self, ja_treinado=None):
        if ja_treinado:
            self.veder()
        else:
            self.supervisonado()

    def plot_graphs(self,history, metric):
        plt.plot(history.history[metric])
        plt.plot(history.history['val_' + metric], '')
        plt.xlabel("Epochs")
        plt.ylabel(metric)
        plt.legend([metric, 'val_' + metric])

    def exploracao(self):
        print(self.Tweets.shape)
        print(self.Tweets.info())
        self.tratamento()

    def tratamento(self):
        ## na coluna sentiment: vamos pegar o sentimento irrelevante da doluna sentiment e passar para neutro
        try:
            self.Tweets.loc[self.Tweets['sentiment']=='Irrelevant', 'sentiment'] = 'Neutral'
        except:
            pass
        self.Tweets = self.Tweets.dropna(subset=['text'])
        self.Tweets.reset_index(drop=True, inplace=True)
        print(self.Tweets.groupby(['sentiment']).size())

    def supervisonado(self):
        token = Tokenizer(num_words=60)
        token.fit_on_texts(self.Tweets['text'].values)

        x = token.texts_to_sequences(self.Tweets['text'].values)
        x = pad_sequences(x, padding="post", maxlen=60)

        labelencoder = LabelEncoder()
        y = labelencoder.fit_transform(self.Tweets['sentiment'])
        y = np_utils.to_categorical(y)

        x_treino, x_teste, y_treino, y_teste = train_test_split(x, y, test_size=0.3)

        tamanho_token = len(token.word_index) + 1

        modelo = Sequential()
        modelo.add(Embedding(input_dim=tamanho_token, output_dim=128, input_length=60))
        modelo.add(Dropout(0.2))
        modelo.add(LSTM(units=196, activation='tanh', recurrent_activation='sigmoid', unroll=False, use_bias=True))
        modelo.add(Dense(units=3, activation='softmax'))
        modelo.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        """print(modelo.summary())
        
        Model: "sequential"
        _________________________________________________________________
         Layer (type)                Output Shape              Param #   
        =================================================================
         embedding (Embedding)       (None, 60, 128)           4324352   
                                                                         
         dropout (Dropout)           (None, 60, 128)           0         
                                                                         
         lstm (LSTM)                 (None, 196)               254800    
                                                                         
         dense (Dense)               (None, 3)                 591       
                                                                         
        =================================================================
        Total params: 4,579,743
        Trainable params: 4,579,743
        Non-trainable params: 0
        _________________________________________________________________
        None

        """

        history = modelo.fit(x_treino, y_treino, epochs=10, batch_size=500, verbose=True)

        test_loss, test_acc = modelo.evaluate(x_teste, y_teste)
        print('Test Loss:', test_loss)
        print('Test Accuracy:', test_acc)

        try:
            plt.figure(figsize=(16, 8))
            plt.subplot(1, 2, 1)
            self.plot_graphs(history, 'accuracy')
            plt.ylim(None, 1)
            plt.subplot(1, 2, 2)
            self.plot_graphs(history, 'loss')
            plt.ylim(0, None)
        except:
            pass


        modelo_sentimentos = modelo.to_json()
        with open('./modelo_sentimentos.json', 'w') as json_file:
            json_file.write(modelo_sentimentos)
        modelo.save_weights('./modelo_sentimentos.h5')

    def veder(self):
        # para carregar o modelo
        # arquivo = open('./modelo_sentimentos.json', 'r')
        # estrutura_rede = arquivo.read()
        # arquivo.close()
        #
        # modelo = model_from_json(estrutura_rede)
        # modelo.load_weights('./modelo_sentimentos.h5')

        mas = SentimentIntensityAnalyzer()
        self.Tweets['veder_sentiment'] = ''

        for y in range(len(self.Tweets.index)):
            x = mas.polarity_scores(str(self.Tweets['text'].iloc[y]))
            del x['compound']
            maior = max(x, key=x.get, default=None)  # neg ou pos ou neu
            self.Tweets.loc[y,'veder_sentiment'] = maior

        # Normalizando o dado
        self.Tweets.loc[self.Tweets['veder_sentiment'] == 'neg', 'vander_sentiment'] = 'Negative'
        self.Tweets.loc[self.Tweets['veder_sentiment'] == 'neu', 'vander_sentiment'] = 'Neutral'
        self.Tweets.loc[self.Tweets['veder_sentiment'] == 'pos', 'vander_sentiment'] = 'Positive'

        y_pred = self.Tweets['vander_sentiment']
        y_test = self.Tweets['sentiment']

        self.matrix(y_pred, y_test)

    def matrix(self, y_pred, y_test):
        cm = confusion_matrix(y_test, y_pred)
        print(cm)

        accuracy = accuracy_score(y_test, y_pred)
        print(accuracy)

if __name__ == "__main__":
    p = por_regras()
    p.run(ja_treinado=True)