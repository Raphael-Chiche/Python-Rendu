Pour démarrer l'environnement de développement il faut : 
env/Scripts/activate

Installer les modules avec requirements.txt : 
pip install -r requirements.txt

Lancer le script présent dans app.py


PHASE 1 : 
Récupération de l'URL de la page d'un livre depuis la page d'accueil.
Une fois l'URL obtenue, je récupère toutes les informations nécessaires sur le livre.
J'ajoute toutes ces informations dans un fichier CSV nommé livre.csv.

PHASE 2 :
Récupération d'une catégorie depuis la page d'accueil.
Une fois l'URL obtenue, je récupère tous les livres puis toutes les informations nécessaires sur les livres.
J'ajoute toutes ces informations dans un fichier CSV.

PHASE 3 :
Création du dossier images.
Récupération de l'url et du titre de l'image.
Téléchargement de l'image.

PHASE 4 :
Récupération de chaque catégorie depuis la page d'accueil.
Une fois l'URL obtenue, je récupère tous les livres de toutes les catégories puis toutes les informations nécessaires sur les livres.
J'ajoute toutes ces informations dans un dossier CSV avec le fichier csv avec le bon nom.
Création du dossier images.
Récupération de l'url et du titre de l'image.
Téléchargement de l'image dans un dossier de la catégorie.
