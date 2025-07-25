import requests
from bs4 import BeautifulSoup


def get_books_html(url: str) -> BeautifulSoup:
    """Fetch the HTML content of a book page.

    Args:
        url (str): The URL of the book page.

    Returns:
        BeautifulSoup: A BeautifulSoup object containing the HTML content.
    """
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup
# Extraction de données à partir d'un site web
def extract_title(book: BeautifulSoup) -> str:
    """Extract the title of a book from a BeautifulSoup object.

    Args:
        book (BeautifulSoup): The HTML element of the book.

    Returns:
        str: The title of the book.
    """
    return book.find('h3').find('a')['title']
def extract_price(book: BeautifulSoup) -> str:
        
        """Extract the price of a book from a BeautifulSoup object.

    Args:
        book (BeautifulSoup): The HTML element of the book.

    Returns:
        str: The price of the book.

    """
        return book.find('p', class_='price_color').text
def extract_rating(book: BeautifulSoup) -> str:
        """Extract the rating of a book from a BeautifulSoup object.

    Args:
        book (BeautifulSoup): The HTML element of the book.

    Returns:
        str: The rating of the book.
    """
        return book.find('p', class_='star-rating')['class'][1]
def extract_availability(book: BeautifulSoup) -> str:
        """Extract the availability of a book from a BeautifulSoup object.

    Args:
        book (BeautifulSoup): The HTML element of the book.

    Returns:
        str: The availability of the book.
    """
        return book.find('p', class_='instock availability').text.strip()
def extract_book_info(book: BeautifulSoup) -> dict:
        """Extract all information of a book from a BeautifulSoup object.

    Args:
        book (BeautifulSoup): The HTML element of the book.

    Returns:
        dict: A dictionary containing the title, price, rating, and availability of the book.
    """
        livre = {
            'title': extract_title(book),
            'price': extract_price(book),
            'rating': extract_rating(book),
            'availability': extract_availability(book)
        }
        return livre
def scrape_books(pages: int) -> list[dict]:

    """Scrape books from the specified number of pages.

    Args:
        pages (int): The number of pages to scrape.

    Returns:
        list: A list of dictionaries containing books information.
    """
    base_url = "http://books.toscrape.com/catalogue/page-{}.html" # Url de base du catalogue
    all_books = [] # Création d'une liste qui contiendra les dictionnaires scrapés
    for page_num in range(1, pages +1): # Boucle pour parcourir les pages
        url = base_url.format(page_num) # format() permet de substituer une valeur entre accolade, ici c'est le numéro de page dans le base_url
        soup = get_books_html(url)
        books = soup.find_all('article', class_='product_pod')
        data_books = [extract_book_info(book) # comprehensive list qui permet l'extraction des informations
                      for book
                      in books]
        all_books.extend(data_books) # extend() pour ajouter les informations scrapés dans la liste all_books
    return all_books

# Extraction de données à partir de l'API Google Books

def get_param_api():
    print("Paramètres de recherche...")
# Demande des termes de recherche
    title = input("Que recherchez-vous ? (titre, auteur...) ").strip()
    while not title:
        print('\n Veuillez saisir votre recherche \n')
        title = input("\n Que recherchez-vous ? (titre, auteur...) ").strip()

# Demande du type de format
    while True:
        printType = input("Quel format d'ouvrage ? 'all' / 'books' / 'magazines' ").lower().strip()
        match printType:
            case 'books' | 'magazines' | 'all':
                break
            case _:
                print("Veuillez saisir l'une des trois valeurs proposées" )
# Demande du nombre de résultats
    while True:
        max_results = input('Combien de résultats souhaitez-vous ? (min. 1 / max: 40) ').strip()
        if max_results == "":
            max_results = 10
            break
        elif max_results.isdigit() and 1 <= int(max_results) <= 40:
            max_results = int(max_results)
            break
        else:
            print('Veuillez renseigner un nombre compris entre 1 et 40. ')


    param = {
    'q': title,
    'printType': printType,
    'filter': 'paid-ebooks',
    'maxResults': max_results,
    'orderBy': 'relevance'
    }

    return param
def get_scraping_data_api(BASE_URL, param):
    response = requests.get(BASE_URL, params=param)
# Récolte de l'ensemble de données des livres recherchés
    data_books_raw = response.json()
# Ciblage de la partie 'items' contenant les données à récolter
    data_books = data_books_raw['items']
    for book in data_books:
        volume = book.get('volumeInfo', {})
        sale = book.get('saleInfo', {})
        title = volume.get('title')
        price = sale.get('listPrice', {}).get('amount')
        rating = volume.get('averageRating')
# Affichage des valeurs
        print(f'Titre : {title}')
        print(f'Prix : {price}')
        print(f'Note moyenne : {rating}')
    return data_books

def save_data_dict(data_books):
    # Création d'une liste de dictionnaires pour les livres
    books_list = []

    for book in data_books:
        volume = book.get('volumeInfo', {})
        sale = book.get('saleInfo', {})
        title = volume.get('title')
        price = sale.get('listPrice', {}).get('amount')
        rating = volume.get('averageRating')

        book_dict = {
        'title': title,
        'price': price,
        'rating': rating
    }
        books_list.append(book_dict)
    return books_list