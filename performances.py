import time
import random
import os   # On importe le module os qui permet d'interagir avec le système d'exploitation
import matplotlib.pyplot as plt   # type: ignore     # On importe la bibliothèque matplotlib pour créer et afficher des graphiques
from tri import tri_insertion, tri_selection, tri_bulles, tri_fusion, tri_rapide
from read import extraire_candidatures

def cle_score(i):   # On définit une fonction qui sert de règle pour trier les dictionnaires par score
    return -i["score"]   # On renvoie un tri décroissant des scrores 

def mesurer_temps(algo, liste):   # On définit une fonction pour calculer la durée exacte d'un tri sur une liste donnée
    debut = time.perf_counter()   # On enregistre l'heure précise juste avant le début du tri
    copie_liste = liste[:]   # On cée une copie de la liste originale pour éviter que le tri ne la modifie définitivement
    resultat = algo(copie_liste, cle_score)   # On lance l'algorithme de tri sur la copie en utilisant la règle du score pour classer les éléments
    return time.perf_counter() - debut   # On calcule et renvoie la différence entre l'heure de fin et l'heure de début

def comparer_graphique(candidatures, tailles = None):   # On définit une fonction qui gère la création du graphique 
    if tailles is None:   # On vérifie si aucune liste de tailles n'a été fournie en entrée
        tailles = [100, 500, 1000, 2000, 5000, 10000]   # On définit les tailles de listes par défaut à tester

    algorithmes = {   # On crée un dictionnaire pour lier chaque nom de tri à sa fonction correspondante
        "Insertion" : tri_insertion,
        "Sélection" : tri_selection,
        "Bulles"    : tri_bulles,
        "Fusion"    : tri_fusion,
        "Rapide"    : tri_rapide
    }

    resultats = {}   # On initialise un dictionnaire vide pour stocker les temps de calcul obtenus
    for nom in algorithmes:   # On parcourt un par un les noms des méthodes de tri enregistrés dans le dictionnaire
        resultats[nom] = []   # On crée la liste des mesures pour un algorithme spécifique

    print()

    for taille in tailles:
        print(f"  Taille {taille}...")
        echantillon = random.sample(candidatures, min(taille, len(candidatures)))   # On prend aléatoirement un nombre de candidats égal à la taille actuelle

        for nom, algo in algorithmes.items():   # On parcourt chaque algorithme pour le tester sur l'échantillon actuel
            if nom in ("Insertion", "Sélection", "Bulles") and taille > 5000:   # On vérifie si le tri est trop lent pour les grosses listes
                resultats[nom].append(None)   # On enregistre une valeur vide dans les résultats pour indiquer que le tri a été ignoré car il est trop lent
            else:
                duree = mesurer_temps(algo, echantillon)   # On appelle la fonction de mesure pour obtenir le temps d'exécution
                resultats[nom].append(duree)   # On enregistre le temps trouvé dans la liste des résultats de l'algorithme

    print()
    
    couleurs = {   # On associe une couleur spécifique à chaque algorithme pour les distinguer sur le dessin
        "Insertion" : "red",
        "Sélection" : "orange",
        "Bulles"    : "gold",
        "Fusion"    : "green",
        "Rapide"    : "blue"
    }

    for nom, durees in resultats.items():   # On parcourt le nom de chaque algorithme et la liste des temps d'exécution qui lui sont associés

        tailles_graphique = []   # On crée une liste vide pour stocker les tailles d'échantillons à afficher sur l'axe x
        durees_graphique = []   # On crée une liste vide pour stocker les temps d'exécution correspondants sur l'axe y

        for i in range(len(tailles)):   # On parcourt les indices de la liste des tailles pour traiter chaque mesure une par une
            duree = durees[i]   # On récupère la durée de tri enregistrée pour l'indice actuel
            taille = tailles[i]   # On récupère la taille de l'échantillon correspondante à l'indice
    
            if duree is not None:   # On vérifie que la mesure existe et qu'elle n'a pas été sautée car trop lente
                tailles_graphique.append(taille)   # On ajoute la taille à la liste finale pour qu'elle soit tracée sur le graphique
                durees_graphique.append(duree)   # On ajoute la durée à la liste finale pour qu'elle soit tracée sur le graphique

        plt.plot(tailles_graphique, durees_graphique, label = nom, color = couleurs[nom], marker = "o")   
        # On dessine une courbe en reliant les points définis par les tailles et les durées, en utilisant le nom du graphique, la couleur de la courbe et la forme du point sur le graphique

    plt.title("Comparaison des algorithmes de tri")   # On affiche le titre en haut du graphique
    plt.xlabel("Nombre d'éléments")   # On affiche le nom de l'axe horizontal (le nombre d'éléments)
    plt.ylabel("Temps (secondes)")   # On affiche le nom de l'axe vertical (le temps en secondes)
    plt.legend()   # On affiche la légende du graphique
    plt.grid(True)   # On affiche un quadrillage en arrière-plan pour faciliter la lecture des valeurs
    plt.tight_layout()   # On ajuste les marges pour que tout soit bien visible
    plt.show()   # On ouvre une fenêtre contextuelle pour afficher le résultat visuel final

if __name__ == "__main__":   # On vérifie que le fichier est exécuté directement et non importé
    chemin = os.path.join("APP3_Fichiers", "parcoursup_small_10000.csv")   # On construit le chemin d'accès vers le fichier de candidatures
    candidatures = extraire_candidatures(chemin)   # On enregistre les données réelles de Parcoursup dans la variable candidatures
    comparer_graphique(candidatures)   # On lance toute la procédure de test et de génération du graphique
