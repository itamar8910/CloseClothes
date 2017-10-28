from keras_resnet.resnet import *
import numpy as np
import cv2
from os import listdir
from os.path import join
np.random.seed(1337)

def load_data(dir_path, size):
    x = []
    for f in listdir(dir_path):
        im = cv2.imread(join(dir_path, f))
        x.append(cv2.resize(im, size))
    return np.array(x)

if __name__ == "__main__":
    x_cats = load_data("data/cats", (64,64))
    x_dogs = load_data("data/dogs", (64,64))
    X = np.concatenate((x_cats, x_dogs))
    Y = np.array([0 for x in x_cats] + [1 for x in x_dogs])

    input_shape = (3, 64, 64)
    num_outputs = 1
    resnet18 = ResnetBuilder.build_resnet_18(input_shape, num_outputs)
    resnet18.compile(loss="binary_crossentropy", optimizer="adam")
    #NUM = 100

    # x = np.random.rand(100, 64, 64, 3)
    # y = np.random.rand(NUM, num_outputs)
    print("starts training")
    resnet18.fit(X, Y, epochs=10, batch_size=32, shuffle=True)
    print("done")
