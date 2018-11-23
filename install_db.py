""" Main file for the creation of the database, launch from this file the creation
    Be sure you modified the fil 'classes_db.py' your own connection's informations"""

import classes_db

db = classes_db.Database()
db.create_food_store_category()

#request = classes_db.ApiRequest()

data = classes_db.criteria("Desserts", 500)
for product in data['products']:
    db.insert_product(product)

data = classes_db.criteria("Boissons", 250)
for product in data['products']:
    db.insert_product(product)

data = classes_db.criteria("Conserves", 500)
for product in data['products']:
    db.insert_product(product)

db.connection.commit()
