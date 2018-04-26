from unittest import TestCase
from database.TinyDB_DB import TinyDB_DB
class TinyDbTest(TestCase):
    def setUp(self):
        self.tiny = TinyDB_DB()
    
    def testKNN(self):
        test_image = self.tiny.get_all()[0]
        knn = self.tiny.knn(test_image['imgs'][0],num_neighbors=1)
        self.assertEqual(test_image,knn[0])