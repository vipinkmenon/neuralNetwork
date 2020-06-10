import mnist_loader
import network2
import json

training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
net = network2.Network([784, 30, 20, 10])#change the number of layers or number of neurons in each layer here
validation_data = list(validation_data)
training_data = list(training_data)
net.SGD(training_data, 30, 10, 0.1, lmbda=5.0,evaluation_data=validation_data, monitor_evaluation_accuracy=True)
net.save("WeigntsAndBiases.txt")