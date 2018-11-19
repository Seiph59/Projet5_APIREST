import pymysql.cursors
import sys
try:
    connection = pymysql.connect(host='localhost',
                            user='seiph_',
                            password='abc',
                            db='projet5',
                            charset='utf8',)

    print("Connected")

except:
    print("oops")


cursor = connection.cursor()

def host():
    print(""" Bienvenue sur l'application Pur Beurre !!
            --------------------------------------------
            1: Quel aliment souhaitez-vous remplacer ?
            2: Retrouver mes aliments substitués
            3: Quitter""")

    while True:
        try:
            choice = int(input("Entrez votre choix: \n"))
            if choice in range(1,4):
                break
        except ValueError:
            continue

    return choice

def categories_choice():
    cursor.execute(" SELECT id, name FROM category ORDER BY id LIMIT 5 OFFSET 0")
    rows = cursor.fetchall()
    print("Choisissez votre catégorie :")
    for row in rows:
        print(row[0], row[1])
    while True:
        try:
            choice = int(input("Entrez votre choix: \n"))
            if choice in range(1,100):
                break
        except ValueError:
            continue

    return choice

def food_choice(category_id):
    cursor.execute(""" SELECT food.id, food.name
                    FROM food
                    INNER JOIN category_food
                        ON food.id = category_food.food_id
                    WHERE category_food.category_id = %s && nutriscore > 'b'
                    ORDER BY id LIMIT 8 OFFSET 0""", category_id)
    rows = cursor.fetchall()
    print("Choisissez votre aliment :")
    for row in rows:
        print(row[0], row[1])

    while True:
        try:
            choice = int(input("Entrez votre choix: \n"))
            if choice in range(1,1000):
                break
        except ValueError:
            continue

    return choice

def insert_in_favourite(food_id, substitute_id):
    ref = (food_id, substitute_id)
    print("""\n Souhaitez-vous ajouter cette recherche dans vos favoris ?
                1. Oui
                0. Non """)

    choice = int(input("Entrez votre choix: \n"))
    if choice == 1:
        cursor.execute("INSERT INTO favourite (food_id, substitute_id) VALUES (%s, %s)", ref)
    else:
        return

def substitute_display(category_id, food_id):
    ref = category_id, food_id
    cursor.execute(""" SELECT food.name, store.name, food.link_openffacts, food.nutriscore, food.description, food.id
                    FROM food
                    INNER JOIN store_food
                        ON food.id = store_food.food_id
                    INNER JOIN store
                        ON store_food.store_id = store.id
                    WHERE food.id IN (SELECT category_food.food_id FROM category_food WHERE category_food.category_id = %s) AND food.id != %s
                    ORDER BY food.nutriscore
                    LIMIT 1 OFFSET 0""", ref)
    row = cursor.fetchone()
    print("Voici un subistitut de votre choix initial : ")
    print(row[0])
    print(row[3])
    print(row[2])
    print(row[1])
    print(row[4])
    return row[5]

def favourite_screen():
    cursor.execute(""" SELECT *
                        FROM favourite
                        ORDER BY id """)
    rows = cursor.fetchall()
    print("Voici vos recherches sauvegardées:")
    for row in rows:
        ref = row[1], row[2]
        cursor.execute(""" SELECT name
                        FROM food
                        WHERE id = %s
                        UNION
                        SELECT name
                        FROM food
                        WHERE id = %s """, ref)
        list = cursor.fetchall()
        i = 0
        for element in list:
            if i == 0:
                print("Produit initial sélectionné: " + element[0], end= "")
                i += 1
            else:
                print(" substitué par : " + element[0])
        print("-----------------------------------------------------------------")

out = False
while out == False:
    choice = host()

    if choice == 1:
        id_category = categories_choice()
        id_food = food_choice(id_category)
        id_substitute = substitute_display(id_category, id_food)
        insert_in_favourite(id_food, id_substitute)

    elif choice == 2:
        favourite_screen()
    else:
        out = True

