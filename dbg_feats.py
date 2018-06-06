from algorithm.feats.FeatsExtractor import VGG_FeatsExtractor
import numpy as np
import time

feats = VGG_FeatsExtractor().get_feats(['/home/itamar/programming/closeClothes/DeepFashion/clf_train_dummy/Jacket/Abstract_Watercolor_Floral_Jacket_img_00000011.jpg'])

feats = feats[0]
print('feats:', feats)
print('feats shape:', feats.shape)
print('feats sum:', np.sum(feats))