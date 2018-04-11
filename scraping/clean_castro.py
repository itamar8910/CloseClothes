import json

with open('scrapes/castro.json', 'r') as f:
    items = json.load(f)

for item in items:
    item['description'] = item['description'].strip()
    item['sizes'] = [x for x in item['sizes'] if x != "\u05d0\u05d6\u05dc \u05d1\u05de\u05dc\u05d0\u05d9"] # filter our "out of stock"


with open('scrapes/castro_clean.json', 'w') as f:
    json.dump(items, f, indent=2)
