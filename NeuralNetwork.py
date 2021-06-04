import numpy as np
from tensorflow import keras
from sklearn.utils import class_weight
from Dataprocessing import prepaireData



def prepaireModel(vocab_size,sentence_size):
	input=keras.layers.Input(shape=(sentence_size))
	inputmask=keras.layers.Input(shape=(sentence_size,1))
	x=keras.layers.Embedding(vocab_size, 64)(input)
	x=keras.layers.Multiply()([x,inputmask])
	x=keras.layers.LSTM(128,return_sequences=True,activation="tanh")(x)
	x=keras.layers.LSTM(256,return_sequences=True,activation="tanh")(x)
	x=keras.layers.LSTM(512,return_sequences=False,activation="tanh")(x)
	x=keras.layers.Flatten()(x)
	x=keras.layers.Dense(128,activation="relu")(x)
	x=keras.layers.Dense(64,activation="relu")(x)
	x=keras.layers.Dense(32,activation="relu")(x)
	x=keras.layers.Dense(16,activation="relu")(x)
	x=keras.layers.Dense(8,activation="relu")(x)
	x=keras.layers.Dense(2,activation="softmax")(x)
	model=keras.models.Model((input,inputmask),x)
	model.compile('rmsprop', keras.losses.CategoricalCrossentropy(from_logits=False),metrics=["accuracy"])
	# out=model.predict((np.random.randint(vocab_size, size=(32, sentencelen)),np.random.randint(1,3,(32,sentencelen))))
	# print(np.random.randint(vocab_size, size=(32, sentencelen)).shape,np.random.randint(1,3,(32,sentencelen,1)).shape)
	# print(out.shape)
	return model


sentencelen=50
xdata,ydata,vocab_size,masks,_=prepaireData(sentencelen)
masks+=1
model=prepaireModel(vocab_size+1,sentencelen)
YDATA=np.argmax(ydata,axis=1)
class_weights = dict(zip(np.unique(YDATA), class_weight.compute_class_weight('balanced', np.unique(YDATA),YDATA)))
class_weights[1]*=1.5
print(class_weights)
model.fit((xdata,masks),ydata,epochs=15,batch_size=64,validation_split=.2,class_weight=class_weights)
model.save("../models/MODEL.h5")
