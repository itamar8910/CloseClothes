from database import BaseDB

def test_inner_index():
    inner_index = BaseDB.inner_index
    li = ['b'] + ['a'] * 5
    assert inner_index(3,li) == 2
    assert inner_index(0,li) == 0
    li = ['b'] * 2 + ['a'] * 3 + ['c'] * 2
    assert inner_index(0,li) == 0
    assert inner_index(2,li) == 0
    assert inner_index(6,li) == 1
    assert inner_index(4,li) == 2
