import imageio
import numpy as np
from typing import List, Dict
from multiprocessing import Pool

def get_image_rgb_mean_and_median(images: List[str] or List[np.ndarray], info_index = None) -> List[Dict]:
    if info_index:
        print('info index rgb utils:', info_index)
    try:
        images_arrays = [imageio.imread(img) if type(img) == type(str()) else img for img in images]
    except IOError:
        return [None for img in images]
    return [{'mean':get_img_mean(img), 'median':get_img_median(img)} for img in images_arrays]

def get_img_mean(img):
    return np.mean(img, axis=(0, 1))

def get_img_median(img):
    return np.median(img, axis=(0, 1))



if __name__ == "__main__":
    pass
