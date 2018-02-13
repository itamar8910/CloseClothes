import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras import applications
import os 
from math import ceil
from keras.utils import to_categorical
from keras import optimizers
from keras import Model
from keras.callbacks import ModelCheckpoint


def count_samples(path):
    return sum([len(os.listdir(os.path.join(path, d))) for d in os.listdir(path)])


#classify with feature layers frozen

def train(train_data_dir, validation_data_dir, save_path = 'tmp_save',NUM_CLASSES = 6, img_width = 150, img_height = 150, batch_size=16, epochs = 5):
    nb_train_samples = count_samples(train_data_dir)
    nb_validation_samples = count_samples(validation_data_dir)
     # build the VGG16 network
    base_model = applications.VGG16(weights='imagenet', include_top=False, input_shape=(img_width, img_height, 3))
    print('Model loaded.')

    # build a classifier model to put on top of the convolutional model
    top_model = Sequential()
    top_model.add(Flatten(input_shape=base_model.output_shape[1:]))
    top_model.add(Dense(256, activation='relu'))
    top_model.add(Dropout(0.5))
    top_model.add(Dense(NUM_CLASSES, activation='sigmoid'))

    # note that it is necessary to start with a fully-trained
    # classifier, including the top classifier,
    # in order to successfully do fine-tuning
    #top_model.load_weights(top_model_weights_path)

    # add the model on top of the convolutional base
    #model.add(top_model)
    model = Model(input= base_model.input, output= top_model(base_model.output))
    # set the first 25 layers (up to the last conv block)
    # to non-trainable (weights will not be updated)
    print(len(model.layers))
    for layer in model.layers[:19]:
        layer.trainable = False

    # compile the model with a SGD/momentum optimizer
    # and a very slow learning rate.
    model.compile(loss='categorical_crossentropy',
                optimizer=optimizers.SGD(lr=1e-4, momentum=0.9),
                metrics=['accuracy'])
    model.summary()
    
    # prepare data augmentation configuration
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

    test_datagen = ImageDataGenerator(rescale=1. / 255)

    train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='categorical')

    validation_generator = test_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='categorical')

    steps_per_epoch_train = nb_train_samples/batch_size
    steps_per_epoch_val = nb_validation_samples/batch_size

    # fine-tune the model
     #only save model checkpoint when accuracy is at a maximum
    checkpoint = ModelCheckpoint(save_path, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    callbacks_list = [checkpoint]
    model.fit_generator(
        train_generator,
    steps_per_epoch=steps_per_epoch_train,
        epochs=epochs,
        validation_data=validation_generator,
    validation_steps=steps_per_epoch_val,
    callbacks=callbacks_list)


if __name__ == "__main__":
    train(train_data_dir="../DeepFashion/clf_train_dummy/", validation_data_dir="../DeepFashion/clf_test_dummy/")