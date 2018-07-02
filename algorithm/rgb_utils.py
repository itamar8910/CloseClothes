import imageio
import numpy as np
from typing import List, Dict

def get_image_rgb_mean_and_median(images: List[str] or List[np.ndarray]) -> List[Dict]:
    images_arrays = [imageio.imread(img) if type(img) == type(str()) else img for img in images]
    return [{'mean':get_img_mean(img), 'median':get_img_median(img)} for img in images_arrays]

def get_img_mean(img):
    return np.mean(img, axis=(0, 1))

def get_img_median(img):
    return np.median(img, axis=(0, 1))

if __name__ == "__main__":
    image_urls = ['/home/itamar/Pictures/upperbody_blue2.png', 'https://d356cpcjxoolwe.cloudfront.net/media/catalog/product/cache/3/image/373x485/72b4a3c89279b6295f5413414e9ad668/7/1/7170651.01.2200_5f90b55.jpg', 'https://d356cpcjxoolwe.cloudfront.net/media/catalog/product/cache/3/image/373x485/72b4a3c89279b6295f5413414e9ad668/7/1/7170651.01.2200_d_410c25c.jpg', 'https://d356cpcjxoolwe.cloudfront.net/media/catalog/product/cache/3/image/373x485/72b4a3c89279b6295f5413414e9ad668/7/1/7170651.01.2200_d1_f3f83f2.jpg']
    imgs_rgbs_data = get_image_rgb_mean_and_median(image_urls)
    for img_url, img_rgb_data in zip(image_urls, imgs_rgbs_data):
        print(img_url)
        print('mean:', img_rgb_data['mean'])
        print('median:', img_rgb_data['median'])
        # print('median repeated:', np.repeat(img_rgb_data['median'].reshape([, 5, axis=1))