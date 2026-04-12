from tri import tri_fusion

def policy_1(i):   # On définit une fonction pour une première policy qui reçoit un candidat i (sous forme de dictionnaire) pour faire un classement par ordre de priorité
    return (-i["score"], i["timestamp"], i["candidate_id"])   # On renvoie trois critères pour classer les candidats par score décroissant, par ancienneté et par identifiant croissant

def policy_2(i):   # On définit une fonction pour une deuxième policy qui reçoit un candidat i pour calculer sa priorité boursière
    score_arrondi = round(i["score"], -1)   # On arrondit le score à la dizaine la plus proche pour créer des égalités entre les scores très proches
    if i["is_scholarship"] == 1:   # On vérifie si le candidat est boursier
        rang_boursier = 0   # On donne le rang 0 (très prioritaire) au candidat
    else:
        rang_boursier = 1   # On donne le rang 1 (moins prioritaire) au candidat

    temps = i["timestamp"]   # On récupère l'heure précise de validation du vœu
    identifiant = i["candidate_id"]   # On récupère l'identifiant du candidat pour servir de critère de classement final en cas d'égalité 
    
    return (-score_arrondi, rang_boursier, temps, identifiant)   # On renvoie les quatre critères dans l'ordre d'importance pour classer les candidats par meilleur score par ,priorité boursière et par ancienneté

def tri(candidatures, policy):   # On définit une fonction qui choisit comment classer les candidats selon la policy choisie
    if policy == 1:
        return tri_fusion(candidatures, policy_1)   # On lance le tri fusion en utilisant les critères de la policy 1 
    else:
        return tri_fusion(candidatures, policy_2)   # On lance le tri fusion en utilisant les critères de la policy 2

def classer_candidats(groupes, formations, policy = 1):   # On définit une fonction qui gère le classement pour toutes les formations en utilisant la règle 1
    resultats = {}   # On crée un dictionnaire vide pour stocker les listes finales de chaque formation
    for program_id, candidatures in groupes.items():   # On parcourt chaque formation une par une avec son identifiant et sa liste de candidats
        capacite = formations.get(program_id, 0)   # On récupère le nombre de places disponibles pour une formation précise
        ordre = tri(candidatures, policy)   # On appelle la fonction de tri pour classer les candidats de la formation

        resultats[program_id] = {   # On ouvre un dictionnaire pour stocker quatre informations pour la formation actuelle
            "ordre_appel"   : ordre,
            "admis"         : ordre[:capacite],
            "liste_attente" : ordre[capacite:],
            "capacite"      : capacite
        }

    return resultats

def afficher_formation(program_id, resultats, nombre_candidats = 5):   # On définit une fonction d'affichage qui reçoit l'identifiant de la formation, ses résultats et le nombre de candidats 
    print()
    print(f"  FORMATION : {program_id}  |  {len(resultats["ordre_appel"])} candidats  |  {resultats["capacite"]} places")   # On affiche le nom de la formation, le total de candidats et le nombre de places disponibles 
    print(f"  Admis : {len(resultats["admis"])}   En attente : {len(resultats["liste_attente"])}")   # On affiche le bilan fina avec le nombre de candidats acceptés et le nombre de candidats en attente

    print(f"\n  ADMIS :")
    for rang, candidat in enumerate(resultats["admis"][:nombre_candidats], 1):   # On parcourt la liste des candidats admis jusqu'à la limite choisie en créant un rang qui démarre à 1 pour numéroter chaque ligne du classement
        if candidat["is_scholarship"]:   # Si le candidat est boursier
            statut = "boursier"
        else:
            statut = "non boursier"
        print(f"    {rang}. Identifiant = {candidat["candidate_id"]}   Score = {candidat["score"]}   Statut = {statut}")   # On affiche le rang du candidat, son identifiant, sa note et son statut de boursier ou non

        if resultats["liste_attente"]:   # On vérifie si la liste d'attente n'est pas vide 
            print(f"\n  LISTE D'ATTENTE :")

            for rang, candidat in enumerate(resultats["liste_attente"][:nombre_candidats], 1):   # On parcourt la liste des candidats en attente jusqu'à la limite choisie en créant un rang qui démarre à 1 pour numéroter chaque ligne du classement
                if candidat["is_scholarship"]:
                    statut = "boursier"
                else:
                    statut = "non boursier"
                print(f"    {rang}. Identifiant = {candidat["candidate_id"]}   Score = {candidat["score"]}   Statut = {statut}")

def afficher_resume(resultats):   # On définit une fonction qui va calculer et afficher le bilan global de toutes les formations

    total_admis = 0   # On initialise trois compteurs à zéro pour additionner les statistiques de chaque formation au fur et à mesure
    total_places = 0
    boursiers = 0

    for formation in resultats.values():   # On parcourt l'ensemble des dossiers de chaque foramtion stockés dans les résultats pour pouvoir traiter leurs données une par une
        total_admis += len(formation["admis"])   # On ajoute le nombre de candidats acceptés dans la formation actuelle au compteur total
        total_places += formation["capacite"]   # On ajoute le nombre de places disponibles dans la formation au total 

        for candidat in formation["admis"]:   # On parcourt la liste de toutes les personnes acceptées dans la formation actuelle pour examiner le profil de chaque candidat admis
            if candidat["is_scholarship"]:   # Si le candidat est boursier
                boursiers += 1

    print(f"  Formations : {len(resultats)}")
    print(f"  Places     : {total_places}")
    print(f"  Admis      : {total_admis}")
    print(f"  Boursiers  : {boursiers} ({100 * boursiers / max(total_admis, 1):.1f} %)")

if __name__ == "__main__":   # On vérifie que le fichier est exécuté directement et non importé

    candidats = [   # On crée une liste qui contient trois dictionnaires représentant chacun un candidat avec ses données 
        {"candidate_id": 1, "score": 15, "timestamp": 100, "is_scholarship": 0},
        {"candidate_id": 2, "score": 18, "timestamp": 105, "is_scholarship": 1},
        {"candidate_id": 3, "score": 14, "timestamp": 110, "is_scholarship": 0}
    ]
    
    groupes = {"Licence informatique": candidats}   # On crée un dictionnaire où la clé est le nom de la formation et la valeur est la liste des candidats 
    places = {"Licence informatique": 2}   # On crée un dictionnaire pour dire que la "Licence informatique" n'offre que 2 places 

    bilan = classer_candidats(groupes, places, policy = 1)   # On appelle la fonction classer_candidats qui va trier les candidats et décider qui est admis ou en attente et stocker tout dans le dictionnaire bilan

    for id_formation, resultats in bilan.items():   # On parcourt le dictionnaire bilan des résultats pour récupérer le nom de la formation et son dossier de classement complet à chaque tour
        afficher_formation(id_formation, resultats)   # On appelle la fonction afficher_formation pour afficher le tableau détaillé de la formation
    
    print("\n=== RÉSUMÉ ===")
    print()
    afficher_resume(bilan)   # On appelle la fonction afficher_resume qui calcule et affiche le bilan global de toutes les formations
    print()
