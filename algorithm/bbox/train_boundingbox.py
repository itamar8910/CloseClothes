

import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import SGD
import json
import cv2
from os import listdir
from os.path import join, dirname, realpath
from PIL import Image, ImageDraw
import time
import pickle

def draw_bbox(img_array, x, y, width, height):
    pil_img = Image.fromarray(img_array)

    draw = ImageDraw.Draw(pil_img)
    draw.rectangle(((x, y), (x + width, y + height)), outline="black")

    pil_img.show()

def prep_image_and_bbox(img,input_shape):
    """
    preprocess image for bbox training resizes it and scales it between -1,1
    returns the resized image and its resize scalse
    """
    orig_shape = img.shape
    resized = cv2.resize(img, input_shape)
    scale = np.array([x/float(y) for x, y in zip(input_shape , orig_shape)])
    resized  = (resized)/(255.0/2.0) - 1 # scale between -1, 1 
    return resized,scale
    
    
def gen_XY_data(bbox_json_path, input_shape, rel_img_path, MAX_SAMPLES = None,verbose = False):
    bbox_json = json.load(open(bbox_json_path, 'r'))
    if MAX_SAMPLES is None:
        MAX_SAMPLES = len(bbox_json)
    X = [] # x.shape = (num_imgs, inputshape[0], inputshape[1])
    Y = [] # y.shape = (num_imgs, 4) y[i] = (x,y,w,h)
    verbose_steps = 100
    start_time = time.time()
    print("Extracting X, Y data")
    for index,img_data in enumerate(bbox_json[:MAX_SAMPLES]):
        if verbose and index % verbose_steps == 1:
            delta_t = time.time() - start_time
            time_per_step = delta_t / float(index)
            time_left = (min(len(bbox_json), MAX_SAMPLES) - index) * time_per_step
           # print('time left:{0:.1f} s'.format(time_left))
            print('progress: {0:.1f}%, time left: {1:.1f}s'.format(index/float(min(len(bbox_json), MAX_SAMPLES))*100.0, time_left))
        print("reading image from path:" , join(rel_img_path, img_data['image_path']))
        img = cv2.imread(join(rel_img_path, img_data['image_path']), 0)
        resized,scale = prep_image(img,input_shape)
        rect = img_data['rects'][0]
        x = float(rect['x1'])
        y = float(rect['y1'])
        width = float(rect['x2'] - rect['x1'])
        height = float(rect['y2'] - rect['y1'])

        #draw_bbox(img, x, y, width, height)

        x *= scale[1]
        width *= scale[1]
        y *= scale[0]
        height *= scale[0]
        bbox = np.array([x,y,width,height])
        
        resized  = (resized)/(255.0/2.0) - 1 # scale between -1, 1 
        bbox = np.array([x/float(input_shape[1]), # scale between 0, 1
                         y/float(input_shape[0]),
                         width/float(input_shape[1]), 
                         height/float(input_shape[0])])
        

        #draw_bbox(resized, x, y, width, height)

        X.append(resized)
        Y.append(bbox)

    return np.array(X), np.array(Y)

def save_model(model, base_name = "a_model", models_save_path = "utils/saved_models"):
    # todo: test this function
    # saved models are named 'base_name_<index>'
    # todo: check if model_save_path is a directory, if not create it
    same_base_names = [x for x in listdir(models_save_path) if base_name in x]
    if len(same_base_names) == 0:   
        max_index = -1
    else:
        max_index = max([int(x[x.rfind("_")+1:x.rfind(".")]) if x.rfind("_") != -1 else -1 for x in same_base_names])
    max_index += 1
    model.save(join(models_save_path, base_name + "_" + str(max_index) + ".h5"))

if __name__ == "__main__":
    # Generate dummy data
    input_shape = (200, 200)

    GENERATE_DATA = True
    if GENERATE_DATA:
        X, Y = gen_XY_data('bb_test_unresized.json', input_shape, join(dirname(realpath(__file__)), "../Data/Img/"), MAX_SAMPLES = 2,verbose = True)
        print(X.shape, Y.shape)
    X = X.reshape(*X.shape, 1)
    #Y = Y.reshape(*Y.shape, 1)
    print(X.shape, Y.shape)

    # partition dummy data
    split_index = int(X.shape[0] * float(0.7))
    x_train, y_train = X[:split_index], Y[:split_index]
    x_test, y_test = X[split_index:], Y[split_index:]

    print("train x,y shapes:" , x_train.shape, y_train.shape)
    print("test x,y shapes:", x_test.shape, y_test.shape)

    model = Sequential()
    # input: 100x100 images with 3 channels -> (100, 100, 3) tensors.
    # this applies 32 convolution filters of size 3x3 each.
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=X.shape[1:]))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(4, activation='softmax'))

    model.summary()

    model.compile(loss='mse', optimizer='adam')

    model.fit(x_train, y_train, batch_size=32, epochs=2)
    score_train = model.evaluate(x_train, y_train, batch_size=32)
    score_test = model.evaluate(x_test, y_test, batch_size=32)
    print(score_train)
    print(score_test)
    save_model(model, "dummy_model")
    #model.save('save_model_{}.h5'.format(str(time.time())))
