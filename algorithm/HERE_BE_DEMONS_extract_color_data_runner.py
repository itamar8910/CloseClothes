import sys
sys.path.append('..')
from algorithm.rgb_utils import get_image_rgb_mean_and_median
from multiprocessing import Pool
from database.TinyDB_DB import TinyDB_DB
import pickle

def extact_color_data():

    all_items = TinyDB_DB().get_all()

    pool = Pool(8)

    imgs_urls = [item['imgs'] for item in all_items]
    imgs_urls = imgs_urls[:2]
    img_url_to_color_data = {}
    results = pool.starmap(get_image_rgb_mean_and_median, imgs_urls)
    for res, item_imgs in zip(results, imgs_urls):
        for img_url, color_data in zip(item_imgs, res):
            img_url_to_color_data[img_url] = color_data



    with open('img_url_to_color_data.p', 'wb') as f:
        pickle.dump(img_url_to_color_data, f)

def update_with_color_feats(pickle_path = 'img_url_to_color_data.p'):
    with open(pickle_path, 'rb') as f:
        img_url_to_color_data = pickle.load(f)
    
    db = TinyDB_DB()
    imgs_urls = [item['url'] for item in db.all_items]
    for item_i, item in enumerate(db.all_items):
        print(item_i)
        rgb_median_weight = int(len(item['feats'][0]) / 2 / 3)
        item['feats'] = [
            deep_feats + img_url_to_color_data[img_url] * rgb_median_weight for  deep_feats, img_url in zip(item['feats'], item['imgs'])
        ]
    


if __name__ == "__main__":
    update_with_color_feats()