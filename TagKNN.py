import os
import json
from os.path import join
import argparse


def tag_knn(dir_path,file_name,k,append):
    """Tags the K NN of all images in dir_path(using user input)\n 
    if append is true it will only tag images that arent in the given file"""
    output = {}
    output['k'] = k
    output['knns'] = dict()
    a = dict()
    if append:
        output = json.loads(open(file_name,mode='r'))
    images = (image for image in os.listdir(dir_path) if not image in output['knns'].keys() and image.endswith((".jpg",".png")))
    for image in sorted(images):
        print(image)
        print("")
        knn = list()
        for i in range(k):
            nn = input(str(i) + "th nearest neighbor:")
            print(nn)
            knn.append(nn)
        output[image] = knn
        output_json = json.dump(output,open(file_name,mode='w'))

def get_args():
    """usage dir filename [-k int] [--append]"""
    parser = argparse.ArgumentParser()
    parser.add_argument("dir",type=str)
    parser.add_argument("filename",type=str)
    parser.add_argument("-k", type=int,default=5)
    parser.add_argument("--append", action='store_true',help="Append more to given file")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    tag_knn(args.dir,args.filename,args.k,args.append)
    print("Done")
    