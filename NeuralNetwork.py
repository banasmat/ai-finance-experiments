import tensorflow as tf

class NeuralNetwork:

    def classify(self, x_train, y_train, x_test, y_test):

        n_nodes_layer_1 = 500
        n_nodes_layer_2 = 500
        n_nodes_layer_3 = 500

        n_classes = 1
        batch_size = 100

        print(x_train[0])
        quit()

        x = tf.placeholder('float', [None, ])
