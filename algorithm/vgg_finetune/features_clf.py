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
def count_samples(path):
    return sum([len(os.listdir(os.path.join(path, d))) for d in os.listdir(path)])

# dimensions of our images.
img_width, img_height = 150, 150
batch_size = 16
NUM_CLASSES = 6
top_model_weights_path = 'bottleneck_fc_model_dummy.h5'
train_data_dir = '../../DeepFashion/clf_train_dummy/'
validation_data_dir = '../../DeepFashion/clf_test_dummy/'
nb_train_samples = count_samples(train_data_dir)
nb_validation_samples = count_samples(validation_data_dir)
print("# samples train:" , nb_train_samples)
print("# samples validation:" , nb_validation_samples)



def save_bottlebeck_features():

    #datagen = ImageDataGenerator(rescale=1./255.0)
    datagen = ImageDataGenerator(rescale=1., featurewise_center=True)
    datagen.mean=np.array([103.939, 116.779, 123.68],dtype=np.float32).reshape(1,1,3)

    # build the VGG16 network
    model = applications.VGG16(include_top=False, weights='imagenet')

    generator = datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    bottleneck_features_train = model.predict_generator(
        generator, int(ceil(nb_train_samples / batch_size)))

    print(len(bottleneck_features_train))

    np.save(open('bottleneck_features_train_dummy.npy', 'wb'),
            bottleneck_features_train)

    np.save(open('classes_train_dummy.npy', 'wb'),
            generator.classes)

    generator = datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    
    bottleneck_features_validation = model.predict_generator(
        generator, int(ceil(nb_validation_samples / batch_size)))
    np.save(open('bottleneck_features_validation_dummy.npy', 'wb'),
            bottleneck_features_validation)
    np.save(open('classes_validation_dummy.npy', 'wb'),
            generator.classes)

def train_top_model():
    train_data = np.load(open('bottleneck_features_train_dummy.npy', 'rb'))
    train_labels = np.load(open('classes_train_dummy.npy', 'rb'))

    validation_data = np.load(open('bottleneck_features_validation_dummy.npy', 'rb'))
    validation_labels = np.load(open('classes_validation_dummy.npy', 'rb'))

    # convert labels to one-hot encoding
  

    train_labels = to_categorical(train_labels)
    validation_labels = to_categorical(validation_labels)

    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(NUM_CLASSES, activation='sigmoid'))

    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy', metrics=['accuracy'])

    epochs = 50

    model.fit(train_data, train_labels,
              epochs=epochs,
              batch_size=batch_size,
              validation_data=(validation_data, validation_labels))
    model.save_weights(top_model_weights_path)

def finetune_vgg16():

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
    top_model.load_weights(top_model_weights_path)

    # add the model on top of the convolutional base
    #model.add(top_model)
    model = Model(input= base_model.input, output= top_model(base_model.output))
    # set the first 25 layers (up to the last conv block)
    # to non-trainable (weights will not be updated)
    for layer in model.layers[:25]:
        layer.trainable = False

    # compile the model with a SGD/momentum optimizer
    # and a very slow learning rate.
    model.compile(loss='categorical_crossentropy',
                optimizer=optimizers.SGD(lr=1e-4, momentum=0.9),
                metrics=['accuracy'])

    # prepare data augmentation configuration
    
    # train_datagen = ImageDataGenerator(
    # rescale=1. / 255,
    # shear_range=0.2,
    # zoom_range=0.2,
    # horizontal_flip=True)

    train_datagen = ImageDataGenerator(
    rescale=1., 
    featurewise_center=True,
    horizontal_flip=True)

    #test_datagen = ImageDataGenerator(rescale=1. / 255)
    test_datagen = ImageDataGenerator(rescale=1., 
    featurewise_center=True)

    train_datagen.mean=np.array([103.939, 116.779, 123.68],dtype=np.float32).reshape(1,1,3)
    test_datagen.mean=np.array([103.939, 116.779, 123.68],dtype=np.float32).reshape(1,1,3)


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
    epochs = 50
    steps_per_epoch_train = nb_train_samples/batch_size
    steps_per_epoch_val = nb_validation_samples/batch_size
    # fine-tune the model
    model.fit_generator(
    train_generator,
    #samples_per_epoch=nb_train_samples,
    steps_per_epoch=steps_per_epoch_train,
    epochs=epochs,
    validation_data=validation_generator,
    #nb_val_samples=nb_validation_samples
    validation_steps=steps_per_epoch_val)

if __name__ == "__main__":
    #save_bottlebeck_features()
    #train_top_model()
    finetune_vgg16()