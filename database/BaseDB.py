from typing import Dict, List
from urllib.error import HTTPError
import json
import numpy as np
import abc
from algorithm.feats import FeatsExtractor
from tqdm import tqdm
from sklearn.neighbors import NearestNeighbors
import pickle

KNN_PATH = 'database/data/knn_20180425.p'
class BaseDB(abc.ABC):
    def __init__(self, path,knn_path=KNN_PATH):
        self._path = path
        try:        
            with open(knn_path, 'rb') as fp:
                self.__knn_clasifier = pickle.load(fp)
        except FileNotFoundError:
            self.__knn_clasifier = None

    

    @abc.abstractmethod
    def add_item(self, url : str, item : Dict) -> Dict:
        pass
        
    @abc.abstractmethod
    def remove_item(self, url : str):
        pass

    @abc.abstractmethod
    def get_by_url(self, url : str) -> Dict:
        pass
    
    @abc.abstractmethod
    def update_feats(self, url : str, feats: List[np.ndarray]):
        pass
    
    @property
    @abc.abstractmethod
    def feat_extractor(self) -> FeatsExtractor:
        pass
    
    def init_knn(self, save_path = KNN_PATH):
        clf = NearestNeighbors()
        # TODO: run fit every time you the db changes
        all_items = self.get_all()
        X = np.stack([np.array(feats) for item in all_items for feats in item['feats']])
        labels = [item['url'] for item in all_items for feat in item['feats']]
        clf.fit(X,labels) # flattened array https://stackoverflow.com/a/952952/4342751
        if save_path:
            with open(save_path, 'wb') as f:
                pickle.dump(clf, f)
        return clf

    @property
    def knn_clasifier(self) -> NearestNeighbors:
        if not self.__knn_clasifier:
            raise Exception('knn_classifier must be initialized,initialize it by running init_knn()')
        return self.__knn_clasifier

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
                try:
                    item_feats = self.feat_extractor.get_feats(item['imgs'])
                    self.update_feats(item['url'], item_feats)
                except HTTPError as e:
                    print(e) #don't stop for one error

    def get_all(self):
        pass

    @classmethod
    def init_from_json(cls, db_path, *json_paths):
        db = cls(db_path)
        for json_path in json_paths:
            print(json_path)
            with open(json_path, 'r') as fp:
                items = json.load(fp)
                for item in items:
                    db.add_item(url=item['url'], item=item)
        return db

