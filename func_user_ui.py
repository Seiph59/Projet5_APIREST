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


    choice = int(input("Entrez votre choix: \n"))
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

    choice = int(input("Entrez votre choix: \n"))
    return choice

def substitute_display(category_id):
    cursor.execute(""" SELECT food.name, food.nutriscore, food.link_openffacts, store.name, food.description
                    FROM store_food
                    INNER JOIN food
                        ON food.id = food_id
                    INNER JOIN store
                        ON store.id = store_id
                    WHERE category_food.category_id = %s
                    ORDER BY food.nutriscore
                    LIMIT 1 OFFSET 0""", category_id)
    row = cursor.fetchone()
    print("Voici un subistitut plus sain que votre choix initial : ")
    print(row[0])
    print(row[4])
    print(row[2])
    print(row[1])
    print(row[3])
    #def favourite_screen():


while True:
    choice = host()

    if choice == 1:
        id_category = categories_choice()
        id_food = food_choice(id_category)
        substitute_display(id_category)

    #elif choice == 2:
        #favourite_screen()
    else:
        sys.exit

