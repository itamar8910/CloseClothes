import os
import json
import config
from resnetimpl import resnet_152_without_top
from keras import backend as K
from keras.models import Model
from keras.layers import Input, Dense, Conv2D, MaxPooling2D, AveragePooling2D, ZeroPadding2D, Flatten, Activation, add
from keras.applications.resnet50 import ResNet50
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import SGD
from keras.callbacks import ModelCheckpoint
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import os
import numpy as np
import h5py

def get_X_Y(DIR_PATH, tar_size):
    "returns (X,Y)"
    X = []
    Y = []
    class_to_index = {name:index for index, name in enumerate(os.listdir(DIR_PATH))}
    

    for p_dir in os.listdir(DIR_PATH):
        #print(p_dir)
        y_vec = np.array([0 if i != class_to_index[p_dir] else 1 for i in range(len(class_to_index))])
        #print(y_vec)
        for f in os.listdir(os.path.join(DIR_PATH, p_dir)):
           # print(f)
            img = load_img(os.path.join(DIR_PATH, p_dir, f), target_size=tar_size)
            img_arr = img_to_array(img)
            X.append(img_arr)
            Y.append(y_vec)

    return np.array(X), np.array(Y)

def get_data_mean_std(DIR_PATH, tar_size):
    X, Y =get_X_Y(DIR_PATH, tar_size)

    return np.mean(X, axis = (0,1,2)), np.std(X, axis = (0,1,2))

if __name__ == "__main__":

    print("dim ordering:", K.image_dim_ordering())
    NUM_CLASSES = 6
    INPUT_SHAPE = (224, 224, 3)
    RESNET_SIZE = 152
    if RESNET_SIZE == 152: # note: this size is currently not working
        model = resnet152_model(weights_path = None, num_classes = NUM_CLASSES)
        sgd = SGD(lr=1e-2, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])
        model.summary()
    elif RESNET_SIZE == 50:
        model = ResNet50(include_top=True, weights=None, classes=NUM_CLASSES)
        sgd = SGD(lr=1e-2, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])
        model.summary()
    else:
        raise Exception("Unsupported resnet size")


    LOAD_WEIGHTS = False
    filepath="weights_checkpoint_resnet152_1.hdf5"
    if LOAD_WEIGHTS:
        print("loading pre-trained weights from:" , filepath)
        model = load_model(filepath)


    filepath="weights_checkpoint_resnet152_1.hdf5"
    model_json = model.to_json()
    with open(os.join(__file__.__dir__,'clf_model.json','w')) as file:
        json.dump(model_json,file)
    print("Saved clf model")
    TRAIN_DIR = config.TRAIN_DIR
    TEST_DIR = config.TEST_DIR    

    train_datagen = ImageDataGenerator(
        featurewise_std_normalization=True,
        featurewise_center=True,
        horizontal_flip=True)

    test_datagen = ImageDataGenerator( featurewise_center=True,
        horizontal_flip=True)   

    #TODO: compare with the values provided in the DeepShopping blog
    #calcaulte global mean, std
    X, Y = get_X_Y(TRAIN_DIR, INPUT_SHAPE[:2])
    train_datagen.fit(X)
    
    train_mean = train_datagen.mean
    train_std = train_datagen.std
    
    #apply them to the data generators
    train_datagen.mean = train_mean
    train_datagen.std = train_std
    test_datagen.mean = train_mean
    test_datagen.std = train_std

    train_generator = train_datagen.flow_from_directory(
            TRAIN_DIR,
            target_size= INPUT_SHAPE[:2],
            batch_size=32,
            class_mode='categorical')

    validation_generator = test_datagen.flow_from_directory(
            TEST_DIR,
            target_size= INPUT_SHAPE[:2],
            batch_size=32,
            class_mode='categorical')

    ONLY_EVAL = False
    if ONLY_EVAL:
        print(model.evaluate_generator(validation_generator, steps=800))
        exit()


    #only save model checkpoint when accuracy is at a maximum
    checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    callbacks_list = [checkpoint]

    print("fitting")
    
    model.fit_generator(
            train_generator,
            steps_per_epoch=2000,
            epochs=50,
            validation_data=validation_generator,
            validation_steps=800) # TODO: add callbacks to save checkpoints
