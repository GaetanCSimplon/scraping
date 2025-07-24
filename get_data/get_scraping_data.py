import requests
from bs4 import BeautifulSoup
import pandas as pd

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

