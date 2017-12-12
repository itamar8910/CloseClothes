import json
import os
import random
TRAIN_TEST_SPLIT = .7
DATA_PATH = os.path.join("utils","TensorBox","data","DeepFashion")
def main():
    """ """
    upper_body_images = set()
    index_to_type = []

    with open(os.path.join(DATA_PATH,"Anno/list_category_cloth.txt")) as file:
        lines = file.readlines()
        index_to_type = [[x for x in line.split()][1] for line in lines[2:]]

    with open(os.path.join(DATA_PATH,"Anno/list_category_img.txt")) as file:
        lines = file.readlines()
        for line in lines[2:]:
            #print line
            data = line.split(" ")
            data = [x.strip() for x in data if x.strip() != ""]
            if int(index_to_type[int(data[1])]) == 1: # TODO: enumerate bounding box types (1 is for upper body)
                upper_body_images.add(data[0])

    print("# of upper body images:", len(upper_body_images))

    all_data = []

    with open(os.path.join(DATA_PATH,"Anno/list_bbox.txt")) as file:
        lines = file.readlines()
        #print len(lines)
        for line in lines[2:]:
            data = line.split(" ")
            data = [x.strip() for x in data if x.strip() != ""]
            #rint data[0]
            if data[0] in upper_body_images:
                all_data.append({
                "image_path":data[0], "rects":[{"x1":int(data[1]),"y1":int(data[2]), "x2":int(data[3]), "y2":int(data[4]) }]
                })
            #json_data.append()




    shuffled_data = random.sample(all_data, len(all_data))
    split_index = int(len(all_data) * TRAIN_TEST_SPLIT)
    train_data = shuffled_data[:split_index]
    test_data = shuffled_data[split_index:]
    print("saving...")
    json.dump(train_data, open(os.path.join(DATA_PATH,"bb_train_unresized.json"),'w'),indent=2)  
    json.dump(test_data, open(os.path.join(DATA_PATH,"bb_test_unresized.json"),'w'),indent=2)
    print("done")

if __name__ == '__main__':
    main()