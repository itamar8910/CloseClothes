from resnetimpl import resnet_152_without_top
from keras import backend as K
from keras.models import Model
from keras.layers import Input, Dense, Conv2D, MaxPooling2D, AveragePooling2D, ZeroPadding2D, Flatten, Activation, add
from keras.applications.resnet50 import ResNet50
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import SGD

if __name__ == "__main__":
    print("dim ordering:", K.image_dim_ordering())
    NUM_CLASSES = 6
    INPUT_SHAPE = (224, 224, 3)
    RESNET_SIZE = 50
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
        raise Exception("Unsupported resnet size")

    TRAIN_DIR = "../../DeepFashion/clf_train/"
    TEST_DIR = "../../DeepFashion/clf_test/"

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