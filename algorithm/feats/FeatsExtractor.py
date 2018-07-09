from typing import List, Tuple

import cv2
import imageio
import numpy as np
from keras import applications
from PIL import Image
from algorithm.bbox.bbox_heuristic import get_uperbody_bbox_from_npy
from algorithm.rgb_utils import get_image_rgb_mean_and_median


class FeatsExtractor:

    def __init__(self):
        # child will load model
        pass

    def get_feats(self, imgs_paths : List[str or np.ndarray], verbose=False) -> List[np.ndarray]:
        """
        if received str, handles downloading the image
        handles croppoing the image to upperbody
        """
        return self.get_feats_raw([self.preprocess_input(self.crop_to_upperbody(imageio.imread(img) if isinstance(img, str) else img)) for img in imgs_paths], verbose=verbose)
        # return self.get_feats_raw(self.crop_to_upperbody(np.array([imageio.imread(path) if isinstance(path,str) else path for path in imgs_paths])))

    def get_feats_raw(self, img_array : np.ndarray, verbose=False) -> np.ndarray:
        "extract feats for a single image, given as a numpy array"
        raise NotImplementedError
    
    def good_img_shape(self, img_array : np.ndarray) -> bool:
        return tuple(img_array.shape[:2]) == self.get_tar_img_shape() and img_array.shape[2] == 3

    def get_tar_img_shape(self) -> Tuple[int, int]:
        raise NotImplementedError

    def preprocess_input(self, img_array : np.ndarray) -> np.ndarray:
        raise NotImplementedError

    def crop_to_upperbody(self, img : np.ndarray) -> np.ndarray:
        # print(img.shape)
        
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

    def preprocess_input(self, img_array : np.ndarray, reverse=False) -> np.ndarray:
        img_array = cv2.resize(img_array, self.get_tar_img_shape())
        assert self.good_img_shape(img_array)
        img_mean_pixel = np.array([[VGG_FeatsExtractor.TRAIN_MEAN for x in range(img_array.shape[1])] for x in range(img_array.shape[0])])
        if not reverse:
            return img_array - img_mean_pixel
        else:
            return img_array + img_mean_pixel

    def get_feats_raw(self, imgs_arrays : np.ndarray, verbose=False) -> np.ndarray:
        # print(imgs_arrays[0].shape)
        images_deep_feats = [self.model.predict(np.array([img]))[0].flatten() for img in imgs_arrays]
        print('num of deep features:', len(images_deep_feats[0]))
        images_rgb_data = get_image_rgb_mean_and_median([self.preprocess_input(img, reverse=True) for img in imgs_arrays])
        # images_rgb_mean = [rgb_data['mean'] for rgb_data in images_rgb_data]
        images_rgb_median = [rgb_data['median'] for rgb_data in images_rgb_data]
        if verbose:
            print('median RGB:', images_rgb_median)
            Image.fromarray(imgs_arrays[0].astype('uint8'), 'RGB').show()
        rgb_median_weight = 1 # int(len(images_deep_feats[0]) / 2 / 3)
        images_color_feats = [ np.array(list(med) * rgb_median_weight, dtype=np.float32) for med in images_rgb_median]
        images_whole_feats = [np.concatenate((deep_feats, color_feats), axis=0) for deep_feats, color_feats in zip(images_deep_feats, images_color_feats)]
        return images_whole_feats

    def get_tar_img_shape(self) -> Tuple[int, int]:
        return (VGG_FeatsExtractor.IMG_WIDTH, VGG_FeatsExtractor.IMG_HEIGHT)
