import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from closest_feat import closest_pairs
import sys,os

def plot_pairs(pairs,dir_path):
    f, subplots= plt.subplots(len(pairs) , 2)
    print(pairs)
    for plot,pair in zip(subplots,pairs):
        plot[0].imshow(mpimg.imread(os.path.join(dir_path,pair[0].strip(".npy") + ".jpg")))
        plot[1].imshow(mpimg.imread(os.path.join(dir_path,pair[1].strip(".npy") + ".jpg")))
        plot[0].axes.get_xaxis().set_visible(False)
        plot[0].axes.get_yaxis().set_visible(False)
        plot[1].axes.get_xaxis().set_visible(False)
        plot[1].axes.get_yaxis().set_visible(False)
        plt.axis('off')
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        plot_pairs(closest_pairs(sys.argv[1]),sys.argv[2])
    else:
        print("Missing path to features and/or images")
