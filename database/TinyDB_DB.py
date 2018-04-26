from tinydb import TinyDB, Query
from database.BaseDB import BaseDB
from typing import Dict, List
import numpy as np
from algorithm.feats.FeatsExtractor import VGG_FeatsExtractor
from sklearn.neighbors import NearestNeighbors
import pickle
TINYDB_PATH = 'database/data/items_tinydb.json'
KNN_PATH = 'database/data/knn_20180425.p'

class TinyDB_DB(BaseDB):

    def __init__(self, path=TINYDB_PATH, knn_path = KNN_PATH):
        super().__init__(path)
        self.db = TinyDB(self._path)
        self.__feat_extractor = VGG_FeatsExtractor()
        try:        
            with open(knn_path, 'rb') as f:
                self.__knn_clasifier = pickle.load(f)
        except FileNotFoundError:
            self.__knn_clasifier = None
        
    def init_knn(self, save_path = KNN_PATH):
        clf = NearestNeighbors()
        # TODO: run fit every time you the db changes
        all_items = self.get_all()
        clf.fit([feats for item in all_items for feats in item['feats']],[item['url'] for item in all_items for feat in item['feats']]) # flattened array https://stackoverflow.com/a/952952/4342751
        if save_path:
            with open(save_path, 'wb') as f:
                pickle.dump(clf, f)
        return clf

    @property
    def knn_clasifier(self) -> NearestNeighbors:
        if not self.__knn_clasifier:
            raise Exception('knn_classifier must be initialized')
        return self.__knn_clasifier
    

    def add_item(self, url : str, item : Dict) -> Dict:
        self.db.insert({**item,  **{'url': url}})
        
    def remove_item(self, url : str):
        q_remove = Query()
        self.db.remove(q_remove.url == url)

    def get_by_url(self, url : str) -> Dict:
        q_get = Query()
        results = self.db.search(q_get.url == url)
        assert len(results) == 1
        return results[0]
    
    def update_feats(self, url : str, feats: List[np.ndarray]):
        q_update = Query()
        feats = [list(feat) for feat in feats] # ndarray is not json-serializeable
        for feat in feats:
            for index,item in enumerate(feat):
                feat[index] = str(item) # floats are not json-serializeable
        self.db.update({'feats':feats}, q_update.url == url)
    
    @property
    def feat_extractor(self):
        return self.__feat_extractor

    def get_all(self):
        return self.db.all()
