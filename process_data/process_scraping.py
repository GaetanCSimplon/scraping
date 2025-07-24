import pandas as pd

def convert_availability(value : str) -> bool:
    """Convert the availability value to a boolean.

    Args:
        value (str): The availability status of the book.

    Returns:
        bool: True if the book is available, False otherwise.
    """
    if value == 'In stock':
        return True
    else:
        return False

def convert_types(df_books: pd.DataFrame) -> pd.DataFrame:
    """Convert the types of the DataFrame columns to appropriate types.

    Args:
        df_books (pd.DataFrame): The DataFrame containing book data.

    Returns:
        pd.DataFrame: The DataFrame with converted types.
    """
    
    # Convertir en str
    df_books["title"] = df_books["title"].astype(str)

    # Nettoyer les prix (enlever le symbole £ et les caractères parasites) puis convertir en float
    df_books["price"] = df_books["price"].str.replace('£', "", regex=False)
    df_books["price"] = df_books["price"].str.replace('Â', "", regex=False)
    df_books["price"] = df_books["price"].str.strip()
    df_books["price"] = pd.to_numeric(df_books["price"], errors="coerce")
    df_books["price"] = df_books["price"].astype(float)
    
    # Convertir la disponibilité en booléen
    df_books["availability"] = df_books["availability"].apply(convert_availability)

    # Mapper les notes en chiffres
    ratings_map = {
        'Zero': 0,
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
    df_books["rating"] = df_books["rating"].map(ratings_map)

    

    return df_books