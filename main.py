from database.TinyDB_DB import TinyDB_DB
tiny = TinyDB_DB.init_from_json('tinydb_with_feats.json','scraping/castro_clean.json')
tiny.update_all_feats()