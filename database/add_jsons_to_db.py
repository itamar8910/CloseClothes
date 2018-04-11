from BaseDB import *
from TinyDB_DB import *


TinyDB_DB.from_json(TinyDB_DB.PATH, 'scraping/scrapes/castro_clean.json', 'scraping/scrapes/hm_clean.json')
