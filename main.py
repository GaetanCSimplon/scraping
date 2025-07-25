from pipelines.pipeline_scraping import run_scraping_pipeline

nb_books = int(input("Combien de pages souhaitez-vous parcourir ? "))
run_scraping_pipeline(nb_books)
