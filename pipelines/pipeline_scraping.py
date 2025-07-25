import pandas as pd
from get_data.get_scraping_data import scrape_books
from process_data.process_scraping import convert_types
from database.insert_data import insert_data_to_db
import os

def run_scraping_pipeline(nb_books):
    print("Lancement du scraping...")
    scraped_data = scrape_books(nb_books)
    df = pd.DataFrame(scraped_data)
    print(f'Scraping terminé : {len(df)} livres récupérés')
    print('Nettoyage et conversion des données...')
    df_clean = convert_types(df)
    print((f'Données nettoyées. {len(df_clean)} livres sauvegardés après traitements'))
    print(" Sauvegarde des données brutes dans un fichier CSV...")
    os.makedirs("data", exist_ok=True)  # Crée le dossier s'il n'existe pas
    raw_csv_path = "data/data_scraping.csv"
    df_clean.to_csv(raw_csv_path, index=False)
    print(f" Données sauvegardées dans : {raw_csv_path}")

    print(" Insertion des données en base SQLite...")
    insert_data_to_db(csv_path=raw_csv_path)
    print(" Insertion terminée.")

    print(" Pipeline complet exécuté avec succès !")


