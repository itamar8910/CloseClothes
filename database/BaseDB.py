from typing import Dict
import json

class BaseDB:

    def __init__(self, path):
        self._path = path

    def add_item(self, url : str, item : Dict) -> Dict:
        raise NotImplementedError
        
    def remove_item(self, url : str):
        raise NotImplementedError

    def get_by_url(self, url : str) -> Dict:
        raise NotImplementedError
    
    @classmethod
    def from_json(cls, db_path, *json_paths):
        db = cls(db_path)
        for json_path in json_paths:
            print(json_path)
            with open(json_path, 'r') as f:
                items = json.load(f)
                for item in items:
                    db.add_item(url=item['url'], item=item)
        return db
