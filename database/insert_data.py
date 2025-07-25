import sqlite3
import pandas as pd

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