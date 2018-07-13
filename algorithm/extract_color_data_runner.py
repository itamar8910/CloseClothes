import sys
sys.path.append('..')
from algorithm.rgb_utils import get_image_rgb_mean_and_median
from multiprocessing import Pool
from database.TinyDB_DB import TinyDB_DB
import pickle
import numpy as np
import json


def extract_color_data():
    all_items = TinyDB_DB().get_all()
    print('num of items:', len(all_items))
    pool = Pool(8)

    imgs_urls = [item['imgs'] for item in all_items]
    imgs_urls = imgs_urls
    img_url_to_color_data = {}
    results = pool.starmap(get_image_rgb_mean_and_median, [(x, x_i) for x_i, x in enumerate(imgs_urls)])
    for res, item_imgs in zip(results, imgs_urls):
        for img_url, color_data in zip(item_imgs, res):
            img_url_to_color_data[img_url] = color_data

    with open('img_url_to_color_data.p', 'wb') as f:
        pickle.dump(img_url_to_color_data, f)

def insert_into_feats(color_data_pickle_path = 'img_url_to_color_data.p'):
    with open(color_data_pickle_path,  'rb') as f:
        img_url_to_color_data = pickle.load(f)
    
    # db = TinyDB_DB()
    with open('database/data/items_tinydb.json', 'r') as f:
        tinydb_data = json.load(f)
    clothes_data = tinydb_data['_default']
    # print(db.all_items)
    # exit()
    from tqdm import tqdm
    for item_i, item in tqdm(clothes_data.items()):
        # print
        rgb_median_weight = int(len(item['feats'][0]) / 2 / 3)
               
        new_feats = [
            deep_feats + list(color_data['median']) * rgb_median_weight for color_data, deep_feats in zip([img_url_to_color_data[url] for url in item['imgs']], item['feats'])
        ]
        
        item['feats'] = new_feats
        # print(item['feats'])
    with open('database/data/items_tinydb.json', 'w') as f:
        json.dump(tinydb_data, f)

if __name__ == "__main__":
    insert_into_feats()