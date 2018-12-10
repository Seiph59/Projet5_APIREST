""" Main file for the user interface, launch from this file to launch the application
    Before to luanch be sure to have created the database with the 'main_db.py' file.
    You also need to modify your databases information in the 'classes_user.py' file with yours"""

import classes_user

ui_user = classes_user.Interface()

loop = True
while loop == True:
    choice = classes_user.host()

    if choice == 1:
        id_category = ui_user.categories_choice()
        id_food = ui_user.food_choice(id_category)
        id_substitute = ui_user.substitute_display(id_category, id_food)
        ui_user.insert_in_favourite(id_food, id_substitute)

    elif choice == 2:
        ui_user.favourite_screen()
    else:
        ui_user.connection.commit()
        loop = False
