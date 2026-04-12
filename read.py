import csv   # On importe le module csv permettant de lire et manipuler des fichiers au format CSV
import os   # On importe le module os qui permet d'interagir avec le système d'exploitation

DOSSIER = "APP3_Fichiers"   # On crée une variable pour stocker le nom du dossier qui contient toutes les données
 
FICHIER_CANDIDATURES = os.path.join(DOSSIER, "parcoursup_small_10000.csv")   # On crée le chemin complet vers le fichier des vœux en assemblant le nom du dossier et le nom du fichier CSV
FICHIER_FORMATIONS = os.path.join(DOSSIER, "parcoursup_programs_small_800.csv")   # On paramètre le lien vers le fichier des formations pour faciliter la lecture par le programme

def extraire_candidatures(chemin_csv):   # On définit une fonction pour extraire la liste de tous les vœux des étudiants depuis un fichier
    candidatures = []   # On crée une liste vide pour stocker les dictionnaires de chaque candidature
    with open(chemin_csv, newline = "", encoding = "utf-8") as file:   # On ouvre le fichier en mode lecture en s'assurant que tous les accents et les retours à la ligne s'affichent correctement
        for ligne in csv.DictReader(file):   # On convertit chaque donnée de la ligne en nombre entier int
            candidature = {}   # On crée un dictionnaire vide pour stocker les informations du vœu en cours de lecture
            for cle, valeur in ligne.items():   # On analyse tour à tour chaque couple "nom de colonne" et "donnée" présent dans la ligne
                candidature[cle] = int(valeur)   # On transforme la donnée textuelle en nombre entier et on l'enregistre dans notre dictionnaire sous le bon nom
            candidatures.append(candidature)   # On ajoute le dictionnaire à la liste qui regroupe tous les vœux des étudiants
    return candidatures

def extraire_formations(chemin_csv):   # On définit une fonction qui va traiter le fichier des formations pour en extraire les informations essentielles
    with open(chemin_csv, newline = "", encoding = "utf-8") as file:
        capacites = {}   # On initialise un dictionnaire vide qui servira à stocker les places disponibles par formation
        for ligne in csv.DictReader(file):
            id_formation = int(ligne["program_id"])   # On récupère l'identifiant de la formation et on le transforme en nombre entier pour pouvoir l'utiliser comme clé
            nombre_places = int(ligne["capacity"])   # On récupère le nombre de places disponibles et on le convertit en nombre entier
            capacites[id_formation] = nombre_places   # On enregistre dans le dictionnaire le nombre de places correspondant à l'identifiant de la formation
    return capacites

def afficher_candidature(i):   # On définit une fonction qui va affihcer les informations détaillées d'une candidature passée en paramètre
    print(f"  Candidat ID    : {i["candidate_id"]}")   # On affiche l'identifiant de l'étudiant
    print(f"  Formation ID   : {i["program_id"]}")   # On affiche le code de la formation pour laquelle le vœu a été fait
    print(f"  Score          : {i["score"]}")   # On affiche le score obtenu par le candidat pour ce vœu

    heures = i["timestamp"] // 60
    minutes = i["timestamp"] % 60

    print(f"  Timestamp      : {heures}h {minutes:02d}min")   # On affiche l'heure du dépôt du vœu
    
    if i['is_scholarship'] == 1:   # Si le candidat est boursier
        print("  Boursier       : Oui")
    else:
        print("  Boursier       : Non")
        
    print(f"  Lycée (hs_id)  : {i['hs_id']}")   # On affiche l'identifiant du lycée d'origine de l'élève

def rechercher_par_candidat(candidatures, id_candidature):   # On définit une fonction qui reçoit la liste de tous les vœux et l'identifiant du candidat recherché
    resultats = []   # On crée une liste vide pour stocker les vœux appartenant au candidat précis
    for i in candidatures:   # On parcourt un par un tous les vœux présents dans les dictionnaires de chaque candidat 
        if i["candidate_id"] == id_candidature:   # On vérifie si l'identifiant du candidat dans le vœu actuel correspond à celui que l'on cherche
            resultats.append(i)   # On ajoute le vœu dans la liste de résultats
    return resultats

def rechercher_par_formation(candidatures, id_formation):   # On définit une fonction qui reçoit la liste des vœux et l'identifiant de la formation visée
    resultats = []   # On crée une liste vide pour stocker les candidatures liées à la formation précise
    for i in candidatures:
        if i["program_id"] == id_formation:   # On vérifie si l'identifiant de la formation dans le vœu est bien celui que l'on a précisé
            resultats.append(i)   # On enregistre le vœu dans notre sélection de candidatures
    return resultats

def grouper_par_formation(candidatures):   # On définit une fonction pour organiser tous les vœux en les regroupant par formation
    groupes = {}   # On crée un dictionnaire vide qui contiendra les formations et la liste des candidats 
    for i in candidatures:
        id_formation = i["program_id"]   # On récupère l'identifiant de la formation concernée par le vœu
        if id_formation not in groupes:   # On vérifie si c'est la première fois qu'on rencontre la formation dans le dictionnaire
            groupes[id_formation] = []   # On prépare une liste vide pour contenir les futurs candidats de la formation
        groupes[id_formation].append(i)   # On ajoute le vœu actuel dans la liste correspondant à la formation     
    return groupes

