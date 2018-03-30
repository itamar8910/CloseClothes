import unittest

#from extract_feats import extract_feats_vgg16 # TODO: change to real func name
import os.path
from os import listdir

class DataProcessingTests(unittest.TestCase):

    def test_extract_feats_vgg16(self):
        TEST_IMGS_DIR = "test_data/feats_extraction"
        #extract_feats_vgg16(TEST_IMGS_DIR) # TODO: change to real func name
        self.assertTrue(os.path.isdir(os.path.join(TEST_IMGS_DIR, "feats"))) # check that created feats dir
        num_imgs = len([x for x in listdir(TEST_IMGS_DIR) if os.path.isfile(os.path.join(TEST_IMGS_DIR, x))])
        self.assertEqual(num_imgs, len(listdir(os.path.join(TEST_IMGS_DIR, "feats")))) # check that created feats file for each image
        # TODO: assert that feats are correct



if __name__ == '__main__':
    unittest.main()
