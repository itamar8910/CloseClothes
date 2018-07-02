from typing import Dict, List,Tuple
from urllib.error import HTTPError
import json
import numpy as np
import abc
from algorithm.feats import FeatsExtractor
from tqdm import tqdm
from sklearn.neighbors import NearestNeighbors
import pickle
from lazy import lazy

KNN_PATH = 'database/data/knn_20180610.p'
class BaseDB(abc.ABC):
    @lazy
    def all_items(self):
        return self.get_all()

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
        X = np.stack([np.array(feats) for item in self.all_items for feats in item['feats']])
        labels = self.labels()
        clf.fit(X,labels) # flattened array https://stackoverflow.com/a/952952/4342751
        if save_path:
            with open(save_path, 'wb') as f:
                pickle.dump(clf, f)
        return clf

    @lazy
    def labels(self):
        labels = [item['url'] for item in self.all_items for feat in item['feats']]
        return labels

    @property
    def knn_clasifier(self) -> NearestNeighbors:
        if not self.__knn_clasifier:
            raise Exception('knn_classifier must be initialized,initialize it by running init_knn()')
        return self.__knn_clasifier

    @staticmethod
    def inner_index(index : int,labels :List[str]):
        """
        given an index in `self.labels` returns the "inner_index" of that item.
        meaning what number picture it is inside the item
        """
        item_url = labels[index]
        url = item_url
        i = 0
        try:
            while url == item_url:
                i+=1
                url = labels[index - i]
        except IndexError: # i out of range, it's the first item
            pass
        return i-1

    def knn(self, center: str, num_neighbors: int) -> List[Tuple[int,dict]]:
        """ given a "center" path to image vector, return the {num_neighbors} nearest DB items """
        center_feats = self.feat_extractor.get_feats([center])
        neighbor_indicies = self.knn_clasifier.kneighbors(center_feats, num_neighbors, return_distance=False)
        clothes_urls = [self.labels[index] for index in neighbor_indicies[0]]
        inner_indices = [self.inner_index(index,self.labels) for index in neighbor_indicies[0]]
        clothes = [self.get_by_url(url) for url in clothes_urls]
        assert len(clothes) == num_neighbors
        return list(zip( inner_indices,clothes))

    def update_all_feats(self, verbose=True):
        for item in tqdm(iterable=self.get_all(), desc="Feats updated", disable=not verbose):
            # if verbose:
            #     print(item['url'])
 
            try:
                item_feats = self.feat_extractor.get_feats(item['imgs'])
                self.update_feats(item['url'], item_feats)
            except (HTTPError, IOError) as e: #Non-existant scrape image. 
                print(e)
                self.remove_item(item['url'])

    
    def get_all(self):
        raise NotImplementedError

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

