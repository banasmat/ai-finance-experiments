import tensorflow as tf
import numpy as np


class NeuralNetwork:

    features_n = 0
    classes_n = 0

    def train(self, x_train: np.ndarray, y_train: np.ndarray, x_test: np.ndarray, y_test: np.ndarray):

        self.features_n = len(x_train[0])
        self.classes_n = y_train.shape[1]

        x = tf.placeholder('float', [None, self.features_n])
        y = tf.placeholder('float')

        prediction = self.build_model(x)
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
        optimizer = tf.train.AdamOptimizer().minimize(cost)

        how_many_epochs = 10

        sess = tf.InteractiveSession()

        # sess = tf_debug.LocalCLIDebugWrapperSession(sess)
        # sess.add_tensor_filter("has_inf_or_nan", tf_debug.has_inf_or_nan)

        sess.run(tf.global_variables_initializer())

        x_train_len = len(x_train)
        pointer = 0
        batch_size = 100

        for epoch in range(how_many_epochs):
            epoch_loss = 0
            for _ in range(int(x_train_len / batch_size)):
                epoch_x = x_train[:pointer]
                epoch_y = y_train[:pointer]
                pointer += batch_size
                _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
                epoch_loss += c
            print('Epoch', epoch, 'completed out of', how_many_epochs, 'loss:', epoch_loss)

        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))

        accuracy = tf.reduce_mean(tf.cast(correct, dtype=tf.float32))
        print('Accuracy:', accuracy.eval({x: x_test, y: y_test}))

    def build_model(self, data):

        n_nodes_layer_1 = 500
        n_nodes_layer_2 = 500
        n_nodes_layer_3 = 500

        hidden_1_layer = {'weights': tf.Variable(tf.random_normal([self.features_n, n_nodes_layer_1])),
                          'biases': tf.Variable(tf.random_normal([n_nodes_layer_1]))}

        hidden_2_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_layer_1, n_nodes_layer_2])),
                          'biases': tf.Variable(tf.random_normal([n_nodes_layer_2]))}

        hidden_3_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_layer_2, n_nodes_layer_3])),
                          'biases': tf.Variable(tf.random_normal([n_nodes_layer_3]))}

        output_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_layer_3, self.classes_n])),
                        'biases': tf.Variable(tf.random_normal([self.classes_n]))}

        # (input_data * weights) + biases

        layer_1 = tf.add(tf.matmul(data, hidden_1_layer['weights']), hidden_1_layer['biases'])
        layer_1 = tf.nn.relu(layer_1)

        layer_2 = tf.add(tf.matmul(layer_1, hidden_2_layer['weights']), hidden_2_layer['biases'])
        layer_2 = tf.nn.relu(layer_2)

        layer_3 = tf.add(tf.matmul(layer_2, hidden_3_layer['weights']), hidden_3_layer['biases'])
        layer_3 = tf.nn.relu(layer_3)

        output = tf.add(tf.matmul(layer_3, output_layer['weights']), output_layer['biases'])

        return output
