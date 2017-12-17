import os
import json

if __name__ == "__main__":
    META_CATS = {'Jacket': {'Anorak', 'Bomber', 'Jacket', 'Paraka'},
                'Cardigan': {'Cardigan'},
                'Sweater': {'Sweater'},
                'Tank': {'Tank'},
                'Blouse': {'Blouse'},
                'Tee': {'Tee'}}
                

    imgs_metacats = []

    imgs_cats = json.load(open('imgs_categories.json','r'))
    meta_cat_count = {cat:0 for cat in META_CATS.keys()}
    for imgdata in imgs_cats:
        for metacat in META_CATS.keys():
            if imgdata['category'] in META_CATS[metacat]:
                imgs_metacats.append({'img_path':imgdata['img_path'], 'category':metacat})
                meta_cat_count[metacat] = meta_cat_count[metacat] + 1
                break

    print meta_cat_count
    
    json.dump(imgs_metacats, open('imgs_meta_categories.json', 'w'), indent=4)
