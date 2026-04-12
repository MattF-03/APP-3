import time
import random
from tri import tri_insertion, tri_fusion

def policy_1(i):   # On définit une fonction pour une première policy qui reçoit un candidat i (sous forme de dictionnaire) pour faire un classement par ordre de priorité
        return (-i["score"], i["timestamp"], i["candidate_id"])   # On renvoie trois critères pour classer les candidats par score décroissant, par ancienneté et par identifiant croissant

def policy_2(i):   # On définit une fonction pour une deuxième policy qui reçoit un candidat i pour calculer sa priorité boursière
        score_arrondi = round(i["score"], -1)   # On arrondit le score à la dizaine la plus proche pour créer des égalités entre les scores très proches
        if i["is_scholarship"] == 1:   # On vérifie si le candidat est boursier
            rang_boursier = 0   # On donne le rang 0 (très prioritaire) au candidat
        else:
            rang_boursier = 1   # On donne le rang 1 (moins prioritaire) au candidat
    
        return (-score_arrondi, rang_boursier, i["timestamp"], i["candidate_id"])   # On renvoie les quatre critères dans l'ordre d'importance pour classer les candidats par meilleur score, par priorité boursière et par ancienneté

def calculer_ordre_appel(candidatures, numero_policy = 1):   # On définit les policies de tri pour qu'elles soient accessibles
    ordre = candidatures[:]   # On crée une copie intégrale de la liste candidatures pour pouvoir la trier sans modifier les données de départ
    if numero_policy == 1:   # Si la policy choisie est la policy 1
        ordre.sort(key = policy_1)   # On trie la liste ordre en utilisant les critères de la policy 1
    else:
        ordre.sort(key = policy_2)   # On trie la liste ordre en utilisant les critères de la policy 2
    return ordre

def audit_egalite(candidatures, capacite, program_id = None):   # On définit une fonction pour auditer les scores identiques en précisant les candidats, les places et le nom de la formation
    print(f"=== AUDIT CANDIDATS A EGALITE : {program_id} ===")
    print()

    compteur = {}   # On crée un dictionnaire vide qui servira à compter combien de fois chaque score apparaît
    for i in candidatures:   # On parcourt la liste de tous les candidats un par un pour examiner leur score
        score = i["score"]   # On récupère la note du candidat et on la stocke dans la variable score
        if score in compteur:   # Si le score existe déjà dans le dictionnaire compteur
            compteur[score] += 1
        else:
            compteur[score] = 1   

    nombre_egalite = 0   # On initialise à zéro le compteur qui servira à compter le nombre total d'élèves ayant une note en double
    nombre_groupes = 0   # On initialise à zéro le compteur qui servira à identifier le nombre de groupes de notes identiques

    for n in compteur.values():   # On parcourt uniquement le nombre d'élèves pour chaque score stockées dans le dictionnaire compteur
        if n > 1:   # Si le score a été obtenu par plus d'une personne (égalité)
            nombre_egalite += n   # On ajoute le nombre de personnes concernées au total des candidats à égalité
            nombre_groupes += 1   # On compte un nouveau groupe d'égalité pour les statistiques

    print(f"  Candidats à égalité             : {nombre_egalite} ({100 * nombre_egalite / len(candidatures):.1f} %)")
    print(f"  Groupes de candidats à égalité  : {nombre_groupes}")

    classement_officiel = calculer_ordre_appel(candidatures, 1)   # On génère le classement officiel en appliquant les règles de départage de la policy 1
    admis_officiels = classement_officiel[:capacite]   # On sélectionne les meilleurs candidats du classement dans la limite des places disponibles
    identifiants_officiels = []   # On crée une liste vide qui servira à stocker les numéros d'identifiant des candidats admis officiels
    for i in admis_officiels:
        identifiants_officiels.append(i["candidate_id"])   # On ajoute le numéro d'identifiant du candidat à la liste de suivi des admis officiels

    ordre_aleatoire = random.sample(candidatures, len(candidatures))   # On crée une liste contenant tous les candidats mais mélangés dans un ordre totalement aléatoire
    ordre_aleatoire.sort(key = policy_1)   # On trie la liste ordre_alea en utilisant les critères de la policy 1

    admis_aleatoires = ordre_aleatoire[:capacite]   # On extrait les premiers candidats du classement pour ne garder que ceux qui auraient été acceptés selon la capacité de la formation
    identifiants_aleatoires = []   # On crée une liste vide qui servira à stocker les numéros d'identifiant des candidats admis aléatoirement par la simulation 
    for i in admis_aleatoires:
        identifiants_aleatoires.append(i["candidate_id"])   # On ajoute le numéro d'identifiant du candidat à la liste de suivi des admis aléatoires

    nombre_instables = 0   # On initialise à zéro le compteur qui servira à compter le nombre de candidats dont l'admission change selon la policy utilisée
    for identifiant_candidat in identifiants_officiels:   # On examine un par un chaque identifiant de candidat ayant été admis par la policy officielle
        if identifiant_candidat not in identifiants_aleatoires:   # On vérifie si le candidat admis officiellement aurait perdu sa place si on avait utilisé un tirage au sort 
            nombre_instables += 1
    
    print(f"  Admissions instables            : {nombre_instables}")

