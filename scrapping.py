from bs4 import BeautifulSoup
import requests
import csv

url = "https://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

books = soup.select('article > div > a')[0]['href']

url = "https://books.toscrape.com/" + books
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

book_title = soup.select('h1')[0].text
book_img = "books.toscrape.com" + soup.select("img")[0]["src"].replace('../..', '')
universal_product_code = soup.select('table > tr > td')[0].text
price_including_tax = soup.select('table > tr > td')[3].text.replace('Â','')
price_excluding_tax = soup.select('table > tr > td')[2].text.replace('Â','')
number_available = soup.select('table > tr > td')[5].text
product_description = soup.select('article > p')[0].text
category = soup.select('ul > li > a')[2].text
review_rating = soup.select('p')[2]['class'][1]


with open('CSV/livre.csv', 'w', newline='', encoding='utf-8') as fichier_csv:
    fieldnames = ["Product_Page_URL", "Universal_Product_Code", "Title", "Price_Including_Taxe", "Price_Excluding_Taxe", "Number_Available", "Product_Description", "Category", "Review_Rating", "Image_URL"]
    writer_csv = csv.DictWriter(fichier_csv, fieldnames=fieldnames)
    writer_csv.writeheader()
    writer_csv.writerow({
            "Product_Page_URL": url,
            "Universal_Product_Code": universal_product_code,
            "Title": book_title,
            "Price_Including_Taxe": price_including_tax,
            "Price_Excluding_Taxe": price_excluding_tax,
            "Number_Available": number_available,
            "Product_Description": product_description,
            "Category": category,
            "Review_Rating": review_rating,
            "Image_URL": book_img
        })