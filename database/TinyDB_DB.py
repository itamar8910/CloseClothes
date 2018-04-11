from tinydb import TinyDB, Query
from BaseDB import BaseDB
from typing import Dict, List
import numpy as np


class TinyDB_DB(BaseDB):
    
    PATH = 'database/items_tinydb.json'
    
    def __init__(self, path):
        super().__init__(path)
        self.db = TinyDB(self._path)

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
        self.db.update({'feats':feats}, q_update.url == url)


    def get_all(self):
        return self.db.all()