def audit_microecarts(candidatures, capacite, seuil = 0.5, program_id = None):   # On définit une fonction pour auditer les micro-écarts en prenant en compte les candidats, les places et le seuil
    print(f"\n=== AUDIT MICRO-ECARTS : {program_id} ===")
    print()

    identifiants_officiels = []   # On crée une liste vide destinée à stocker uniquement les numéros d'identifiant des admis officiels
    for i in calculer_ordre_appel(candidatures, 1)[:capacite]:   # On parcourt les candidatures dont le rang est inférieur ou égal à la capacité d'accueil de la formation selon la policy 1
        identifiants_officiels.append(i["candidate_id"])   # On ajoute le numéro d'identifiant du candidat à la liste de suivi des admis officiels

    identifiants_aleatoires = []   # On crée une liste vide qui servira à stocker les numéros d'identifiant des candidats admis aléatoirement par la simulation 
    for i in calculer_ordre_appel(candidatures, 2)[:capacite]:   # On parcourt les candidatures dont le rang est inférieur ou égal à la capacité d'accueil de la formation selon la policy 2
        identifiants_aleatoires.append(i["candidate_id"])   # On ajoute le numéro d'identifiant du candidat à la liste de suivi des admis aléatoires

    gagnants = 0   # On initialise à zéro le compteur qui servira à compter les élèves qui n'étaient pas admis officiellement mais qui le deviennent avec la policy 2
    perdants = 0   # On initialise à zéro le compteur qui servira à compter les élèves admis officiellement qui perdent leur place à cause de la policy 2

    for i in identifiants_aleatoires:   # On examine chaque candidat présent dans la liste des admis par la méthode aléatoire
        if i not in identifiants_officiels:   # On vérifie si le candidat est un nouveau qui profite de la modification de la policy
            gagnants += 1

    for i in identifiants_officiels:   # On examine chaque candidat présent dans la liste des admis officiels
        if i not in identifiants_aleatoires:   # On vérifie si un candidat admis normalement se retrouve exclu à cause de la policy 2
            perdants += 1

    print(f"  Candidats qui gangnent une place  : {gagnants}")
    print(f"  Candidats qui perdent une place   : {perdants}")

    classement_actuel = calculer_ordre_appel(candidatures, 1)   # On génère la liste de tous les candidats en appliquant les critères de la policy 1
    
    if len(classement_actuel) > capacite:   # On vérifie qu'il y a plus de candidats que de places 
        dernier_admis = classement_actuel[capacite - 1]   # On récupère les données du dernier candidat qui a obtenu la dernière place disponible
        premier_attente = classement_actuel[capacite]   # On récupère les données du premier candidat qui se retrouve en liste d'attente
        ecart = abs(dernier_admis["score"] - premier_attente["score"])   # On calcule la différence entre la note du dernier reçu et celle du premier refusé

        if ecart < seuil:   # Si la différence est trop faible pour être significative
            attention = " = micro-écart détecté "  
        else :
            attention = " = aucun micro-écart détecté "
        print(f"  Distance entre admis et refusé    : {ecart:.2f} points" + attention)

