from database.TinyDB_DB import TinyDB_DB
import imageio
tiny = TinyDB_DB('tinydb_with_feats.json')
tiny.update_all_feats()
test_image = tiny.get_all()[0]
knn = tiny.knn(test_image['imgs'][0],num_neighbors=1)
assert knn[0] == test_image