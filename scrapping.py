from bs4 import BeautifulSoup
import requests
import re
import csv
import os

url = "https://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

create_directory('images')
create_directory('CSV')

def getBookData(soup, url) :
    """
    Extrait les données d'un livre à partir de l'objet BeautifulSoup et de l'URL donnés.

    Args:
        soup (BeautifulSoup): L'objet BeautifulSoup contenant le contenu HTML du livre.
        url (str): L'URL de la page du livre.

    Returns:
        dict: Un dictionnaire contenant les données du livre, y compris :
            - Product_Page_URL (str): L'URL de la page du livre.
            - Universal_Product_Code (str): Le code produit universel du livre.
            - Title (str): Le titre du livre.
            - Price_Including_Taxe (str): Le prix du livre taxes comprises.
            - Price_Excluding_Taxe (str): Le prix du livre hors taxes.
            - Number_Available (str): Le nombre d'exemplaires disponibles.
            - Product_Description (str): La description du livre.
            - Category (str): La catégorie du livre.
            - Review_Rating (str): La note de critique du livre.
            - Image_URL (str): L'URL de l'image du livre.
    """
    book_url = url
    book_title = soup.select('h1')[0].text
    book_img = "https://books.toscrape.com" + soup.select("img")[0]["src"].replace('../..', '')
    universal_product_code = soup.select('table > tr > td')[0].text
    price_including_tax = soup.select('table > tr > td')[3].text.replace('Â','')
    price_excluding_tax = soup.select('table > tr > td')[2].text.replace('Â','')
    number_available_text = soup.select('table > tr > td')[5].text
    number_available = re.search(r'\d+', number_available_text).group()
    product_description = soup.select('article > p')[0].text
    category = soup.select('ul > li > a')[2].text
    review_rating = soup.select('p')[2]['class'][1]


    return {
        "Product_Page_URL": book_url,
        "Universal_Product_Code": universal_product_code,
        "Title": book_title,
        "Price_Including_Taxe": price_including_tax,
        "Price_Excluding_Taxe": price_excluding_tax,
        "Number_Available": number_available,
        "Product_Description": product_description,
        "Category": category,
        "Review_Rating": review_rating,
        "Image_URL": book_img
    }

def getCategoryBooks(soup, url, category_number,category_folder, category_name):
    """
    Extrait les données des livres pour tous les livres d'une catégorie donnée et les écrit dans un fichier CSV.

    Args:
        soup (BeautifulSoup): L'objet BeautifulSoup contenant le contenu HTML de la page principale.
        url (str): L'URL de base du site.
        category_number (int): L'index de la catégorie à scraper.

    """
    try:
        category_url = url + soup.select("ul > li > a")[category_number]["href"]
        response = requests.get(category_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        dataBook = []

        while True :
            book = soup.select("article > div > a")
            nextButton = soup.find("li", class_="next")
            for i in range(len(book)):
                book_url = "https://books.toscrape.com/catalogue/" + book[i]['href'].replace('../../../', '')
                response = requests.get(book_url)
                book_soup = BeautifulSoup(response.content, 'html.parser')
                dataBook.append(getBookData(book_soup, book_url))
            
            if nextButton :
                next_link = nextButton.find('a')['href']
                response = requests.get(category_url.rsplit('/',1)[0] +'/'+ next_link)
                soup = BeautifulSoup(response.content, 'html.parser')
            else :
                break

        for book in dataBook:
            book_img = book["Image_URL"]
            img_response = requests.get(book_img)
            img_name = re.sub(r'[^\w\s-]', '', book["Title"]) + '.jpg'
            img_name = img_name.replace(' ', '_')
            with open(f'{category_folder}/{img_name}', 'wb') as img_file:
                img_file.write(img_response.content)
    except Exception as e:
        print(f"Failed : {e}")
        img_name = "N/A"

    csv_file = f'CSV/{category_name}.csv'   
    with open(csv_file, 'w', newline='', encoding='utf-8') as fichier_csv:
        fieldnames = ["Product_Page_URL", "Universal_Product_Code", "Title", "Price_Including_Taxe", "Price_Excluding_Taxe", "Number_Available", "Product_Description", "Category", "Review_Rating", "Image_URL"]
        writer_csv = csv.DictWriter(fichier_csv, fieldnames=fieldnames)
        writer_csv.writeheader()
        writer_csv.writerows(dataBook)

def getAllCategories(soup, url):
    """
    Extrait toutes les catégories de livres disponibles et les scrape.

    Args:
        soup (BeautifulSoup): L'objet BeautifulSoup contenant le contenu HTML de la page principale.
        url (str): L'URL de base du site.

    Returns:
        None
    """
    try:
        categories = soup.select("ul > li > a")
        for category_number in range(2, len(categories)):
            category_name = categories[category_number].text.strip().replace(' ', '_').replace('/', '_').replace(':', '_')
            category_folder = os.path.join('images', category_name)
            create_directory(category_folder)
            getCategoryBooks(soup, url, category_number, category_folder, category_name)
    except Exception as e:
        print(f"Erreur lors de l'extraction des catégories: {e}")
        return []

getAllCategories(soup, url)
