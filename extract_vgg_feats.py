
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras import applications
import sys
from os import listdir,makedirs
from os.path import join,exists

def count_sample_num(dir_path):
    return len(listdir(dir_path))


def bottleneck_features(dir_path, img_width=150,img_height=150,batch_size=16):
    datagen = ImageDataGenerator(rescale=1. / 255)

    # build the VGG16 network
    model = applications.VGG16(include_top=False, weights='imagenet')

    generator = datagen.flow_from_directory(
        dir_path,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    bottleneck_features_train = model.predict_generator(generator,count_sample_num(dir_path) // batch_size)

    if not exists('feats'):
        makedirs('feats')

    for name,features in zip(listdir(dir_path),bottleneck_features_train):
        np.save(open(join("feats",name[:name.index('.')], '.npy'), 'w'))

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Missing path to dir")
    else:
        bottleneck_features(sys.argv[1])
