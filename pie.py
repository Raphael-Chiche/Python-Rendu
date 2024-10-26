import os
import csv
import matplotlib.pyplot as plt

csv_folder = 'CSV'

csv_files = []
for f in os.listdir(csv_folder):
    if f.endswith('.csv'):
        csv_files.append(f)

        
category_counts = {}
category_prices = {}

for csv_file in csv_files:
    category_name = os.path.splitext(csv_file)[0]
    csv_path = os.path.join(csv_folder, csv_file)
    
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        row_count = 0
        total_price = 0.0
        for row in reader:
            row_count += 1
            total_price += float(row['Price_Including_Taxe'].replace('£', ''))
        category_counts[category_name] = row_count
        if row_count > 0:
            category_prices[category_name] = total_price / row_count

def plot_pie_chart(data):
    """
    Crée un diagramme circulaire montrant la répartition des livres par catégorie.

    Args:
        data (dict): Un dictionnaire contenant le nombre de livres par catégorie.
    """
    labels = data.keys()
    sizes = data.values()

    plt.figure(figsize=(10, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=0)
    plt.title('Répartition des livres par catégorie')
    plt.show()

def plot_average_price_bar_chart(data):
    """
    Crée un graphique en barres représentant le prix moyen des livres par catégorie.

    Args:
        data (dict): Un dictionnaire contenant le prix moyen des livres par catégorie.
    """
    categories = list(data.keys())
    average_prices = list(data.values())

    plt.figure(figsize=(10, 6))
    plt.bar(categories, average_prices, color='skyblue')
    plt.xlabel('Catégories')
    plt.ylabel('Prix moyen (£)')
    plt.title('Prix moyen des livres par catégorie')
    plt.xticks(rotation=45, ha='right') 
    plt.tight_layout()  
    plt.show()

plot_pie_chart(category_counts)
plot_average_price_bar_chart(category_prices)