def statistiques(candidatures):   # On définit une fonction qui va analyser la liste des vœux reçue en paramètre
    total = len(candidatures)   # On compte le nombre total de vœux présents dans la liste 
    if total == 0:   # Si la liste est vide
        print("Aucune donnée")   # On affiche un message d'erreur 
        return   # On arrête la fonction avec return pour ne pas exécuter la suite du code inutilement

    formations_vues = []   # On crée une liste vide qui va stokcer les formations déjà rencontrées
    for i in candidatures:
        id_formation = i["program_id"]
        if id_formation not in formations_vues:   # On vérifie si l'identifiant n'est pas déjà présent dans la liste
            formations_vues.append(id_formation)
    nombre_formations = len(formations_vues)   # On compte combien d'identifiants différents sont dans la liste pour obtenir le nombre total de formations

    candidats_vus = []   # On crée une liste vide pour noter les identifiants des candidats déjà comptés
    for i in candidatures:
        id_candidature = i["candidate_id"]
        if id_candidature not in candidats_vus:   # On regarde si l'étudiant a déjà été enregistré lors d'un vœu précédent
            candidats_vus.append(id_candidature)
    nombre_candidats = len(candidats_vus)   # On compte la taille de la liste pour savoir combien d'étudiants distincts ont postulé

    nombre_boursiers = 0   # On crée une variable qui compte le nombre de boursiers en la mettant à zéro pour débuter le calcul
    for i in candidatures:
        if i["is_scholarship"] == 1:   # Si le candidat est boursier
            nombre_boursiers += 1

    print("\n===  STATISTIQUES GÉNÉRALES ===")
    print()
    print(f"  Nombre total de vœux  : {total}")
    print(f"  Nombre de formations  : {nombre_formations}")
    print(f"  Nombre de candidats   : {nombre_candidats}")
    pourcentage = (100 * nombre_boursiers) / total   # On calcule le pourcentage de boursiers parmi l'ensemble des candidats
    print(f"  Nombre de boursiers   : {nombre_boursiers} ({pourcentage:.1f} %)")   # On affiche le nombre de boursiers et de leur pourcentage 

if __name__ == "__main__":   # On vérifie si le script est lancé directement et non importé 
    print()
    print("=== ÉVALUATION DU PROGRAMME ===")
    print()
    print(f"Dossier actuel : {os.getcwd()}")   # On affiche le chemin du dossier où le programme est en train de s'exécuter
 
    if not os.path.exists(FICHIER_CANDIDATURES):   # On vérifie si le fichier contenant les candidatures est absent du dossier
        print(f"ERREUR : '{FICHIER_CANDIDATURES}' introuvable")
        print(f"Fichiers visibles : {os.listdir()}")   # On liste tous les fichiers présents dans le dossier actuel pour à trouver l'erreur
        if os.path.exists(DOSSIER):   # On vérifie si le dossier spécifié dans la variable DOSSIER existe 
            print(f"Contenu de {DOSSIER} : {os.listdir(DOSSIER)}")   # On affiche la liste des fichiers contenus à l'intérieur du dossier spécifique
    else:
        print("Fichier trouvé ! Lecture en cours...")
        candidatures = extraire_candidatures(FICHIER_CANDIDATURES)   # On appelle la fonction extraire_candidatures pour enregistrer les données du fichier dans la variable candidatures
 
        if len(candidatures) == 0:   # On vérifie si la liste des candidatures ne contient aucun élément
            print("Le fichier est vide")
        else:
            print(f"{len(candidatures)} lignes lues avec succès")
            statistiques(candidatures)   # On lance la fonction qui calcule et affiche les statistiques
 
            print("\n=== EXEMPLE : premier candidat ===")
            print()
            afficher_candidature(candidatures[0])   # On appelle la fonction afficher_candidature pour voir les détails du premier dossier de la liste
 
            print("\n=== EXEMPLE : recherche candidat ID 300 ===")
            print()
            resultats = rechercher_par_candidat(candidatures, 300)   # On récupère dans une liste tous les vœux correspondant au candidat portant le numéro 300
            for i in resultats:   # On parcourt un par un chaque vœu trouvé pour ce candidat 
                afficher_candidature(i)   # On déclenche l'affichage pour chaque dossier appartenant au candidat recherché
 
    if not os.path.exists(FICHIER_FORMATIONS):   # On vérifie si le fichier contenant la liste des formations est absent du dossier spécifié
        print(f"ERREUR : '{FICHIER_FORMATIONS}' introuvable")
    else:
        formations = extraire_formations(FICHIER_FORMATIONS)   # On appelle la fonction extraire_formations pour transformer le contenu du fichier CSV en un dictionnaire 
        print(f"\n{len(formations)} formations enregistrées")   # On affiche le nombre total de formations enregistrées 
        print("Exemples (10 premières) :")
        compteur = 0
        for id_formation, capacite in formations.items():   # On parcourt chaque formation du dictionnaire pour récupérer son identifiant et sa capacité d'accueil
            if compteur < 10:
                print(f"  Formation {id_formation} : {capacite} places")
                compteur += 1
            else:
                break
    print()
