from pipelines.pipeline_scraping import run_scraping_pipeline
from pipelines.pipeline_scraping_api import run_scraping_api

choice = int(input('Recherche sur un site web ou Google Books ?' ' ' '1 / 2 ' ))

if choice == 1:
    nb_books = int(input("Combien de pages souhaitez-vous parcourir ? "))
    run_scraping_pipeline(nb_books)
elif choice == 2:
    run_scraping_api()
else:
    choice = int(input('Veuillez saisir 1 pour Web / 2 pour Google Books. '))
