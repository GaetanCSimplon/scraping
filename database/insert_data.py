import sqlite3
import pandas as pd

# Insertion des données de site web
def insert_data_to_db(csv_path='book_infos_cleaned.csv', db_path='book_store.db'):
    # Initialisation
    connection = sqlite3.connect(db_path) # connection à la bdd
    cursor = connection.cursor() # fonction permettant d'envoyer des requêtes SQL depuis python
    df_books = pd.read_csv(csv_path)
    if 'Unnamed: 0' in df_books.columns: # Ayant exporter les données en csv sans utiliser index=False, cette ligne permet supprimer l'ajout d'un nouvel index
        df_books = df_books.drop(columns=['Unnamed: 0'])
    # Création de la table si elle n'existe pas
        cursor.execute("""
                       
    CREATE TABLE IF NOT EXISTS book (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price DECIMAL,
        availability BOOLEAN,
        rating INT
    )
    """)

    # Création & Insertion des données
    df_books.to_sql(
        name='book',
        con=connection,
        if_exists='append',
        index=False,
    )
    connection.commit()
    connection.close()

# Insertion des données depuis l'API Google Books

def insert_api_data_to_db(df_books_list):
    # Connexion à la base
    connection = sqlite3.connect('book_store.db')
    cursor = connection.cursor()
    df_books_list = pd.read_csv('data/books_api_cleaned.csv')
    if 'Unnamed: 0' in df_books_list.columns: # Ayant exporter les données en csv sans utiliser index=False, cette ligne permet supprimer l'ajout d'un nouvel index
        df_books = df_books_list.drop(columns=['Unnamed: 0'])
        # Création de la table si elle n'existe pas
    cursor.execute("""
                       
    CREATE TABLE IF NOT EXISTS book (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price DECIMAL,
        availability BOOLEAN,
        rating INT
    )
    """)


    # Préparation des données à insérer
    df_book_list = df_book_list.copy().reset_index(drop=True)
    # df_book_list['book_id'] = range(last_id + 1, last_id + 1 + len(df_book_list))

    # Insertion dans la base
    df_book_list.to_sql(
        name='book',
        con=connection,
        if_exists='append',
        index=False
    )
    connection.commit()
   
    # Vérifier que le nombre de livres dans la table correspond au nb de livres scrapés + livres de l'API
    # cursor.execute('SELECT COUNT(book_id) from book')
    # resultat = cursor.fetchone()
    # print(f'Nombre total de livres :  {resultat[0]}') 