""" File used by 'main_db.py',
before to launch be sure to modify with your database informations """

import pymysql.cursors
import requests


def criteria(category_name, page_size):
    """To modify the criteria research of the API """

    criteria_api = {
        "tagtype_0": "categories",
        "tag_contains_0": "contains",
        "tag_0": category_name,
        "sort_by": "unique_scans_n",
        "page_size": page_size,
        "json": 1,
        "action": "process",
        }

    request = requests.get("https://fr.openfoodfacts.org/cgi/search.pl", params=criteria_api)
    data = request.json()
    return data


class Database:
    """ Class to connect on your MYSQL database and to insert the data directly in """

    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                          user='seiph_',
                                          password='abc',
                                          db='projet5',
                                          charset='utf8mb4',)
        self.cursor = self.connection.cursor()

    def create_food_store_category(self):
        """ Create tables food, store and category """

        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS food(
                            id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(250) NOT NULL,
                            description TEXT,
                            link_openffacts VARCHAR(200),
                            nutriscore CHAR(1) NOT NULL)
                        ENGINE=INNODB;""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS store(
                            id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(75))
                        ENGINE=InnoDB;""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS category(
                            id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR (150))
                        ENGINE=InnoDB;""")
        self.create_favourite_category_food()

    def create_favourite_category_food(self):
        """ Create tables favourite and category_food """

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS favourite(
                            id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            food_id INT UNSIGNED NOT NULL,
                            substitute_id INT UNSIGNED NOT NULL,
                            CONSTRAINT fk_fav_food
                                FOREIGN KEY (food_id)
                                REFERENCES food(id),
                            CONSTRAINT fk_fav_substitute
                                FOREIGN KEY (substitute_id)
                                REFERENCES food(id))
                        ENGINE=InnoDB;""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS category_food(
                            id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            category_id INT UNSIGNED NOT NULL,
                            food_id INT UNSIGNED NOT NULL,
                            CONSTRAINT fk_category_id
                                FOREIGN KEY (category_id)
                                REFERENCES category(id),
                            CONSTRAINT fk_cat_food_id
                                FOREIGN KEY (food_id)
                                REFERENCES food(id))
                        ENGINE=InnoDB;""")
        self.create_store_food()

    def create_store_food(self):
        """ Create table store_food """

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS store_food(
                            id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            store_id INT UNSIGNED NOT NULL,
                            food_id INT UNSIGNED NOT NULL,
                            CONSTRAINT fk_store_id
                                FOREIGN KEY (store_id)
                                REFERENCES store(id),
                            CONSTRAINT fk_store_food_id
                                FOREIGN KEY (food_id)
                                REFERENCES food(id))
                        ENGINE=InnoDB;""")

        print("Database created successfully")

    def select_or_insert_category(self, category):
        """ Method which allow to create a category if it doesn't exist and
        take the category's ID otherwise only take the category ID """

        recup = self.cursor.execute(" SELECT id FROM category WHERE name = %s", category)
        if recup > 0:
            value = self.cursor.fetchone()
            return value[0]
        else:
            self.cursor.execute("INSERT INTO category (name) VALUES (%s)", category)
            recup = self.cursor.execute("SELECT id FROM category WHERE id=LAST_INSERT_ID()")
            value = self.cursor.fetchone()
            return value[0]

    def select_or_insert_store(self, store):
        """ Method which allow to create a store if it doesn't exist, and
        take the store's ID otherwise only take the store ID """

        recup = self.cursor.execute(" SELECT id FROM store WHERE name = %s", store)
        if recup > 0:
            value = self.cursor.fetchone()
            return value[0]
        else:
            self.cursor.execute("INSERT INTO store (name) VALUES (%s)", store)
            recup = self.cursor.execute("SELECT id FROM store WHERE id=LAST_INSERT_ID()")
            value = self.cursor.fetchone()
            return value[0]

    def insert_store_food(self, id_store, id_food):
        """ Add the id_store and the id_food in the store_food TABLE"""

        ref = (id_store, id_food)
        self.cursor.execute("""INSERT INTO store_food (store_id, food_id)
                                VALUES (%s, %s)""", ref)

    def insert_category_food(self, id_category, id_food):
        """ Do insertion into category_food TABLE """
        ref = (id_category, id_food)
        self.cursor.execute(""" INSERT INTO category_food (category_id, food_id)
                                VALUES (%s, %s)""", ref)

    def insert_product(self, product):
        """ Insert the product name in the database, if the product_name_fr doesn't exist,
        the method skip the product to avoid an error """

        product_name = product.get('product_name_fr')
        if product_name is None:
            product_name = product['product_name']

        nutrition_grade = product.get('nutrition_grades')
        if nutrition_grade is None:
            print(f"{product_name} n'a pas été ajouté")
            return

        ingredients_text = product.get('ingredients_text_fr')
        if ingredients_text is None:
            ingredients_text = product['ingredients_text']

        ref = (product_name, ingredients_text, product['url'], product['nutrition_grades'])
        self.cursor.execute(""" INSERT INTO food (name, description, link_openffacts, nutriscore)
                    VALUES (%s, %s, %s, %s)""", ref)
        self.cursor.execute("SELECT id FROM food WHERE id=LAST_INSERT_ID() ")
        value = self.cursor.fetchone()
        food_id = value[0]
        categories = product['categories'].split(",")
        for category in categories:
            category_id = self.select_or_insert_category(category)
            self.insert_category_food(category_id, food_id)
        stores = product['stores'].split(",")
        for store in stores:
            store_id = self.select_or_insert_store(store)
            self.insert_store_food(store_id, food_id)
        print("données de " + product_name + " insérées !")
