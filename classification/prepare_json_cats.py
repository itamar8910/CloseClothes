import os
import json

if __name__ == "__main__":
    json_data = []
    categories = []
    with open('../../DeepFashion/Anno/list_category_cloth.txt', 'r') as f:
        lines = f.readlines()
        categories = {line_i+1 : line.split()[0] for line_i, line in enumerate(lines[2:])}
    
   
    with open('../../DeepFashion/Anno/list_category_img.txt', 'r') as f:
        lines = f.readlines()[2:]
        for line in lines:
            img_path = line.split()[0]
            category_index = int(line.split()[1])
            json_data.append({'img_path':img_path, 'category':categories[category_index]})
            
    json.dump(json_data, open('imgs_categories.json', 'w'), indent=4)

   