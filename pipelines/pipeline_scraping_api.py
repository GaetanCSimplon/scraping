import requests
import json
import pandas as pd
from get_data.get_scraping_data import get_scraping_data_api, get_param_api, save_data_dict
from process_data.process_scraping import process_data_api
from database.insert_data import insert_api_data_to_db
import os

def run_scraping_api():

    print('\n Lancement du scraping...')
    BASE_URL = "https://www.googleapis.com/books/v1/volumes"
    param = get_param_api()
    data_books = get_scraping_data_api(BASE_URL, param)
    books_list = save_data_dict(data_books)
    print(f'{len(books_list)} livres extraits depuis l\'API.')
    print('\n Nettoyage des données...')
    df_books_list = process_data_api(books_list)
    print('\n Sauvegarde des données')
    os.makedirs("data", exist_ok=True)
    df_books_list.to_csv("data/books_api_cleaned.csv", index=False)
    print("\n Intégration des données dans la base de données...")
    insert_api_data_to_db(df_books_list)
    print('\n Insertion terminée.')
