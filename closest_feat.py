import numpy as np
import sys
import os

def closest_feat(index,names_feats):
    return min([(name,np.linalg.norm(names_feats[index][1] - feats)) for name,feats in names_feats if name != names_feats[index][0]]
,key=lambda x:x[1])
#TODO nearest_neighbor not symettrical => bugged
def closest_pairs(dir_path):
    """returns a list of tuples (feature,neighbor,distance)"""
    names_feats = [(f,np.load(os.path.join(dir_path,f)).flatten()) for f in os.listdir(dir_path)]
    pairs = list()
    for index in range(len(names_feats)):
        neighbor_name,distance = closest_feat(index,names_feats)
        pairs.append((names_feats[index][0],neighbor_name,distance))
    return sorted(pairs, key=lambda x: int(x[0][:x[0].index(".npy")]))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(closest_pairs(sys.argv[1]))
    else:
        print("Missing path to features")
