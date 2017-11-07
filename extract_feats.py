import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras import applications
import sys
from os import listdir,makedirs
from os.path import join,exists
from math import ceil
from resnetimpl import get_resnet_152_without_top
def count_sample_num(dir_path):
    return len(listdir(join(dir_path, "sub_imgs")))


def bottleneck_features(dir_path, model_name = 'vgg16' ,img_width=150,img_height=150,batch_size=16):

    if model_name == 'vgg16':
        # build the VGG16 network
        model = applications.VGG16(include_top=False, weights='imagenet')
        datagen = ImageDataGenerator(rescale=1. / 255)
        img_height = 150
        img_width = 150
    elif model_name == 'resnet_152':
        model = get_resnet_152_without_top()
        datagen = ImageDataGenerator(featurewise_center = True,rescale=1.)
        datagen.mean=np.array([103.939, 116.779, 123.68],dtype=np.float32).reshape(1,1,3)
        img_height = 224
        img_width = 224
    else:
        raise Exception("model type " + str(model_name) + " is not supported")
    
    generator = datagen.flow_from_directory(
        dir_path,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    
    bottleneck_features_train = model.predict_generator(generator, 2)
    print("num of feats:" , len(bottleneck_features_train) ,",", bottleneck_features_train.shape)
    if not exists(join(dir_path,'feats')):
        makedirs(join(dir_path,'feats'))

    for name,features in zip(listdir(join(dir_path, "sub_imgs")),bottleneck_features_train):
        #print(name, features)
        np.save(open(join(dir_path, "feats", name[:name.index('.jpg')] +  '.npy'), 'wb'), features)


if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Missing path to dir")
    else:
        if len(sys.argv) >= 3:
            bottleneck_features(sys.argv[1], model_name = sys.argv[3])
        bottleneck_features(sys.argv[1])
