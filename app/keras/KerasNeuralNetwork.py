import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import KFold, GridSearchCV, cross_val_score
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

class KerasNeuralNetwork:

    x_input_len = 0
    y_input_len = 1

    def predict(self, X):
        self.x_input_len = X.shape[0]

        model = self.build_model()
        model.load_weights(os.path.join(os.path.abspath(os.getcwd()), 'app', 'keras', 'forex_analyzer_model.h5'))
        prediction = model.predict(np.array([X]), 10)[0][0]
        return prediction

        # return np.round(prediction * 2) / 2

    def train(self, x_train: np.ndarray, y_train: np.ndarray, x_test: np.ndarray, y_test: np.ndarray):

        self.x_input_len = x_train.shape[1]

        # X = np.append(x_train, x_test, axis=0)
        # Y = np.append(y_train, y_test, axis=0)
        #
        # seed = 7
        # np.random.seed(seed)
        #
        # estimators = []
        # estimators.append(('standardize', StandardScaler()))
        # estimators.append(('mlp', KerasRegressor(build_fn=self.build_model, epochs=10, batch_size=5, verbose=1)))
        # pipeline = Pipeline(estimators)
        # kfold = KFold(n_splits=10, random_state=seed)
        # results = cross_val_score(pipeline, X, Y, cv=kfold, n_jobs=-1)
        # print("Larger: %.2f (%.2f) MSE" % (results.mean(), results.std()))


        estimator = KerasRegressor(build_fn=self.build_model, epochs=1, batch_size=10, verbose=1)

        parameters = {'batch_size': [32, 10],
                      'epochs': [10, 50],
                      'optimizer': ['adam', 'sgd', 'rmsprop'],
                      'loss': ['mean_squared_error', 'squared_hinge']}
        grid_search = GridSearchCV(estimator=estimator,
                                   param_grid=parameters,
                                   scoring='r2',
                                   cv=10,
                                   n_jobs=-1)
        grid_search = grid_search.fit(x_train, y_train)

        print('scores', grid_search.grid_scores_)
        print('best score', grid_search.best_score_)


        # model = self.build_model()
        # model.fit(x_train, y_train,
        #           batch_size=10,
        #           epochs=10,
        #           verbose=1,
        #           validation_split=0.1
        #           )

        # loss_and_metrics = model.evaluate(x_test, y_test, batch_size=128)
        #
        # model.save('forex_analyzer_model.h5')

        # print('model summary', model.summary())
        # print('')
        # print('accuracy', loss_and_metrics[1])

    def build_model(self, optimizer='adam', loss='mean_squared_error'):

        x_y_input_len_avg = int((self.x_input_len + self.y_input_len) / 2)

        model = Sequential()

        model.add(Dense(units=x_y_input_len_avg,
                        activation='relu',
                        kernel_initializer='uniform',
                        input_shape=(self.x_input_len,)
                        ))
        # TODO activate dropout in case of overfitting (big difference between training and testing accuracy)
        # model.add(Dropout(p=0.1))

        model.add(Dense(units=x_y_input_len_avg,
                        activation='relu',
                        kernel_initializer='uniform',
                        ))
        # model.add(Dropout(p=0.1))

        model.add(Dense(units=self.y_input_len,
                        activation='tanh',
                        kernel_initializer='uniform',
                        ))

        model.compile(loss=loss,
                      optimizer=optimizer,
                      metrics=['accuracy'])

        return model
