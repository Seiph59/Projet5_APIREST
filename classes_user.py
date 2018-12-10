"""File linked with 'main_user.py'  """
import pymysql.cursors

try:
    import config
except ImportError:
    print("No configuration file found")
    exit()

def host():
    """ Display the 'home menu' """

    print(""" Bienvenue sur l'application Pur Beurre
            --------------------------------------------
            1: Quel aliment souhaitez-vous remplacer ?
            2: Retrouver mes aliments substitués
            3: Quitter""")

    while True:
        try:
            choice = int(input("Entrez votre choix: \n"))
            if choice in range(1, 4):
                break
        except ValueError:
            continue

    return choice

class Interface:
    """ Class which generate the User interface and useful
    to connect on your database (put your own information's connection
    to access to your database) """

    def __init__(self):
        self.connection = pymysql.connect(host= config.DATABASE_HOST,
                                          user= config.DATABASE_USER,
                                          password= config.DATABASE_PASSWORD,
                                          db= config.DATABASE_NAME,
                                          charset= config.DATABASE_CHARSET)
        self.cursor = self.connection.cursor()

    def categories_choice(self):
        """ Display the category menu , limited to 5 choices"""

        self.cursor.execute(""" SELECT id, name
                            FROM category
                            ORDER BY id LIMIT 5 OFFSET 0""")
        rows = self.cursor.fetchall()
        print("Choisissez votre catégorie :")
        possible_choice = []
        while True:
            try:
                for row in rows:
                    possible_choice.append(row[0])
                    print(row[0], row[1])
                choice = int(input("Entrez votre choix: \n"))
                if choice in possible_choice:
                    break
            except ValueError:
                continue

        return choice

    def food_choice(self, category_id):
        """ Display the 'food menu' """

        self.cursor.execute(""" SELECT food.id, food.name
                    FROM food
                    INNER JOIN category_food
                        ON food.id = category_food.food_id
                    WHERE category_food.category_id = %s && nutriscore > 'b'
                    ORDER BY id LIMIT 8 OFFSET 0""", category_id)
        rows = self.cursor.fetchall()
        print("Choisissez votre aliment :")
        possible_choice = []
        while True:
            try:
                for row in rows:
                    possible_choice.append(row[0])
                    print(row[0], row[1])
                choice = int(input("Entrez votre choix: \n"))
                if choice in possible_choice:
                    break
            except ValueError:
                continue

        return choice

    def insert_in_favourite(self, food_id, substitute_id):
        """ Menu which allow the user to save his current research """

        ref = (food_id, substitute_id)
        print("""\n Souhaitez-vous ajouter cette recherche dans vos favoris ?
                    1. Oui
                    0. Non """)

        choice = int(input("Entrez votre choix: \n"))
        if choice == 1:
            self.cursor.execute("""INSERT INTO favourite
                                (food_id, substitute_id)
                                VALUES (%s, %s)""", ref)
        else:
            return

    def substitute_display(self, category_id, food_id):
        """ When the user has choosen his food, display a substitute healthier

        with all the informations needed"""
        ref = category_id, food_id
        self.cursor.execute(""" SELECT food.name, store.name,
                        food.link_openffacts,
                        food.nutriscore, food.description, food.id
                        FROM food
                        INNER JOIN store_food
                            ON food.id = store_food.food_id
                        INNER JOIN store
                            ON store_food.store_id = store.id
                        WHERE food.id IN (SELECT category_food.food_id
                                          FROM category_food
                                          WHERE category_food.category_id = %s)
                                          AND food.id != %s
                                          ORDER BY food.nutriscore
                                          LIMIT 1 OFFSET 0""", ref)
        row = self.cursor.fetchone()
        print("Voici un subistitut de votre choix initial : ")
        print("Nom du produit : " + row[0])
        print("Grade nutriscore : " + row[3])
        print("Lien OpenFoodFacts : " + row[2])
        print("Magasin(s) : " + row[1])
        print("Description du produit : " + row[4])
        return row[5]

    def favourite_screen(self):
        """Display all the foods that the user saved previously """

        self.cursor.execute(""" SELECT *
                            FROM favourite
                            ORDER BY id """)
        rows = self.cursor.fetchall()
        print("Voici vos recherches sauvegardées: \n")
        for row in rows:
            ref = row[1], row[2]
            self.cursor.execute(""" SELECT name
                            FROM food
                            WHERE id = %s
                            UNION
                            SELECT name
                            FROM food
                            WHERE id = %s """, ref)
            food_names = self.cursor.fetchall()
            i = 0
            for element in food_names:
                if i == 0:
                    print("Produit initial : " + element[0].upper(), end="")
                    i += 1
                else:
                    print(" substitué par : " + element[0].upper())
            print("----------------------------------------------------------")
