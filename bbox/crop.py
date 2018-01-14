from PIL import Image
import json
from os.path import join, isfile
from random import shuffle
def crop(src_path, x1, x2, y1, y2, dst_path, verbose = False):
    img = Image.open(src_path)
    area = (x1, y1, x2, y2)
    cropped_img = img.crop(area)
    if verbose:
        img.show()
        cropped_img.show()
    cropped_img.save(dst_path)

if __name__ == "__main__":
    json_path = 'bb_json_pretty.json'
    save_path = 'cropped_imgs/'
    data = json.load(open(json_path, 'r'))
    shuffle(data)
    NUM_SAVE = 50
    for img_data in data[:NUM_SAVE]:
        if not isfile(join("../../DeepFashion/", img_data['image_path'])):
            continue
        img_fullname = "_".join(img_data['image_path'].split("/")[-2:])
        print(img_fullname)
        
        crop(join("../../DeepFashion/", img_data['image_path']), int(img_data['rects']['x1']), int(img_data['rects']['x2']),int(img_data['rects']['y1']),int(img_data['rects']['y2']), join(save_path, img_fullname))
        