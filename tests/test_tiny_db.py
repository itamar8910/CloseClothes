import pytest

from database.TinyDB_DB import TinyDB_DB

@pytest.fixture
def tiny_db():
    return TinyDB_DB()


def test_knn(tiny_db):
    test_image = tiny_db.get_all()[0]
    knn = tiny_db.knn(test_image['imgs'][0], num_neighbors=1)
    assert test_image == knn[0]
