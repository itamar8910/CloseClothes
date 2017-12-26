import numpy as np
import sys
import os

def closest_feat(index,names_feats):
    return min([(name,np.linalg.norm(names_feats[index][1] - feats)) for name,feats in names_feats if name != names_feats[index][0]]
,key=lambda x:x[1])

def closest_pairs(dir_path):
    """returns a list of tuples (feature,neighbor,distance)"""
    names_feats = [(f,np.load(os.path.join(dir_path,f)).flatten()) for f in os.listdir(dir_path)]
    pairs = list()
    for index in range(len(names_feats)):
        neighbor_name,distance = closest_feat(index,names_feats)
        pairs.append((names_feats[index][0],neighbor_name,distance))
    return pairs
    # return sorted(pairs, key=lambda x: int(x[0][:x[0].index(".npy")]))

def get_KNN(feats_dir, sample_name, k = 1):
    sample_feats = np.load(os.path.join(feats_dir, sample_name+".npy")).flatten()
    names_feats = [(name.replace(".npy",''),np.load(os.path.join(feats_dir,name)).flatten()) for name in os.listdir(feats_dir) if name.replace(".npy",'') != sample_name]

    return [x[0] for x in sorted(names_feats, key=lambda x : np.linalg.norm(sample_feats - x[1]))[:k]]  

if __name__ == "__main__":
    # closest_feat.py feats_path [mode=--pairs/--knn]
    if len(sys.argv) < 3:
        print("Usage: closest_feat.py feats_path [mode=--pairs/--knn sample_name k]")
        exit()
    if sys.argv[2] == '--pairs':
        print(closest_pairs(sys.argv[1]))
    elif sys.argv[2] == '--knn':
        if len(sys.argv) < 4:
            print("need to give sample_name for KNN")
            exit()
        if len(sys.argv) < 5:
            k = 1
            print("missing value for k, defaulting to K=1")
        else:
            k = int(sys.argv[4])
        print(get_KNN(sys.argv[1], sys.argv[3], k=k))

