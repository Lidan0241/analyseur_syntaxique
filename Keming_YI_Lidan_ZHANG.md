# Projet Calculabilité, Module 1

## **Spécification des Interfaces et Organisation des Modules**

### Keming YI, Lidan ZHANG

**1. Module de Lecture (lecture.py)**

•	**Fonction** : Ouvre le fichier source du programme MTddV et lit le contenu.

•	**Interface** :

•	**Fonction** : `ouvrir_fichier(nom_fichier: str) -> str`

•	**Paramètre** : `nom_fichier (str)` – Le nom ou chemin du fichier source MTddV.

•	**Retour** : Une chaîne de caractères contenant le texte brut du programme MTddV.

•	**Librairies Utilisées** : Nous utilisons uniquement les fonctionnalités intégrées de Python pour lire les fichiers (open).

•	**Description** : Cette fonction vérifie si le fichier existe, puis le lit en mode texte et retourne le contenu en une seule chaîne.

**2. Module d’Analyse Lexicale et Syntaxique (analyseur.py)**

•	**Fonctionnalité** : Segmente le texte en unités lexicales (tokens) et vérifie la structure syntaxique du programme.

•	**Interfaces** :

•	**Fonction** : `analyse_lexicale(contenu: str) -> list`

•	**Paramètre** : `contenu (str)` – Le texte brut du programme MTddV.

•	**Retour** : Une liste de tokens, chacun représenté sous forme de tuple (type_token, valeur_token).

•	**Fonction** : `analyse_syntaxique(tokens: list) -> dict`

•	**Paramètre** : `tokens (list)` – Liste des tokens générés par l’analyse lexicale.

•	**Retour** : Un dictionnaire représentant la structure syntaxique sous forme d’arbre.

•	**Librairies Utilisées** : Le module re (expressions régulières) pour l’analyse lexicale.

•	**Pourquoi cette librairie** re : re est léger et permet d’extraire les tokens en fonction des motifs syntaxiques définis pour le langage MTddV.

•	**Description des Fonctions** :

•	`analyse_lexicale` : Cette fonction utilise des expressions régulières pour identifier les types de tokens : mots-clés, variables, opérateurs, etc. Elle parcourt le texte et génère une liste de tokens.

•	`analyse_syntaxique` : Cette fonction prend la liste de tokens et construit un arbre syntaxique pour représenter les structures imbriquées du programme (par exemple, boucles et conditions). Elle implémente les règles de grammaire de MTddV.

**3. Module de Sortie (ecriture.py)**

•	**Fonction** : Exporte l’arbre syntaxique généré au format JSON.

•	**Interfaces** :

•	**Fonction** : `ecrire_sortie(structure: dict, nom_fichier: str) -> None`

•	**Paramètres** :

•	`structure (dict)` – La structure syntaxique sous forme d’arbre générée par l’analyseur syntaxique.

•	`nom_fichier (str)` – Le nom du fichier de sortie.

•	**Retour** : Aucun. La fonction écrit dans un fichier.

•	**Les librairies utilisées** : json pour un format lisible par les machines et facilement manipulable par d’autres applications.

•	**Pourquoi ce format** json : JSON est un format standard qui permet de structurer les données de manière hiérarchique. C’est un bon choix pour représenter des arbres syntaxiques.