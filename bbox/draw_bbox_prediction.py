import click
import keras
import numpy as np
import cv2
from keras.models import load_model
import h5py
from PIL import Image, ImageDraw

@click.command()
@click.argument("model_path")
@click.argument("image_path")
def main(model_path,image_path):
    print(model_path)
    model = load_model(model_path) 
    image = Image.open(image_path)
    resized = cv2.resize(cv2.imread(image_path,0),(200,200))
    X= np.array([resized])
    X = X.reshape(*X.shape,1)
    resized  = (resized)/(255.0/2.0) - 1 # scale between -1, 1     resized = 
    bbox = model.predict(X)[0]
    print(bbox)
    x,y,width,height = bbox
    draw = ImageDraw.Draw(image)
    draw.rectangle(((x,y),(x+width,y+height)),outline="black")
    image.show()


if __name__ == '__main__':
    main()