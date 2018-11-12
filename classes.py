import pymysql.cursors

class Database:
    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                            user='seiph_',
                            password='abc',
                            db='projet5',
                            charset='utf8mb4',)
        self.cursor = self.connection.cursor()

    def open(self):
        try:
            self.connection

            print("Connected")

        except:
            print("Oops not connected")

    def create(self):

        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS food(
                            id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(100) NOT NULL,
                            description TEXT,
                            category VARCHAR (150),
                            link_openffacts VARCHAR(120),
                            store VARCHAR(30),
                            nutriscore CHAR(1) NOT NULL)
                        ENGINE=INNODB;""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS store(
                            id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(30))
                        ENGINE=InnoDB;""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS category(
                            id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR (150))
                        ENGINE=InnoDB;""")

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

    def select_or_insert_category(self,category):
        recup = self.cursor.execute(" SELECT id FROM category WHERE name = %s",category)
        if recup > 0:
            value = cursor.fetchone()
            return value[0]
        else:
            self.cursor.execute("INSERT INTO category (name) VALUES (%s)", category)
            recup = self.cursor.execute("SELECT id FROM category WHERE id=LAST_INSERT_ID()")
            value = cursor.fetchone()
            return value[0]

    def select_or_insert_store(self,store):
        recup = self.cursor.execute(" SELECT id FROM store WHERE name = %s", store)
        if recup > 0:
            value = cursor.fetchone()
            return value[0]
        else:
            self.cursor.execute("INSERT INTO store (name) VALUES (%s)", store)
            recup = self.cursor.execute("SELECT id FROM store WHERE id=LAST_INSERT_ID()")
            value = cursor.fetchone()
            return value[0]

    def insert_store_food(self, id_store, id_food):
        self.cursor.execute("INSERT INTO store_food (store_id, food_id) VALUES (%s, %s)", id_store, id_food)

    def insert_category_food(self, id_category, id_food):
        self.cursor.execute(" INSERT INTO category_food (category_id, food_id) VALUES (%s, %s)", id_category, id_food)


    def insert_product(self,product):
        ref = (product['product_name_fr'], product['ingredients_text_fr'], product['url'], product['nutrition_grades'])
        self.cursor.execute(""" INSERT INTO food (name, description, link_openffacts, nutriscore)
                    VALUES (%s, %s, %s, %s)""", ref)
        recup = self.cursor.execute("SELECT id FROM food WHERE id=LAST_INSERT_ID() ")
        value = cursor.fetchone()
        food_id = value[0]
        categories = product['categories'].split(",")
        for category in categories:
            category_id = self.select_or_insert_category(category)
            self.insert_category_food(category_id, food_id)
        stores = product['stores'].split(",")
        for store in stores:
            store_id = self.select_or_insert_store(store)
            self.insert_store_food(store_id, food_id)
        print("données de "+ product['product_name_fr'] + " insérées !" )