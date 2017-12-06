import os
import json
from PIL import Image
import random
json_data = []

upper_body_images = set()
index_to_type = []

with open("Data/Anno/list_category_cloth.txt") as f:
    lines = f.readlines()
    
    index_to_type = [[x for x in line.split()][1] for line in lines[2:]]

#print(index_to_type)
#exit()

with open("Data/Anno/list_category_img.txt") as f:
    lines = f.readlines()
    for line in lines[2:]:
        #print line
        data = line.split(" ")
        data = [x.strip() for x in data if x.strip() != ""]
        if int(index_to_type[int(data[1])]) == 1: # TODO: enumerate bounding box types (1 is for upper body)
            upper_body_images.add(data[0])

print("# of upper body images:", len(upper_body_images))

all_data = []

with open("Data/Anno/list_bbox.txt") as f:
    lines = f.readlines()
    #print len(lines)
    for line in lines[2:]:
    	data = line.split(" ")
    	data = [x.strip() for x in data if x.strip() != ""]
        #rint data[0]
        if data[0] in upper_body_images:
            all_data.append({
                "image_path":data[0], "rects":{"x1":data[1],"y1":data[2], "x2":data[3], "y2":data[4] }
                })
    		#json_data.append()

TRAIN_TEST_SPLIT = .7



shuffled_data = random.sample(all_data, len(all_data))

split_index = int(len(all_data) * TRAIN_TEST_SPLIT)

train_data = shuffled_data[:split_index]

test_data = shuffled_data[split_index:]


json.dump(train_data, open("bb_train_unresized.json",'w'))  
json.dump(test_data, open("bb_test_unresized.json",'w'))	

print("done")


