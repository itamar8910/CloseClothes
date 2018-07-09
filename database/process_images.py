
from BaseDB import *
from TinyDB_DB import *
from typing import List, Dict
import requests
from os import path
import re
from slugify import slugify
from os import remove
from ..algorithm.bbox.bbox_heuristic import get_uperbody_bbox_from_npy
from PIL import Image
import numpy as np
from ..algorithm.feats.FeatsExtractor import VGG_FeatsExtractor

TMP_DIR = 'database/tmp/'
feats_extractor = VGG_FeatsExtractor()


def download_item_images(item : Dict) -> List[str]:
    "returns saved paths"
    paths = []
    for i, img_url in enumerate(item['imgs']):
        img_data = requests.get(img_url).content
        img_path = path.join(TMP_DIR, slugify(item['url']) + '_{}.jpeg'.format(i))
        with open(img_path, 'wb') as f:
            f.write(img_data)
        paths.append(img_path)
    return paths

def get_items_imgs(db):
    """
    a generator that returns imgs of items as they are downloaded
    yields: Tuple(url, List[imgs_paths])
    """
    
    items = db.get_all()
    for item in items:
        yield (item['url'], download_item_images(item))

def process_img(item_url, img_path):
    # segment upper body
    img = Image.open(img_path)
    # TODO: handle case when there is no face in the image / more than one face
    upperbody_bbox = get_uperbody_bbox_from_npy(np.array(img))
    print(upperbody_bbox)
    img_upperbody = img.crop(upperbody_bbox)
    return feats_extractor.get_feats(img_upperbody)

def remove_imgs(imgs):
    for img in imgs:
        assert img.endswith(".jpeg") or img.endswith(".jpg") or img.endswith(".png")
        remove(img)

def process_all_items(db):
    for item_url, item_imgs in get_items_imgs(db):
        print(item_url, item_imgs)
        imgs_feats = []
        for img in item_imgs:
            imgs_feats.append(process_img(item_url, img))
        db.update_feats(item_url, imgs_feats)
        remove_imgs(item_imgs)

if __name__ == "__main__":
    """
    TODO: fix imports, they are broken
    TODO: add paralelization
    """
    db = TinyDB_DB('database/dummy.json')
    process_all_items(db)