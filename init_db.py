from database.TinyDB_DB import TinyDB_DB
from os.path import join

DB_NAME = 'dummy.json'
SCRAPES = ['castro_clean.json']
DATA_DIR = join('database','data')
SCRAPES_DIR = join('database','data') # might be different
# TinyDB_DB.from_json(TinyDB_DB.PATH, 'scraping/scrapes/castro_clean.json', 'scraping/scrapes/hm_clean.json')
if input("Doing this will overwrite the current db. continue? y/[n]").lower() == 'y':
    db = TinyDB_DB.init_from_json(join(DATA_DIR,DB_NAME),*[join(SCRAPES_DIR,scrape) for scrape in SCRAPES])
    db.update_all_feats()
    db.init_knn()