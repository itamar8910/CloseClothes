import os
import json
from os.path import join
import argparse

def tag_knn(dir_path,file_name,k,dont_append,reverse):
    """Tags the K NN of all images in dir_path(using user input)\n 
    if append is true it will only tag images that arent in the given file"""
    output = dict()
    output['k'] = k
    output['knns'] = dict()
    if not dont_append:
        try:
            output = json.load(open(file_name,mode='r'))
        except FileNotFoundError:
           pass
    k = output['k']
    images = (image for image in os.listdir(dir_path) if not image in output['knns'].keys() and image.endswith((".jpg",".png")))
    iterator = sorted(images)
    if reverse:
        iterator = reversed(iterator)
    for image in iterator:
        print(image)
        # os.system("see " + os.path.join(dir_path,image))
        knn = list()
        for i in range(k):
            nn = input("nearest neighbor #" + str(i) + ':')
            print(nn)
            knn.append(nn)
        output['knns'][image] = knn
        output_json = json.dump(output,open(file_name,mode='w'))

def get_args():
    """usage dir filename [-k int] [--dont_append]"""
    parser = argparse.ArgumentParser()
    parser.add_argument("dir",type=str)
    parser.add_argument("filename",type=str)
    parser.add_argument("-k", type=int,default=5)
    parser.add_argument("--dont_append", action='store_true',help="Append more to given file")
    parser.add_argument("--reverse",action="store_true",help="Tag files in reverse order")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    tag_knn(args.dir,args.filename,args.k,args.dont_append,args.reverse)
    print("Done")
    
