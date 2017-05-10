from keras.models import Sequential
from keras.layers import Dense, SimpleRNN, LSTM, Dropout
from keras.regularizers import l2
from keras.preprocessing import sequence
from keras.datasets import imdb
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import numpy
import cPickle as pickle
import util

# fix random seed for reproducibility
numpy.random.seed(7)
seed = 7


def gen_model():
    print "generating model"
    model = Sequential()
    model.add(Dense(1939, input_dim=1939, activation='relu'))
    model.add(Dropout(.1, seed=seed))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(.1, seed=seed))
    model.add(Dense(4, activation='sigmoid'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def sense_model():
    # load pima indians dataset
    dataset = numpy.loadtxt("sense", delimiter=",")
    # split into input (X) and output (Y) variables
    labels = numpy.loadtxt("sense_labels", delimiter=",")
    model = gen_model()

    # Compile model
    # model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Fit the model
    # model.fit(dataset, labels, epochs=500, batch_size=10)
    # evaluate the model
    # scores = model.evaluate(dataset, labels)
    # print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
    # model.save("sense_deep_simple")
    estimator = KerasClassifier(build_fn=gen_model, epochs=50, batch_size=5, verbose=0)
    kfold = KFold(n_splits=10, shuffle=True, random_state=seed)
    results = cross_val_score(estimator, dataset, labels, cv=kfold)
    util.exportModel("results", results)
    return results


def sense_model_simple():
    # load pima indians dataset
    dataset = numpy.loadtxt("sense", delimiter=",")
    # split into input (X) and output (Y) variables
    labels = numpy.loadtxt("sense_labels", delimiter=",")
    model = gen_model()

    # Fit the model
    model.fit(dataset, labels, epochs=50, batch_size=5)
    # evaluate the model
    scores = model.evaluate(dataset, labels)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
    model.save("sense_deep_simple")
    # estimator = KerasClassifier(build_fn=gen_model, epochs=200, batch_size=5, verbose=0)
    # kfold = KFold(n_splits=10, shuffle=True, random_state=seed)
    # results = cross_val_score(estimator, dataset, labels, cv=kfold)
    # return results