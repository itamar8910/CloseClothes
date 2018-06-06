import numpy as np
from typing import List, Tuple
from keras import applications
import imageio
from PIL.Image import Image
from algorithm.bbox.bbox_heuristic import get_uperbody_bbox_from_npy
import cv2


class FeatsExtractor:

    def __init__(self):
        # child will load model
        pass

    def get_feats(self, imgs_paths : List[str or np.ndarray]) -> List[np.ndarray]:
        """
        if received str, handles downloading the image
        handles croppoing the image to upperbody
        """
        return self.get_feats_raw([self.preprocess_input(self.crop_to_upperbody(imageio.imread(img) if isinstance(img, str) else img)) for img in imgs_paths])
        # return self.get_feats_raw(self.crop_to_upperbody(np.array([imageio.imread(path) if isinstance(path,str) else path for path in imgs_paths])))

    def get_feats_raw(self, img_array : np.ndarray) -> np.ndarray:
        "extract feats for a single image, given as a numpy array"
        raise NotImplementedError
    
    def good_img_shape(self, img_array : np.ndarray) -> bool:
        return tuple(img_array.shape[:2]) == self.get_tar_img_shape() and img_array.shape[2] == 3

    def get_tar_img_shape(self) -> Tuple[int, int]:
        raise NotImplementedError

    def preprocess_input(self, img_array : np.ndarray) -> np.ndarray:
        raise NotImplementedError

    def crop_to_upperbody(self, img : np.ndarray) -> np.ndarray:
        print(img.shape)
        
        upperbody_bbox = [None, None, None, None]
        try:
            upperbody_bbox = get_uperbody_bbox_from_npy(img)  # x, y, w, h
        except Exception as e:  # could not find upperbody
            print('NO FACES DETECTED, cropping from center instead')
            # TODO: bug in here, img.shape 
            img_height, img_width, _ = img.shape
            center_crop_offset = 0.2
            upperbody_bbox = [center_crop_offset * img_width, center_crop_offset * img_height, (1-center_crop_offset*2) * img_width, (1-center_crop_offset*2) * img_height]
        x, y, w, h = [int(x) for x in upperbody_bbox]
        
        upperboy_img = img[y : y + h, x : x + w]
 
        return upperboy_img


class VGG_FeatsExtractor(FeatsExtractor):

    TRAIN_MEAN = np.array([103.939, 116.779, 123.68])
    IMG_HEIGHT = 150
    IMG_WIDTH = 150

    def __init__(self):
        super().__init__()
        self.model = applications.VGG16(include_top=False, weights='imagenet')

    def preprocess_input(self, img_array : np.ndarray) -> np.ndarray:
        img_array = cv2.resize(img_array, self.get_tar_img_shape())
        assert self.good_img_shape(img_array)
        img_mean_pixel = np.array([[VGG_FeatsExtractor.TRAIN_MEAN for x in range(img_array.shape[1])] for x in range(img_array.shape[0])])
        return img_array - img_mean_pixel

    def get_feats_raw(self, imgs_arrays : np.ndarray) -> np.ndarray:
       
        return [self.model.predict(np.array([img]))[0].flatten() for img in imgs_arrays]

    def get_tar_img_shape(self) -> Tuple[int, int]:
        return (VGG_FeatsExtractor.IMG_WIDTH, VGG_FeatsExtractor.IMG_HEIGHT)

