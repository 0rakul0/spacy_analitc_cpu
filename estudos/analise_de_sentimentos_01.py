import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
import numpy as np

Tweets = pd.read_csv('../dados/voos/Tweets.csv')

Tweets = Tweets[Tweets['airline_sentiment_confidence'] > 0.8]

token = Tokenizer(num_words=100)
token.fit_on_texts(Tweets['text'].values)

X = token.texts_to_sequences(Tweets['text'].values)
X = pad_sequences(X, padding="post", maxlen=50)

label_names = Tweets['airline_sentiment'].unique()
label_to_index = {label: index for index, label in enumerate(label_names)}
y = np.array([label_to_index[label] for label in Tweets['airline_sentiment']])

num_classes = len(label_names)
y = np.eye(num_classes)[y]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

tamanho_shape = X.shape[1]

# Definir o modelo LSTM
modelo = Sequential()
modelo.add(Embedding(input_dim=len(token.word_index) + 1, output_dim=128, input_length=tamanho_shape))
modelo.add(LSTM(units=128, recurrent_dropout=0.2))
modelo.add(Dense(units=num_classes, activation="softmax"))

# Compilar o modelo
modelo.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])
modelo.summary()

# Treinar o modelo
modelo.fit(X_train, y_train, epochs=30, batch_size=32, validation_data=(X_test, y_test))

loss, accuracy = modelo.evaluate(X_test, y_test)
print(f"Loss: {loss}\nAccuracy: {accuracy}")

predictions = modelo.predict(X_test)
print(predictions)