def audit_performance(candidatures, tailles = [500, 1000, 2000]):   # On définit une fonction qui va auditer la performance du système parcoursup sur des échantillons
    print(f"\n=== AUDIT PERFORMANCE ===")
    print()
    print(f"   {"Taille":>6}  | {"Insertion":>12} {"Fusion":>12}")
    print("-" * 41)

    def cle_score(i):   # On crée une fonction interne qui indique à l'algorithme de trier en se basant sur le score du candidat
        return -i["score"]   # On renvoie un classement des scores par ordre décroissant du plus grand au plus petit

    for taille in tailles:   # On lance une boucle pour tester chaque volume de candidats
        echantillon = random.sample(candidatures, min(taille, len(candidatures)))   # On prend au hasard un nombre de candidats pour simuler une charge de travail réelle

        copie_insertion = echantillon[:]   # On crée une copie indépendante des données pour tester l'algorithme lent sans modifier l'original
        debut = time.perf_counter()   # On enregistre l'heure précise du système parcoursup avant l'exécution de l'audit
        tri_insertion(copie_insertion, cle_score)   # On exécute le tri par insertion 
        temps_insertion = time.perf_counter() - debut   # On calcule le temps total écoulé pour le tri par insertion

        copie_fusion = echantillon[:]   # On crée une copie indépendante des données pour tester l'algorithme lent sans modifier l'original
        debut = time.perf_counter()   # On enregistre l'heure précise du système parcoursup avant l'exécution de l'audit
        tri_fusion(copie_fusion, cle_score)    # On exécute le tri par fusion 
        temps_fusion = time.perf_counter() - debut   # On calcule le temps total écoulé pour le tri par fusion

        print(f"   {taille:>6}  | {temps_insertion:>11.4f}s {temps_fusion:>11.4f}s")

def comparer_taux_boursiers(resultats_p1, resultats_p2):   # On définit une fonction de comparaison prenant en entrée les bilans d'admission des deux policies 
    print(f"\n=== COMPARAISON DES TAUX D'ADMISSION BOURSIERS ===")
    print()

    def calcul_stats(bilan):   # On définit une fonction interne pour automatiser le comptage des boursiers sur l'ensemble des formations d'un bilan 

        total_admis = 0   # On initialise à zéro le compteur qui servira à compter tous les candidats ayant reçu une proposition d'admission
        total_boursiers = 0   # On initialise à zéro le compteur qui vervira à compter les candidats admis boursiers

        for formation in bilan.values():   # On parcourt les données de chaque formation contenues dans le dictionnaire de résultats bilan
            admis = formation["admis"]   # On récupère la liste des candidats acceptés pour la formation en cours de traitement
            total_admis += len(admis)   # On ajoute le nombre d'admis de la formation actuelle au total d'admis

            for i in admis:   # On examine chaque candidat présent dans la liste des admis de la formation
                if i["is_scholarship"]:   # Si le candidat est boursier
                    total_boursiers += 1

        return total_boursiers, total_admis

    boursiers_p1, total_p1 = calcul_stats(resultats_p1)   # On extrait le nombre de boursiers et le volume global d'admis pour la policy 1
    boursiers_p2, total_p2 = calcul_stats(resultats_p2)   # On extrait le nombre de boursiers et le volume global d'admis pour la policy 2

    print(f"  Policy 1   : {boursiers_p1}/{total_p1} boursiers ({100 * boursiers_p1/max(total_p1, 1):.1f}%)")
    print(f"  Policy 2   : {boursiers_p2}/{total_p2} boursiers ({100 * boursiers_p2/max(total_p2, 1):.1f}%)")
    print(f"  Évolution  : {boursiers_p2 - boursiers_p1} boursiers supplémentaires avec la policy 2")
    print()

if __name__ == "__main__":   # On vérifie que le fichier est exécuté directement et non importé

    test_candidatures = [   # On crée une liste qui contient des dictionnaires pour représenter des candidats tests
        {"candidate_id": 1, "score": 15.5, "timestamp": 100, "is_scholarship": 0},
        {"candidate_id": 2, "score": 15.48, "timestamp": 101, "is_scholarship": 1},
        {"candidate_id": 3, "score": 12.0, "timestamp": 102, "is_scholarship": 0}
    ]

    audit_egalite(test_candidatures, capacite = 2, program_id = "Licence informatique")   # On appelle la fonction pour auditer si des candidats ont des scores identiques dans la formation "L1 Informatique"
    audit_microecarts(test_candidatures, capacite = 2, seuil = 0.5, program_id = "Licence informatique")   # On lance l'audit des écarts de points entre les derniers admis et les premiers refusés
    audit_performance(test_candidatures, tailles = [2, 4])   # On audite et compare la vitesse d'exécution des algorithmes de tri sur des échantillons de 2 et 4 candidats

    resultats_policy1 = {"Formation_A": {"admis": test_candidatures[:2]}}   # On simule un bilan d'admission pour la policy 1 en prenant les deux premiers candidats de la liste
    resultats_policy2 = {"Formation_A": {"admis": test_candidatures[1:3]}}   # On simule un bilan d'admission pour la policy 2 en prenant les deux premiers candidats de la liste
    comparer_taux_boursiers(resultats_policy1, resultats_policy2)   # On compare l'impact des deux méthodes de tri sur l'admission des candidats boursiers
