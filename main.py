import os   # On importe le module os qui permet d'interagir avec le système d'exploitation
from read import extraire_candidatures, extraire_formations, grouper_par_formation, statistiques, afficher_candidature, rechercher_par_candidat
from parcoursup import classer_candidats, afficher_formation, afficher_resume
from audit import audit_egalite, audit_microecarts, audit_performance, comparer_taux_boursiers
from tri import comparer_algorithmes

DOSSIER = "APP3_Fichiers"   # On crée une variable pour stocker le nom du dossier qui contient toutes les données
 
FICHIER_CANDIDATURES = os.path.join(DOSSIER, "parcoursup_small_10000.csv")   # On crée le chemin complet vers le fichier des vœux en assemblant le nom du dossier et le nom du fichier CSV
FICHIER_FORMATIONS = os.path.join(DOSSIER, "parcoursup_programs_small_800.csv")   # On paramètre le lien vers le fichier des formations pour faciliter la lecture par le programme

AFFICHAGE_FORMATIONS = [1]   # On définit une liste contenant l'identifiant de la formation 1 par défaut dont on souhaite afficher les détails

def etape_chargement():   # On définit une fonction qui initialise le processus d'importation et de structuration des données CSV
    print("\n" + "=" * 34)
    print(" ÉTAPE 1 — CHARGEMENT DES DONNÉES")
    print("=" * 34)
    print()

    for i in [FICHIER_CANDIDATURES, FICHIER_FORMATIONS]:   # On lance une boucle pour vérifier la présence du fichier des vœux et du fichier des formations
        if not os.path.exists(i):   # Si le fichier testé est absent du dossier spécifié 
            print(f"ERREUR : Fichiers CSV introuvables dans {DOSSIER}")
            return [], {}   # On renvoie une liste vide et un dictionnaire vide pour signaler l'échec du chargement sans arrêter le programme

    candidatures = extraire_candidatures(FICHIER_CANDIDATURES)   # On enregistre les vœux des étudiants dans une liste de dictionnaires en utilisant la fonction extraire_candidatures
    formations = extraire_formations(FICHIER_FORMATIONS)   # On récupère les caractéristiques et capacités d'accueil de chaque formation en utilisant la fonction extraire_formations
    
    print(f"✓ {len(candidatures)} candidatures et {len(formations)} formations importées")
    statistiques(candidatures)   # On déclenche l'affichage d'un premier bilan sur le profil des candidats 
    return candidatures, formations

def etape_affichage_candidat(candidatures):   # On définit une fonction qui sert à afficher le dossier d'un candidat spécifique
    print("\n" + "=" * 34)
    print(" ÉTAPE 2 — EXEMPLE DE CANDIDATURE")
    print("=" * 34)
    print()

    id_candidature = candidatures[0]["candidate_id"]   # On extrait l'identifiant du premier candidat de la liste pour servir d'exemple automatique
    voeux = rechercher_par_candidat(candidatures, id_candidature)   # On récupère les vœux associés à l'identifiant en filtrant la base de données

    if voeux:   # On vérifie la présence de données avant de lancer l'affichage détaillé
        print(f"  Candidat ID = {id_candidature} | {len(voeux)} vœu(x) :")
        print()
        for i in voeux[:3]:   # On parcourt les trois premiers vœux de la liste afin de ne pas encombrer l'affichage 
            afficher_candidature(i)   # On appelle la fonction afficher_candidature pour présenter les détails de chaque vœu de manière lisible
            print() 
    else:
        print(f"  Candidat {id_candidature} introuvable")

def etape_ordres_appel(candidatures, formations):   # On définit une fonction qui sert à simuler les classements des candidats selon différentes policies
    print("=" * 37)
    print(" ÉTAPE 3 — CALCUL DES ORDRES D'APPEL")
    print("=" * 37)

    groupes = grouper_par_formation(candidatures)   # On regroupe l'ensemble des vœux par formation
    resultats_p1 = None   # On initialise à vide la variable qui servira à stocker les classements générés par la policy 1
    resultats_p2 = None   # On initialise à vide la variable qui servira à stocker les classements générés par la policy 2

    policies_a_tester = {   # On crée un dictionnaire pour associer chaque numéro d'algorithme à un nom pour l'affichage
        1: "Policy 1 (Standard)", 
        2: "Policy 2 (Priorité boursiers)"
    }

    for numero_policy, nom_policy in policies_a_tester.items():   # On parcourt chaque policy définie pour exécuter les deux simulations
        print(f"\n  === {nom_policy} ===")
        print()

        bilan = classer_candidats(groupes, formations, policy = numero_policy)   # On exécute l'algorithme de classement sur tous les groupes en appliquant la policy spécifique
        
        afficher_resume(bilan)   # On affiche un récapitulatif des données contenues dans le dictionnaire bilan pour valider le bon fonctionnement de la policy de classement

        for id_formation in AFFICHAGE_FORMATIONS:   # On parcourt la liste des identifiants sélectionnés pour cibler les formations dont on veut voir le détail du classement
            if id_formation in bilan:
                afficher_formation(id_formation, bilan[id_formation], nombre_candidats = 3)   # On affiche le détail du classement pour la formation limité aux trois premiers candidats

        if numero_policy == 1:   # Si la policy choisie est la policy 1
            resultats_p1 = bilan   # On enregistre les résultats de la simulation standard dans la variable resultats_p1
        else:
            resultats_p2 = bilan   # On enregistre les résultats de la simulation priorisant les boursiers dans la variable resultats_p2

    return groupes, resultats_p1, resultats_p2

