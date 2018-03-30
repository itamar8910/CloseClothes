import numpy as np
import sys
import os
from sklearn.neighbors import NearestNeighbors
from functools import partial
import click


def read_single_feature_array(feat_name, feats_dir):
    return np.load(os.path.join(feats_dir, feat_name)).flatten()

@click.command()
@click.argument("feats_dir")
@click.option("--k", "-k", default=1, help="Amount of nearest neighbors for sample")
def print_KNN(feats_dir, k):
    debug = True
    print(get_KNN(feats_dir, sample_name, k))



def get_KNN(feats_dir, k):
    """returns a list of all KNN of feature arrays in feats_dir
    [[(FEAT1,0),(FEAT1-1nn,dist)...]]"""
    feat_files = os.listdir(feats_dir)
    feat_list = list(map(partial(read_single_feature_array,
                            feats_dir=feats_dir), os.listdir(feats_dir)))
    clf = NearestNeighbors(
        n_neighbors=k + 1, algorithm='auto').fit(feat_list)
    distances_matrix, indices_matrix = clf.kneighbors(feat_list)
    ret = list()
    for knn_indices,distances in zip(indices_matrix,distances_matrix):
        print(knn_indices,distances)
        index_to_file_name = map(lambda index: feat_files[index], knn_indices)
        ret.append(tuple(zip(index_to_file_name,distances)))
    return ret


if __name__ == "__main__":
    # closest_feat.py feats_path [mode=--pairs/--knn]
    print_KNN()
