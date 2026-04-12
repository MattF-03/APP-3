import time
import random
import csv   # On importe le module csv permettant de lire et manipuler des fichiers au format CSV
import os   # On importe le module os qui permet d'interagir avec le système d'exploitation

DOSSIER = "APP3_Fichiers"   # On crée une variable pour stocker le nom du dossier qui contient toutes les données

FICHIER_CANDIDATURES = os.path.join(DOSSIER, "parcoursup_small_10000.csv")   # On crée le chemin complet vers le fichier des vœux en assemblant le nom du dossier et le nom du fichier CSV

def extraire_candidatures(chemin_csv):   # On définit une fonction qui prend en entrée le chemin vers le fichier CSV
    candidatures = []   # On crée une liste vide pour stocker les données de tous les candidats
    if not os.path.exists(chemin_csv):   # On vérifie si le fichier spécifié est introuvable sur l'ordinateur
        return []
    with open(chemin_csv, newline = "", encoding = "utf-8") as file:   # On ouvre le fichier en mode lecture en s'assurant que tous les accents et les retours à la ligne s'affichent correctement
        for ligne in csv.DictReader(file):   # On parcourt chaque ligne du fichier en transformant les colonnes en clés de dictionnaire
            candidature = {}   # On crée un dictionnaire vide qui servira à stocker les informations d'un seul candidat à la fois
            for colonne, donnee in ligne.items():   # On parcourt chaque colonne de la ligne actuelle du CSV pour récupérer le nom de la colonne et la donnée associée
                candidature[colonne] = int(donnee)   # On transforme la donnée en nombre entier et on l'enregistre dans le dictionnaire candidatures 
            candidatures.append(candidature)
    return candidatures

def tri_insertion(liste, cle):   # On défnit une fonction de tri par insertion avec une règle de tri
    n = len(liste)
    for i in range(1, n):
        valeur = liste[i]
        j = i - 1
        while j >= 0 and cle(liste[j]) > cle(valeur):
            liste[j + 1] = liste[j]
            j = j - 1
        liste[j + 1] = valeur
    return liste

def tri_selection(liste, cle):   # On défnit une fonction de tri par sélection avec une règle de tri
    n = len(liste)
    for i in range(0, n - 1):
        minpos = i
        for j in range(i + 1, n):
            if cle(liste[j]) < cle(liste[minpos]):
                minpos = j
        liste[i], liste[minpos] = liste[minpos], liste[i]
    return liste

def tri_bulles(liste, cle):   # On défnit une fonction de tri à bulles
    n = len(liste)
    for i in range(n):
        for j in range(0, n - i - 1):
            if cle(liste[j]) > cle(liste[j + 1]):
                liste[j], liste[j + 1] = liste[j + 1], liste[j]
    return liste

def fusion(liste1, liste2, cle):   # On défnit une fonction qui fusionne deux listes triées avec une règle de tri
    liste = []
    i, j = 0, 0
    while i < len(liste1) and j < len(liste2):
        if cle(liste1[i]) < cle(liste2[j]):
            liste.append(liste1[i])
            i += 1
        else:
            liste.append(liste2[j])
            j += 1        
    while i < len(liste1):
        liste.append(liste1[i])
        i += 1 
    while j < len(liste2):
        liste.append(liste2[j])
        j += 1  
    return liste

def tri_fusion(liste, cle):   # On défnit une fonction de tri par fusion avec une règle de tri
    if len(liste) < 2:
        return liste[:]
    else:
        milieu = len(liste) // 2
        liste1 = tri_fusion(liste[:milieu], cle)
        liste2 = tri_fusion(liste[milieu:], cle)
        return fusion(liste1, liste2, cle)

def tri_rapide(liste, cle):   # On défnit une fonction de tri rapide avec une règle de tri
    if len(liste) < 2:
        return liste   
    e = liste[0]
    liste1, liste2 = [], []
    for x in liste[1:]:
        if cle(x) < cle(e):
            liste1.append(x)
        else:
            liste2.append(x)   
    return tri_rapide(liste1, cle) + [e] + tri_rapide(liste2, cle)

