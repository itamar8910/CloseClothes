import numpy as np
import sys
import os

def closest_feat(index,names_feats):
    return min([(name,np.linalg.norm(names_feats[index][1] - feats)) for name,feats in names_feats if name != names_feats[index][0]]
,key=lambda x:x[1])

def closest_pairs(dir_path):
    names_feats = [(f,np.load(os.path.join(dir_path,f)).flatten()) for f in os.listdir(dir_path)]
    for index in range(len(names_feats)):
        print(names_feats[index][0],closest_feat(index,names_feats))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        closest_pairs(sys.argv[1])
    else:
        print("Missing path to features")
