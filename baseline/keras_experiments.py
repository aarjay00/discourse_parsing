from keras.models import Sequential
from keras.layers import Dense
import numpy
# fix random seed for reproducibility
numpy.random.seed(7)
def trial_model():
    # load pima indians dataset
    dataset = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
    # split into input (X) and output (Y) variables
    X = dataset[:,0:8]
    Y = dataset[:,8]

    # create model
    model = Sequential()
    model.add(Dense(12, input_dim=8, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(4, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    # Fit the model
    model.fit(X, Y, epochs=500, batch_size=10)
    # evaluate the model
    scores = model.evaluate(X, Y)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))


def connective_model():
    # load pima indians dataset
    dataset = numpy.loadtxt("connective-features.csv", delimiter=",")
    # split into input (X) and output (Y) variables
    X = dataset[:, 0:286]
    Y = dataset[:, 286]

    # create model
    model = Sequential()
    model.add(Dense(512, input_dim=286, activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(8,activation="relu"))
    model.add(Dense(1, activation='sigmoid'))

    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    # Fit the model
    model.fit(X, Y, epochs=500, batch_size=10)
    # evaluate the model
    scores = model.evaluate(X, Y)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
    model.save("connective_deep_4")

def connective_rnn():
    # load pima indians dataset
    dataset = numpy.loadtxt("connective-features.csv", delimiter=",")
    # split into input (X) and output (Y) variables
    X = dataset[:, 0:286]
    Y = dataset[:, 286]

    # create model
    model = Sequential()
    model.add(Dense(1024, input_dim=286, activation='relu'))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    # Fit the model
    model.fit(X, Y, epochs=200, batch_size=10)
    # evaluate the model
    scores = model.evaluate(X, Y)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
    model.save("connective_rnn")

connective_model()
