from typing import List

import pytest

import numpy as np
from database.TinyDB_DB import TinyDB_DB


@pytest.fixture(scope='session')
def tiny_db():
    return TinyDB_DB()

@pytest.fixture(scope='session')
def all_items(tiny_db : TinyDB_DB):
    return tiny_db.get_all()

def test_knn(tiny_db):
    test_image = tiny_db.get_all()[0]
    knn = tiny_db.knn(test_image['imgs'][0], num_neighbors=1)
    assert test_image == knn[0]


def test_feats_extracted(all_items : List[dict]):
    assert all(len(item['feats']) == len(item['imgs']) for item in all_items)
    
def test_feats_shape(all_items : List[dict]):
    first_shape = np.array(all_items[0]['feats'][0]).shape
    def is_correct_shape(item:dict):
        return all(np.array(feat).shape == first_shape for feat in item['feats'])
    assert all(is_correct_shape(item) for item in all_items)
