# Projet5_APIREST
Project5 Openclassrooms, with the use of a REST API and MYSQL databases


Link project : https://github.com/Seiph59/Projet5_APIREST 

# What is this project ? 

This project has for objective to supply a list of ingredients substitutes to clean up its food, with a complete description and a place where we can obtain this food.

#  How ? 
To create this solution, we are going to use , Python3, Mysql, and the Openfoodfacts API,you can find this API on this link below: 
[wiki Open Food Facts] (https://en.wiki.openfoodfacts.org/API)

# Libaries Used and Python Version: 

* Python 3.6.5
* See the Requirements.txt

## Before to start

You will have 4 Files:
	* 2 for the creation of the Database and data insertion
		* main_db.py
		*classes_db.py

	* 2 for the User interface
		* main_user.py
		* classes_user.py

### How to use step by step ? 

1. You need to create you own database and modify the informations in the constructor of  the class "Database" , with yours. (main_db.py)

2. To put the language research in English, Replace "https://fr.openfoodfacts.org/cgi/search.pl" by " https://world.openfoodfacts.org/cgi/search.pl" in the "criteria" method  (main_db.py)

3. To change or modify the different criteria, you need to refer to this link [Wiki API Read Search] (https://en.wiki.openfoodfacts.org/API/Read/Search)

4. Then you can launch "main_db.py"

5. Once installed, you can open the file "classes_user.py" and modifiy once again your connection informations for the database 

6. Finally, launch "main_user.py"