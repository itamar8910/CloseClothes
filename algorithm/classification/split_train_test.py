import os
import json
import config
from random import shuffle
from shutil import move

def copy_imgs(imgs_paths, imgs_rel_path, dst_dir):
    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)
    for img_path in imgs_paths:
        #the imgs names are not unique between directories, so we'll append the parnet directory name
        img_name = os.path.split(os.path.split(img_path)[0])[1] + "_" + os.path.split(img_path)[1]
        move(os.path.join(imgs_rel_path, img_path), os.path.join(dst_dir, img_name))

if __name__ == "__main__":
    imgs_meta_cats = json.load(open('imgs_meta_categories.json', 'r'))
    meta_cat_to_imgs = {}

    for imgdata in imgs_meta_cats:
        if imgdata['category'] not in meta_cat_to_imgs.keys():
            meta_cat_to_imgs[imgdata['category']] = []
        meta_cat_to_imgs[imgdata['category']].append(imgdata['img_path'])
    
    MAX_IMGS_PER_CAT = 15000
    # truncate large categories so all classes would have roughly the same #samples 
    for cat in meta_cat_to_imgs.keys():
        if len(meta_cat_to_imgs[cat]) > MAX_IMGS_PER_CAT:
            shuffle(meta_cat_to_imgs[cat])
            meta_cat_to_imgs[cat] = meta_cat_to_imgs[cat][:MAX_IMGS_PER_CAT]

    print([(cat, len(meta_cat_to_imgs[cat])) for cat in meta_cat_to_imgs.keys()])

    print(sum([len(meta_cat_to_imgs[cat]) for cat in meta_cat_to_imgs.keys()]))

    TRAIN_DIR = config.TRAIN_DIR
    TEST_DIR = config.TEST_DIR
    IMGS_REL_PATH = config.DEEP_FASHION
    TEST_REL_SIZE = .1
    for meta_cat in meta_cat_to_imgs.keys():
        print("Preparting data for:" , meta_cat)
        shuffle(meta_cat_to_imgs[meta_cat])
        split_index = int(len(meta_cat_to_imgs[meta_cat]) * TEST_REL_SIZE)
        train_imgs = meta_cat_to_imgs[meta_cat][split_index:]
        test_imgs = meta_cat_to_imgs[meta_cat][:split_index]
        print("Preparing train set:({})".format(len(train_imgs)))
        copy_imgs(train_imgs, IMGS_REL_PATH, os.path.join(TRAIN_DIR, meta_cat))
        print("Preparing test set:({})".format(len(test_imgs)))
        copy_imgs(test_imgs, IMGS_REL_PATH, os.path.join(TEST_DIR, meta_cat))