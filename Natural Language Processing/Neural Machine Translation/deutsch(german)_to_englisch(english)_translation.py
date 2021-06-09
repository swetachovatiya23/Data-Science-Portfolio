# -*- coding: utf-8 -*-
"""Deutsch(German) to Englisch(English) Translation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kjh4sLsLx1e-Eegse3QjH-kueJ-LSks5

#Import the libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import string
import re
from numpy import array, argmax, random, take, delete
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, LSTM, Embedding, Bidirectional, RepeatVector, TimeDistributed
from keras.preprocessing.text import Tokenizer
from keras.callbacks import ModelCheckpoint
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from keras import optimizers
import matplotlib.pyplot as plt
# % matplotlib inline
pd.set_option('display.max_colwidth', 200)

"""#Get the data
- Required steps to follow:
  1. Connect google-collab to google drive
  2. Arrange the files according to directory tree as shown in Readme.md
  3. Add the created model to the directory and use it in deployment.
"""

#read raw text file

def read_text(filename):
    # open the file
    file = open(filename, mode='rt', encoding='utf-8')
    
    # read all text
    text = file.read()
    file.close()
    return text

# split a text into sentences

def to_lines(text):
    sents = text.strip().split('\n')
    sents = [i.split('\t') for i in sents]
    
    return sents

#read the text data and convert into sentencce

data = read_text("/content/drive/MyDrive/Colab Notebooks/natural language processing/Neural Machine Translation/deu.txt")
deu_eng = to_lines(data)
deu_eng = array(deu_eng)

deu_eng

deu_eng = deu_eng[:45000,:] # using only right amount of data as per computer's computation power

"""#Text Preprocessing"""

deu_eng

deu_english = delete(deu_eng, 2, 1)

# convert to lowercase
for i in range(len(deu_eng)):
    deu_english[i,0] = deu_english[i,0].lower()
    
    deu_english[i,1] = deu_english[i,1].lower()

deu_english

# empty lists
eng_l = []
deu_l = []

# populate the lists with sentence lengths
for i in deu_english[:,0]:
    eng_l.append(len(i.split()))

for i in deu_english[:,1]:
    deu_l.append(len(i.split()))

length_df = pd.DataFrame({'eng':eng_l, 'deu':deu_l})

length_df.hist(bins = 30)
plt.show()

# build a tokenizer

def tokenization(lines):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(lines)
    return tokenizer

deu_eng[:,0]

# prepare english tokenizer
eng_tokenizer = tokenization(deu_eng[:, 0])
eng_vocab_size = len(eng_tokenizer.word_index) + 1

eng_length = 8
print('English Vocabulary Size: %d' % eng_vocab_size)

# prepare Deutch tokenizer
deu_tokenizer = tokenization(deu_eng[:, 1])
deu_vocab_size = len(deu_tokenizer.word_index) + 1

deu_length = 8
print('Deutch Vocabulary Size: %d' % deu_vocab_size)

# encode and pad sequences
def encode_sequences(tokenizer, length, lines):
    # integer encode sequences
    seq = tokenizer.texts_to_sequences(lines)
    # pad sequences with 0 values
    seq = pad_sequences(seq, maxlen=length, padding='post')
    return seq

"""#Train a model"""

from sklearn.model_selection import train_test_split
train, test = train_test_split(deu_eng, test_size=0.2, random_state = 12)


# prepare training data
trainX = encode_sequences(deu_tokenizer, deu_length, train[:, 1])
trainY = encode_sequences(eng_tokenizer, eng_length, train[:, 0])


# prepare validation data
testX = encode_sequences(deu_tokenizer, deu_length, test[:, 1])
testY = encode_sequences(eng_tokenizer, eng_length, test[:, 0])

def build_model(input_vocab,output_vocab, input_length,output_length,units):
      model = Sequential()
      model.add(Embedding(input_vocab, units, input_length=input_length, mask_zero=True))
      model.add(LSTM(units))
      model.add(RepeatVector(output_length))
      model.add(LSTM(units, return_sequences=True))
      model.add(Dense(output_vocab, activation='softmax'))
      return model

model = build_model(deu_vocab_size, eng_vocab_size, deu_length, eng_length, 512)
rms = optimizers.RMSprop(lr=0.001) # using RMSProp optimizer
model.compile(optimizer=rms, loss='sparse_categorical_crossentropy') #to use the target sequence as it is instead of one hot encoded format

#using ModelCheckpoint() to save the best model with lowest validation loss

filename = 'model.parameters'
checkpoint = ModelCheckpoint(filename, monitor='val_loss', verbose=1, save_best_only=True, mode='min')

history = model.fit(trainX, trainY.reshape(trainY.shape[0], trainY.shape[1], 1), 
          epochs=30, batch_size=512, 
          validation_split = 0.2,
          callbacks=[checkpoint], verbose=1)

#compare the training loss and the validation loss

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['train','validation'])
plt.show()

"""#Load the model and make predictions"""

model = load_model('/content/drive/MyDrive/Colab Notebooks/natural language processing/Neural Machine Translation/model_parameters')
preds = model.predict_classes(testX.reshape((testX.shape[0],testX.shape[1])))

def get_word(n, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == n:
            return word
    return None

# convert predictions into text (English)
preds_text = []
for i in pred:
    temp = []
    for j in range(len(i)):
        t = get_word(i[j], eng_tokenizer)
        if j > 0:
            if (t == get_word(i[j-1], eng_tokenizer)) or (t == None):
                temp.append('')
            else:
                temp.append(t)
             
        else:
            if(t == None):
                temp.append('')
            else:
                temp.append(t)            
        
    preds_text.append(' '.join(temp))

pred_df = pd.DataFrame({'actual' : test[:,0], 'predicted' : preds_text})

pd.set_option('display.max_colwidth', 200)

pred_df.head(15)

"""#Summary
The prediction of our model can be seen on the right column. Model has been quite good, however, some results are not appropriate. It can be improved by training more epochs.
- I will try to train using BERT to improve accuracy.
"""