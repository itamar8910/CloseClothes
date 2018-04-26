from typing import Dict, List
import json
import numpy as np
import abc
from algorithm.feats.FeatsExtractor import FeatsExtractor
from tqdm import tqdm

class BaseDB(abc.ABC):

    def __init__(self, path):
        self._path = path

    @abc.abstractmethod
    def add_item(self, url : str, item : Dict) -> Dict:
        ...
        
    @abc.abstractmethod
    def remove_item(self, url : str):
        ...

    @abc.abstractmethod
    def get_by_url(self, url : str) -> Dict:
        ...
    
    @abc.abstractmethod
    def update_feats(self, url : str, feats: List[np.ndarray]):
        ...
    
    @property
    @abc.abstractmethod
    def feat_extractor(self) -> FeatsExtractor:
        ...
    
    @property
    @abc.abstractmethod
    def knn_clasifier(self):  # lazily evaluate
        ...

    def knn(self, center: np.ndarray, num_neighbors: int) -> List[dict]:
        """ given a "center" image vector, return the {num_neighbors} nearest DB items """
        center_feats = self.feat_extractor.get_feats([center])
        neighbor_indexes = self.knn_clasifier.kneighbors(center_feats, num_neighbors, return_distance=False)
        all_items = self.get_all()
        knn = [all_items[index] for index in neighbor_indexes[0]]
        assert len(knn) == num_neighbors
        return knn

    def update_all_feats(self, verbose=True):
        for item in tqdm(iterable=self.get_all(), desc="Feats updated", disable=not verbose):
            # if verbose:
            #     print(item['url'])
            try: # check if item already has feats
                item['feats']
            except KeyError:
                item_feats = self.feat_extractor.get_feats(item['imgs'])
                self.update_feats(item['url'],item_feats)

    def get_all(self):
        ...

    @classmethod
    def init_from_json(cls, db_path, *json_paths):
        db = cls(db_path)
        for json_path in json_paths:
            print(json_path)
            with open(json_path, 'r') as f:
                items = json.load(f)
                for item in items:
                    db.add_item(url=item['url'], item=item)
        return db
