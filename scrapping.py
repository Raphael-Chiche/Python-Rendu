from bs4 import BeautifulSoup
import requests
import re
import csv

url = "https://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


def getBookData(soup, url) :
    book_url = url
    book_title = soup.select('h1')[0].text
    book_img = "books.toscrape.com" + soup.select("img")[0]["src"].replace('../..', '')
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

def getCategoryBooks(soup, url, category_number):
    try:
        category_url = url + soup.select("ul > li > a")[category_number]["href"]
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        dataBook = []

        while True :

            book = soup.select("article > div > a")
            nextButton = soup.find("li", class_="next")

            for i in range(len(book)):
                url = "https://books.toscrape.com/catalogue/" + book[i]['href'].replace('../../../', '')
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                dataBook.append(getBookData(soup, url))
            

            if nextButton :
                next_link = nextButton.find('a')['href']
                response = requests.get(category_url.rsplit('/',1)[0] +'/'+ next_link)
                soup = BeautifulSoup(response.text, 'html.parser')
            else :
                break
    except:
        print(f"La catégorie {category_number} n'existe pas.")
        return []
    
   
    with open('CSV/livre.csv', 'w', newline='', encoding='utf-8') as fichier_csv:
        fieldnames = ["Product_Page_URL", "Universal_Product_Code", "Title", "Price_Including_Taxe", "Price_Excluding_Taxe", "Number_Available", "Product_Description", "Category", "Review_Rating", "Image_URL"]
        writer_csv = csv.DictWriter(fichier_csv, fieldnames=fieldnames)
        writer_csv.writeheader()
        writer_csv.writerows(dataBook)


        
            
    # return tabBook


getCategoryBooks(soup, url, 33)

