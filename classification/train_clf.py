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
from keras import backend as K
import tensorflow as tf
import functools
def _center_loss_func(features, labels, alpha, num_classes):
    feature_dim = features.get_shape()[1]
    # Each output layer use one independed center: scope/centers
    centers = K.zeros([num_classes, feature_dim])
    labels = K.reshape(labels, [-1])
    labels = tf.to_int32(labels)
    centers_batch = tf.gather(centers, labels)
    diff = (1 - alpha) * (centers_batch - features)
    centers = tf.scatter_sub(centers, labels, diff)
    loss = tf.reduce_mean(K.square(features - centers_batch))
    return loss

def get_center_loss(alpha, num_classes):
    """Center loss based on the paper "A Discriminative 
       Feature Learning Approach for Deep Face Recognition"
       (http://ydwen.github.io/papers/WenECCV16.pdf)
    """
    @functools.wraps(_center_loss_func)
    def center_loss(y_true, y_pred):
        return _center_loss_func(y_pred, y_true, alpha, num_classes)
    return center_loss

if __name__ == "__main__":
    print("dim ordering:", K.image_dim_ordering())
    NUM_CLASSES = 6
    INPUT_SHAPE = (224, 224, 3)
    RESNET_SIZE = "centerloss"
    if RESNET_SIZE == 152: # note: this size is currently not working
        initial_model = resnet_152_without_top()
        last = initial_model.output

        x = Flatten()(last)
        preds = Dense(NUM_CLASSES, activation='softmax')(x)

        model = Model(initial_model.input, preds)
        model.summary()
    elif RESNET_SIZE == 50:
        model = ResNet50(include_top=True, weights=None, classes=NUM_CLASSES)
        sgd = SGD(lr=1e-2, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])
        model.summary()
    else:
        model = ResNet50(include_top=True, weights=None, classes=NUM_CLASSES)
        sgd = SGD(lr=1e-2, decay=1e-6, momentum=0.9, nesterov=True)
        center_loss = get_center_loss(0.5,NUM_CLASSES)
        model.compile(optimizer='sgd',loss = center_loss)
        model.summary()

    model_json = model.to_json()
    with open(os.join(__file__.__dir__,'clf_model.json','w') as file:
        json.dump(model_json,file)
    print("Saved clf model")
    TRAIN_DIR = config.TRAIN_DIR
    TEST_DIR = config.TEST_DIR    

    train_datagen = ImageDataGenerator(
        rescale=1./255,
        horizontal_flip=True)

    test_datagen = ImageDataGenerator(rescale=1./255)

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

    print("fitting")
    
    model.fit_generator(
            train_generator,
            steps_per_epoch=2000,
            epochs=50,
            validation_data=validation_generator,
            validation_steps=800)
