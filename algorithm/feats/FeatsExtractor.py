from PIL import Image
import numpy as np
from typing import List, Tuple
from keras import applications

class FeatsExtractor:

    def __init__(self):
        # child will load model
        pass

    def get_feats(self, imgs_paths : List[str or Image]) -> List[np.ndarray]:     
        imgs_raw = []
        for img_path in imgs_paths:
                if  type(img_path) is str: # given path
                    img = Image.open(img_path)
                    img.load()
                else: # given PIL Image
                    img = img_path
                img = img.resize(self.get_tar_img_shape())
                imgs_raw.append(self.preprocess_input(np.asarray(img)))

        return self.get_feats_raw(np.array(imgs_raw))

    def get_feats_raw(self, img_array : np.ndarray) -> np.ndarray:
        "extract feats for a single image, given as a numpy array"
        raise NotImplementedError
    
    def good_img_shape(self, img_array : np.ndarray) -> bool:
        return tuple(img_array.shape[:2]) == self.get_tar_img_shape() and img_array.shape[2] == 3

    def get_tar_img_shape(self) -> Tuple[int, int]:
        raise NotImplementedError

    def preprocess_input(img_array : np.ndarray) -> np.ndarray:
        raise NotImplementedError

class VGG_FeatsExtractor(FeatsExtractor):

    TRAIN_MEAN = np.array([103.939, 116.779, 123.68])
    IMG_HEIGHT = 150
    IMG_WIDTH = 150

    def __init__(self):
        super().__init__()
        self.model = applications.VGG16(include_top=False, weights='imagenet')

    def preprocess_input(self, img_array : np.ndarray) -> np.ndarray:
        assert self.good_img_shape(img_array)
        img_mean_pixel = np.array([[VGG_FeatsExtractor.TRAIN_MEAN for x in range(img_array.shape[1])] for x in range(img_array.shape[0])])
        return img_array - img_mean_pixel

    def get_feats_raw(self, imgs_arrays : np.ndarray) -> np.ndarray:
        return [x.flatten() for x in self.model.predict(imgs_arrays)]
        

    def get_tar_img_shape(self) -> Tuple[int, int]:
        return (VGG_FeatsExtractor.IMG_WIDTH, VGG_FeatsExtractor.IMG_HEIGHT)

if __name__ == "__main__":
    print(VGG_FeatsExtractor().get_feats(['/home/itamar/Downloads/hmprod.jpeg', '/home/itamar/Downloads/hmprod.jpeg']))