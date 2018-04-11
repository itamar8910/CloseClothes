import json

with open('scrapes/hm.json', 'r') as f:
    items = json.load(f)

sizes = [
    "XXS",
    "XS",
      "S",
      "M",
      "L",
      "XL",
      "XXL"]

urls_to_remove = set()
for item in items:
    if item['name'] == 'bad' or item['url'] == "http://www.hm.com/il/product/06064?article=06064-A":
        urls_to_remove.add(item['url'])
        continue
    item['description'] = item['description'].strip()
    item['name'] = item['name'].strip()
    item['price'] = item['price'][len("\u20aa ") : ] + "[NIS]"
    try:
        item['sizes'] = sizes[sizes.index(item['sizes'][0].strip()) : sizes.index(item['sizes'][-1].strip()) + 1]
    except: # ranges are numbers, cuz convetions are for pussies
        sizes_range = range(int(item['sizes'][0]), int(item['sizes'][-1]), 2) 
        item['sizes'] = [str(x) for x in sizes_range]

    item['imgs'] = ["https:" + x for x in item['imgs']]
items = [x for x in items if x['url'] not in urls_to_remove]

with open('scrapes/hm_clean.json', 'w') as f:
    json.dump(items, f, indent=2)