def mesurer_temps(nom_algorithme, liste_donnees, cle_tri):   # On définit une fonction qui prend en paramètres un algorithme, une liste à trier et une règle de tri
    copie = liste_donnees[:]
    debut = time.perf_counter()   # On enregistre l'instant précis où le tri débute
    nom_algorithme(copie, cle_tri)   # On exécute l'algorithme de tri passé en paramètre sur les données fournies
    fin = time.perf_counter()   # On enregistre l'instant précis où le tri se termine
    return fin - debut   # On renvoie la différence entre les deux temps pour obtenir la durée exacte de l'exécution

def comparer_algorithmes(candidatures, tailles = None):    # On définit une fonction qui sert à tester l'efficacité de chaque algorithme en changeant le nombre d'éléments à trier
    if tailles is None:   # Si la liste des tailles est vide
        tailles = [500, 1000, 2000, 5000, 10000]   # On définit par défaut une liste de cinq tailles croissantes pour l'analyse des performances
    
    def obtenir_score(candidat):   # On définit une fonction qui extrait la valeur du score dans chaque dictionnaire pour servir de base au classement
        return -candidat["score"]   # On renvoie le score du candidat avec un signe moins pour que le tri se fasse par ordre décroissant

    algorithmes = {   # On ouvre un dictionnaire pour stocker les noms des tris
        "Insertion" : tri_insertion,
        "Sélection" : tri_selection,
        "Bulles"    : tri_bulles,
        "Fusion"    : tri_fusion,
        "Rapide"    : tri_rapide
    }

    resultats = {}   # On crée un dictionnaire vide qui servira à stocker les listes de temps d'exécution pour chaque algorithme
    for nom in algorithmes:   # On parcourt un par un les noms des algorithmes enregistrés dans le dictionnaire de tris
        resultats[nom] = []   # On crée une liste vide associée à chaque nom d'algorithme 

    print(f"{"Taille":>10}  | ", end="")   # On affiche le nombre d'éléments à trier
    for nom in algorithmes:
        print(f"{nom:>14}", end="")   # On affiche chaque nom d'algorithme

    print("\n" + "-" * 88)

    for taille in tailles:   # On parcourt chaque taille contenu dans la liste des tailles à tester
        echantillon = random.sample(candidatures, taille)   # On prend au hasard un nombre de candidats dans la liste de candidats pour créer une petite liste de test
        print(f"{taille:>10}  | ", end="")   # On affiche les différentes taille 

        for nom, algo in algorithmes.items():   # On parcourt le dictionnaire algorithmes pour obtenir le nom du tri et la fonction correspondante
            if nom in ["Insertion", "Sélection", "Bulles"] and taille > 5000:   # On vérifie si l'algorithme est l'un des plus lents et si la taille des données dépasse 5 000 
                print(f"{"trop lent":>14}", end="")
                resultats[nom].append(None)   # On enregistre une valeur vide dans les résultats pour indiquer que le test a été ignoré
            else:
                duree = mesurer_temps(algo, echantillon, obtenir_score)   # On lance le chronomètre pour mesurer combien de secondes l'algorithme met à trier la liste
                resultats[nom].append(duree)   # On ajoute le temps mesuré à la liste des résultats 
                affichage = f"{duree:.4f}s"
                print(f"{affichage:>14}", end="")   # On affiche la durée de chaque tri 

        print()

    return resultats, tailles

if __name__ == "__main__":   # On vérifie que le fichier est exécuté directement et non importé
    print()
    print("Lecture du fichier CSV...")
    donnees = extraire_candidatures(FICHIER_CANDIDATURES)   # On appelle la fonction d'extraction pour enregistrer les informations du fichier CSV dans la variable donnees
    
    if not donnees:   # Si donnees est vide
        print(f"Erreur : Impossible de lire {FICHIER_CANDIDATURES}")
    else:
        print(f"{len(donnees)} candidatures enregistrées")
        print()
        comparer_algorithmes(donnees)   # On lance la fonction qui teste les différents tris et affiche le tableau des chronomètres
        print()
