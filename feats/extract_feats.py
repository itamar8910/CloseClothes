import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras import applications
import keras
import json
import sys
from os import listdir,makedirs
from os.path import join,exists
from math import ceil
from resnetimpl import get_resnet_152_without_top
import click

def count_sample_num(dir_path):
    return len(listdir(join(dir_path, "sub_imgs")))

@click.command()
@click.argument("dir_path")
@click.argument("model_name")
@click.option("-w","--weights",help='Custom Model hdf5 weight file')
@click.option("-n","--name",help='Feature folder name',default=None)
def main(dir_path, weights,name, model_name = 'vgg16',img_width=150,img_height=150,batch_size=16):
    bottleneck_features(dir_path, weights,name, model_name = 'vgg16',img_width=150,img_height=150,batch_size=16)

def bottleneck_features(dir_path, weights,name, model_name = 'vgg16',img_width=150,img_height=150,batch_size=16):

    if model_name == 'vgg16':
        # build the VGG16 network
        model = applications.VGG16(include_top=False, weights='imagenet')
        datagen = ImageDataGenerator(rescale=1. / 255)
        img_height = 150
        img_width = 150
    elif model_name == 'resnet_152':
        # model = get_resnet_152_without_top()
        datagen = ImageDataGenerator(featurewise_center = True,rescale=1.)
        datagen.mean=np.array([103.939, 116.779, 123.68],dtype=np.float32).reshape(1,1,3)
        img_height = 224
        img_width = 224
    else:
        with open(model_name) as json_file:
            model_json = json.load(json_file)
            model = keras.models.model_from_json(model_json)
        model.load_weights(weights)
        datagen = ImageDataGenerator()
        img_height = 224#TODO:change according to model given
        img_width = 224
    print(dir_path)
    generator = datagen.flow_from_directory(
        dir_path,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        save_format='jpg',
        class_mode=None,
        shuffle=False)

    bottleneck_features_train = model.predict_generator(generator, 2)
    print("num of feats:" , len(bottleneck_features_train) ,",", bottleneck_features_train.shape)
    if name:
        feat_dir = join(dir_path,name)
    else:
        feat_dir = join(dir_path,model_name + "-feats")
    try:
        makedirs(feat_dir)
    except OSError:
        pass
    '''
    print(generator.class_indices)
    print(generator.classes)
    print(generator.filenames)
    print([x for x in listdir(join(dir_path, "sub_imgs"))])
    '''
    for fname,features in zip(generator.filenames, bottleneck_features_train):
        #print(name, features)
        print(fname)
        name = fname[fname.index('/')+1:fname.index('.jpg')]
        np.save(open(join(feat_dir, name +  '.npy'), 'wb'), features)


if __name__ == "__main__":
    bottleneck_features()