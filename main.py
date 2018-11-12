import class_test
import requests

db = class_test.Database()
db.open()
db.create()

criteria = {
    "tagtype_0": "categories",
    "tag_contains_0": "contains",
    "tag_0": "pizza",
    "sort_by": "unique_scans_n",
    "page_size": 1,
    "json":1,
    "action": "process",
}

r = requests.get("https://fr.openfoodfacts.org/cgi/search.pl", params = criteria)

pprint(r)
data = r.json()

for product in data['products']:

    db.insert_product(product)

connect.commit()