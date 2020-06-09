import tensorflow as tf
import json

mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test,y_test) = mnist.load_data()
x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(30,activation=tf.nn.sigmoid))
model.add(tf.keras.layers.Dense(30,activation=tf.nn.sigmoid))
model.add(tf.keras.layers.Dense(10,activation=tf.nn.sigmoid))
model.add(tf.keras.layers.Dense(10,activation=tf.nn.sigmoid))

model.compile(optimizer='adam',
             loss='sparse_categorical_crossentropy',
             metrics=['accuracy'])
model.fit(x_train,y_train,epochs=20)
(val_loss,val_accuracy) = model.evaluate(x_test,y_test)

weightList = []
biasList = []
for i in range(1,len(model.layers)):
    weights = model.layers[i].get_weights()[0]
    weightList.append((weights.T).tolist())
    bias = [[float(b)] for b in model.layers[i].get_weights()[1]]
    biasList.append(bias)

data = {"weights": weightList,"biases":biasList}
f = open('weightsandbiases.txt', "w")
json.dump(data, f)
f.close()