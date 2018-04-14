from tinydb import TinyDB, Query
from database.BaseDB import BaseDB
from typing import Dict, List
import numpy as np
from algorithm.feats.FeatsExtractor import VGG_FeatsExtractor

TINYDB_PATH = 'database/items_tinydb.json'
class TinyDB_DB(BaseDB):
    
    
    def __init__(self, path=TINYDB_PATH):
        super().__init__(path)
        self.db = TinyDB(self._path)
        self.__feat_extractor = VGG_FeatsExtractor()

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