def etape_audits(candidatures, formations, groupes, resultats_p1, resultats_p2):   # On définit une fonction qui regroupe les tests de contrôle et la détection d'anomalies sur les classements
    print("\n" + "=" * 31)
    print(" ÉTAPE 4 — AUDIT DES ANOMALIES")
    print("=" * 31)
    print()

    id_formation_audit = ""   # On initialise une variable vide pour stocker l'identifiant de la formation étudiée
    max_candidats = -1   # On initialise un compteur à -1 pour pouvoir trouver le nombre maximum de candidats par comparaison

    for id_formation, liste_candidats in groupes.items():   # On parcourt chaque groupe de formation pour examiner le volume de candidats postulant dans chacune des formation
        if len(liste_candidats) > max_candidats:   # On compare le nombre de candidats de la formation avec le maximum de candidats enregistré 
            max_candidats = len(liste_candidats)   # On met à jour la valeur maximale si la formation contient plus de candidats que la précédente
            id_formation_audit = id_formation   # On mémorise l'identifiant de la formation la plus demandée pour l'utiliser dans les tests suivants

    candidats_audit = groupes[id_formation_audit]   # On récupère la liste complète des candidats rattachés à la formation sélectionnée pour l'audit
    capacite_audit = formations.get(id_formation_audit, 50)   # On obtient le nombre de places disponibles pour la formation avec une valeur par défaut de 50

    print(f"Audit de la formation {id_formation_audit} : {len(candidats_audit)} candidats pour {capacite_audit} places")
    print()

    audit_egalite(candidats_audit, capacite_audit, program_id = id_formation_audit)   # On exécute un test pour vérifier si les candidats ayant des scores identiques sont traités de manière équitable
    audit_microecarts(candidats_audit, capacite_audit, seuil = 10, program_id = id_formation_audit)   # On analyse si de très faibles différences de notes provoquent des changements de classement 
    audit_performance(candidatures, tailles = [500, 1000])   # On mesure la vitesse d'exécution de l'algorithme sur des volumes de données croissants 
    comparer_taux_boursiers(resultats_p1, resultats_p2)   # On compare les résultats des deux policies pour mesurer l'impact réel de la priorité donnée aux boursiers

def etape_comparaison(candidatures):   # On définit une fonction qui va orchestrer la phase finale de test de rapidité des tris
    print("=" * 39)
    print(" ÉTAPE 5 — COMPARAISON DES ALGORITHMES")
    print("=" * 39)
    print()

    comparer_algorithmes(candidatures, tailles = [500, 1000])   # On lance les calculs de temps pour chaque algorithme de tri sur deux échantillons de données

def main():   # On définit une fonction principale qui orchestre le déroulement complet du programme
    print()
    print("-" * 46)
    print("      ANALYSE DES CLASSEMENTS PARCOURSUP")   # On affiche le nom du projet 
    print("         Équipe de contrôle technique")   # On affiche le nom de l'équipe responsable du développement du prototype
    print("-" * 46)

    candidatures, formations = etape_chargement()   # On récupère les informations des fichiers externes pour lancer le programme
    etape_affichage_candidat(candidatures)   # On présente les informations détaillées d'un candidat choisi pour illustrer le fonctionnement
    groupes, resultats_p1, resultats_p2 = etape_ordres_appel(candidatures, formations)   # On calcule les classements selon deux policies différentes et on les organise par formation
    etape_audits(candidatures, formations, groupes, resultats_p1, resultats_p2)   # On lance les tests de contrôle sur la formation la plus demandée
    etape_comparaison(candidatures)   # On analyse et affiche les différences de résultats entre les deux modes de classement

    print("\n  Démonstration terminée")
    print()

if __name__ == "__main__":   # On vérifie que le fichier est exécuté directement et non importé
    main()   # On appelle la fonction principale pour démarrer le programme
