# Oracle
## Description
### Fonctions

Oracle (ORACLE Repère, Accepte et Consulte les Liens Etonnants) est un bot IRC Dont la principale fonction est de rester sur un ou plusieurs channels et de stocker dans une base de données sqlite3 les URLs qu'elle repère.

* Repère les URLs
* Les stocke dans une base de données paramétrable.
* Permet aux utilisateurs présent sur un channel IRC de taguer les liens
* Permet la recherche directement via le channel IRC 

De plus, Oracle est accompagnée de Dodone (DODONE Ordonne les Données d'Oracle Naturellement Éparpillées) et d'une interface Web installable permettant la consultation publique des liens, ainsi que de leurs tags associés.
Dodone se charge quand à lui de fusionner deux bases de données d'Oracle.
Trivia

Oracle est nommée d'après  Barbara Gordon, Batgirl paraplégique, jouant le rôle de spécialiste du renseignement pour Batman.
## Usage
### Principe de fonctionnement

Oracle fonctionne selon le mécanisme suivant:
La dernière URL affichée est l'URL "active". Toutes les commandes vont s'appliquer à celles-ci
Commandes

Les commandes d'Oracle sont les suivantes:

    !help : Affiche l'aide.
    !version : Affiche la version d'Oracle.
    !delete : Supprime la dernière URL ajoutée ou consultée.
    !delete url : Supprime URL.
    !+ tag1 tag2 : Ajoute tag1 et tag2 à la derniere URL ajoutée ou consultée.
    !- tag1 tag2 : Retire tag1 et tag2 de la derniere URL ajoutée ou consultée.
    !search tag1 tag2 : Cherche les liens tagués tag1 ET tag2.
    !last : Affiche le dernier lien.
    !stop : Stops URL watching.
    !start : Starts URL watching.
    !goto #foo : joint le channel #foo.
    !quit : quitte le channel actif. 

## Installation

Pour l'instant, Oracle est uniquement compatible Linux et consorts.
Lancement du Bot IRC

### Cas Oracle <= v1.3.2

Une utilisation typique serait: python2.7 /path/to/Oracle.py irc.server.tld \#channel Oracle /chemin/vers/databasefile
petite explications des paramètres passés à Oracle.py:

    irc.server.tld : Le serveur IRC auquel Oracle doit se connecter. ATTENTION: Oracle n'est pas multi serveurs!
    \#channel : le channel initial qu'Oracle doit rejoindre. ALT: \#channel1,\#channel2
    Oracle : Pseudo à utiliser.
    /chemin/vers/databasefile : fichier de base de donné sqlite3 à utiliser. Par défaut à ~/.Oracle/Oracle?.sq3 . 

### Oracle >= 1.4.0

La configuration se fait maintenant via un fichier de configuration, Oracle.cfg , quoi doit être placé dans le même répertoire que Oracle.py

Lors de son premier lancement, Oracle génèrera les sections nécessaires à son fonctionnement. Voici le contenu du fichier par défaut:

    [connection]
    network = irc.example.tld      # Adresse du serveur irc
    channels = #foo,#bar           # Channels à joindre au lancement
    name = Oracle                  # NICK/USER à utiliser
    dbpath = Oracle.sq3            # Chemin vers la db

    [misc]
    ignore =                       # si des domaines souhaitent être ignorés, les mettre ici, séparés par une virgule. Exemple: 4chan.org,9gag.com

### Installation de l'interface Web

Copier les fichiers du dossier web dans le dossier correspondant de votre serveur web
Éditer le fichier config.php pour adapter à vos besoins. Il est important de configurer le bon chemin d'accès vers la base de données. 
