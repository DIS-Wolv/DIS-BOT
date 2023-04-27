from bot import secrets
from bot.sources import *
from datetime import datetime

from bot.inscription.google import sh
from bot.inscription.utils import init, jourTransfo, UserToID, slice_in_matrix
from bot.inscription.constants import jourNom
from bot.inscription.builder import build_msg
from bot.utils import log


def stateDLC(user, dlc, state):
    """
    est appellé par le bot
      user = utilisateur souhaité
      dlc = n° du dlc (commence a 0)
      state = etat souhaité (1 = ajout, autre = suppression)
    """
    dico = init()
    user = str(user)

    wks = sh[10]  # ouvre la page Technique

    name = wks.get_values("D1", "D2")  # lit le titre
    # print(name)

    colone = ["D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]

    if name == [["Détails techniques (ne PAS toucher)"]]:

        if user in dico[1]:
            pos = dico[1].index(user) + 8

            if state == 1:
                DLC = [["V"]]
            else:
                DLC = [[""]]

            plage = colone[dlc] + str(pos)
            # print(plage)
            wks.update_values(plage, DLC)

            # date(user)

            return 1
        else:
            return 2
    else:
        return -1


def add(user: int, jour, rolevoulue=[""]):
    """
    est appellé par le bot
    incrit l'utilisateur avec le role souhaité au jour demandé

    retourne:
    - 0 si deja inscrit
    - 1 si succes
    - 2 si echec
    """
    dico = init()  # initialise dico
    user = str(user)  # récupère l'id de l'utilisateur

    if (user in dico[1]) and jour != 0:
        # si l'id de l'utilisateur est dans la 2e colonne du dico et que le jour est valide
        pos = dico[1].index(user)  # recupère la position de l'id de l'utilisateur
        usern = dico[0][pos]  # récupère le nom de l'utilisateur
        # print(user, "est a la position", pos, "et correspond a", usern)
        # print(usern, jour, rolevoulue)
        page = 0
        page = jourTransfo(jour)  # transforme le jour en numéro de page

        wks = sh[page]  # lecture du document du jour

        nom = wks.get_values("D1", "D2")  # lit le titre

        if nom != [["Entraînement"]]:
            inscrit = wks.get_values("B17", "B56")  # récupère les inscrits
            role = wks.get_values("C17", "C56")  # recupère les roles
        else:
            inscrit = wks.get_values("B8", "B31")  # récupère les inscrits
            role = wks.get_values("C8", "C31")  # recupère les roles
        # print(inscrit, role)

        while len(inscrit) > len(role):
            role.append(["GV"])

        # test si l'utilisateur est deja inscrit
        if usern in inscrit:  # si l'utilisateur est inscrit
            return 0  # sort de la fonction
        else:  # sinon

            ins = True  # défini l'utilisateur comme à inscrire
            # cherche une place dans la liste des inscrits
            for i in range(len(inscrit)):  # pour chaque élément des inscrits
                if inscrit[i] == [""]:  # si il y a une place
                    if ins:  # si l'utilisateur est a inscrire
                        inscrit[i] = usern  # inscrit l'utilisateur
                        role[i] = rolevoulue  # defini son role
                        ins = False  # défini l'utilisateur comme inscrit

            # si pas de place, se rajoute a la fin
            if ins:  # si utilisateur toujours a inscrire
                inscrit.append(usern)  # ajoute l'utilisateur a la fin
                role.append(rolevoulue)  # defini son role

            # print(inscrit, role)
            if nom != [["Entraînement"]]:
                wks.update_values("B17:B56", inscrit)  # met à jour le google sheet
                wks.update_values("C17:C56", role)  # met à jour la liste des roles
            else:
                wks.update_values("B8:B31", inscrit)  # met à jour le google sheet
                wks.update_values("C8:C31", role)  # met à jour la liste des roles

            # print("utilisateur inscrit")
            date(user)

            return 1  # sort de la fonction
    else:
        # print("Erreur : user n'est pas dans le dico")
        return 2  # sort de la fonction


def date(user):
    """
    mise a jour de la date sur la fiche technique
    """
    dico = init()  # initialise dico
    user = str(user)  # récupère l'id de l'utilisateur

    pos = dico[1].index(user)
    tech = sh[10]
    Date = tech.get_values("O8", "O200")
    Date[pos] = [
        str(datetime.now().day)
        + "/"
        + str(datetime.now().month)
        + "/"
        + str(datetime.now().year)
    ]
    tech.update_values("O8:O200", Date)


def remove(user, jour):
    """
    est appellé par le bot
    deincrit utilisateur au jour demandé

    retourne
     0 si deja désincrit
     1 si succès
     2 si échec
    """
    dico = init()  # initialise dico
    user = str(user)  # récupère l'id de l'utilisateur

    if (
        user in dico[1]
    ) and jour != 0:  # si l'id de l'utilisateur est dans la 2e colonne du dico et que le jour est valide
        pos = dico[1].index(user)  # recupère la position de l'id de l'utilisateur
        usern = dico[0][pos]  # récupère le nom de l'utilisateur
        # print(user, "est à la position", pos, "et correspond à", usern)

        page = 0
        page = jourTransfo(jour)  # transforme le jour en numéro de page

        wks = sh[page]  # lecture du document du jour

        nom = wks.get_values("D1", "D2")  # lit le titre

        if nom != [["Entraînement"]]:
            inscrit = wks.get_values("B17", "B56")  # récupère les inscrits
            role = wks.get_values("C17", "C56")  # recupère les roles
            commentaire = wks.get_values("D17", "D56")  # recupère les commentaires
        else:
            inscrit = wks.get_values("B8", "B31")  # récupère les inscrits
            role = wks.get_values("C8", "C31")  # recupère les roles
            commentaire = wks.get_values("D8", "D31")  # recupère les commentaires

        # print(inscrit)

        if usern in inscrit:  # si l'utilisateur est inscrit

            # cherche dans la liste des inscrits
            for i in range(0, len(inscrit)):  # parcours la liste des inscrits
                if inscrit[i] == usern:  # si on est a la position de l'utilisateur
                    inscrit[i] = [""]  # suprime l'utilisateur
                    if len(role) > i:
                        role[i] = [""]  # supprime son role souhaité
                    if len(commentaire) > i:
                        commentaire[i] = [""]  # supprime son commentaire

            if nom != [["Entraînement"]]:
                wks.update_values("B17:B56", inscrit)  # met à jour la liste des inscrits
                wks.update_values("C17:C56", role)  # met à jour la liste des roles
                wks.update_values("D17:D56", commentaire)  # met à jour la liste des commentaires
            else:
                wks.update_values("B8:B31", inscrit)  # met à jour la liste des inscrits
                wks.update_values("C8:C31", role)  # met à jour la liste des roles

            # print("utilisateur désinscrit")
            date(user)
            return 1  # sort de la fonction

        else:  # si l'utilisateur n'est pas dans la liste des inscrits
            # print("utilistateur", usern, "est déjà désinscrit")
            return 0  # sort de la fonction

    else:  # si l'utilisateur n'est pas dans dico ou le jour est incorrect
        # print("Erreur : user n'est pas dans le dico")
        return 2  # sort de la fonction


def clear(jour):
    """
    est appellé par le bot
    désincrit tous les utilisateurs au jour demandé
    supprime aussi le nom de la mission, du Zeus, et le brief
    """
    page = 0
    page = jourTransfo(jour)  # transforme le jour en page
    print("Nettoyage de la page", page, "correspondant à", jourNom[jour])
    wks = sh[page]  # ouvre la page correspondante

    liste15 = [
        [""],
        [""],
        [""],
        [""],
        [""],
        [""],
        [""],
        [""],
        [""],
        [""],
        [""],
        [""],
        [""],
        [""],
        [""],
    ]  # crée une liste vide
    liste10 = [[""], [""], [""], [""], [""], [""], [""], [""], [""], [""]]

    nom = wks.get_values("D1", "D2")  # lit le titre
    # print(nom)
    if nom != [["Entraînement"]]:
        # Titre
        wks.update_values("D1", [[""]])
        # Zeus
        wks.update_values("E3", [[""]])
        # Brief
        wks.update_values("B7", [[""]])

    clearJoueur(jour)

    print(
        "Nettoyage done"
    )  # met un message dans la console indiquant la page et le jour nettoyé


def clearJoueur(jour):
    """
    est appellé par le bot et la fonction clear
    deincrit tous les utilisateurs au jour demandé
    """
    page = 0
    page = jourTransfo(jour)  # transforme le jour en page
    print("Nettoyage des inscrit de la page", page, "correspondant à", jourNom[jour])
    wks = sh[page]  # ouvre la page correspondante

    liste15 = [[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""]]  # crée une liste vide
    liste10 = [[""], [""], [""], [""], [""], [""], [""], [""], [""], [""]]

    nom = wks.get_values("D1", "D2")  # lit le titre
    if nom != [["Entraînement"]]:
        # liste des joueurs
        wks.update_values("B17:B27", liste10)
        wks.update_values("B27:B37", liste10)
        wks.update_values("B37:B47", liste10)
        wks.update_values("B47:B57", liste10)
        wks.update_values("B57:B67", liste10)

        # liste des roles
        wks.update_values("C17:C27", liste10)
        wks.update_values("C27:C37", liste10)
        wks.update_values("C37:C47", liste10)
        wks.update_values("C47:C57", liste10)
        wks.update_values("C57:C67", liste10)

        # liste des comantaires
        wks.update_values("D17:D27", liste10)
        wks.update_values("D27:D37", liste10)
        wks.update_values("D37:D47", liste10)
        wks.update_values("D47:D57", liste10)
        wks.update_values("D57:D67", liste10)


        # sanglier
        wks.update_values("G19:G33", liste15)
        # grizzli
        wks.update_values("J19:J33", liste15)
        # Taureau
        wks.update_values("M19:M33", liste15)

        # Albatros
        wks.update_values("J44:J47", [[""], [""], [""], [""]])
        # Harfang
        wks.update_values("G44:G47", [[""], [""], [""], [""]])

        # Coyote
        wks.update_values("M8:M14", [[""], [""], [""], [""], [""], [""], [""]])


        # CROCODILE
        wks.update_values("G37:G39", [[""], [""], [""]])
        # ALIGATOR
        wks.update_values("J37:J39", [[""], [""], [""]])
    else:
        # liste des joueurs
        wks.update_values("B8:B22", liste15)
        wks.update_values("B23:B38", liste15)
        # liste des commentaires
        wks.update_values("C8:C22", liste15)
        wks.update_values("C23:C38", liste15)

        # gerant module 1
        wks.update_values("G13", [[""]])
        # liste des incrits Module 1
        wks.update_values("F16:F25", liste10)
        # liste des affectation Module 1
        wks.update_values("G16:G25", liste10)

        # gerant module 2
        wks.update_values("J13", [[""]])
        # liste des incrits Module 2
        wks.update_values("I16:I25", liste10)
        # liste des affectation Module 2
        wks.update_values("J16:J25", liste10)

        # gerant module 3
        wks.update_values("M13", [[""]])
        # liste des incrits Module 3
        wks.update_values("L16:L25", liste10)
        # liste des affectation Module 3
        wks.update_values("M16:M25", liste10)


def message(jour):
    """
    est appellé par le bot
    retourne
     0 si pas de missions
     <str> msg si il y a une mission
    """
    dico = init()  # initialise dico
    log("message")
    log(f"message -- {jour=}")

    log("message -- fetch base")
    page = jourTransfo(jour)  # transforme le jour en page
    wks = sh[page]  # ouvre la page
    name = wks.get_values("D1", "D2")  # lit le titre
    zeus = wks.get_values("E3", "E3")  # lit le zeus
    brief = wks.get_values("B7", "B7")  # lit le brief
    log("message -- fetch base [done]")

    log(f"message -- Test '{name[0][0]}'")
    if name == [["Entraînement"]]:
        log("message -- orga")
        orga(jour)
        log("message -- orga [done]")
        log("message -- fetch Entraînement")
        inscrit = wks.get_values("B8", "B31")  # récupère les inscrits
        role = wks.get_values("C8", "C31")  # recupère les roles
        log("message -- fetch Entraînement [done]")

        log("message -- build_message")
        msg = (
            "<@&"
            + str(secrets.ROLE_ID)
            + "> **"
            + name[0][0]
            + "** "
            + jourNom[jour]
            + " soir : \nLe drill est la clef, venez vous entraîner ! \nInscrivez vous en réagissant ou directement "
            "sur le planning : " + secrets.LINKS[jour]
        )
        log("message -- build_message [done]")
    elif name[0][0] == "":
        log("message -- pas de mission")
        msg = 0
    else:
        log("message -- orga")
        orga(jour)
        log("message -- orga [done]")
        log("message -- fetch groups")
        data = wks.get_values("A1", "O68", include_tailing_empty_rows=True)

        inscrit = slice_in_matrix(data, 1, 2, 16, 67)  # B17 -> 67
        role = slice_in_matrix(data, 2, 3, 16, 67)  # C17 -> 67
        commentaire = slice_in_matrix(data, 3, 4, 16, 67)  # D17 -> 67

        Sanglier = slice_in_matrix(data, 6, 7, 18, 33)  # G19 -> 33
        Grizzli = slice_in_matrix(data, 9, 10, 18, 33)  # J19 -> 33
        Taureau = slice_in_matrix(data, 12, 13, 18, 33) # M19 -> 33

        Coyote = slice_in_matrix(data, 12, 13, 7, 14)   # M8 -> 14

        Crocodile = slice_in_matrix(data, 6, 7, 36, 39)  # G37 -> 39
        Aligator = slice_in_matrix(data, 9, 10, 36, 39)  # J37 -> 39
        
        Harfang = slice_in_matrix(data, 6, 7, 43, 47)    # G44 -> 47
        Albatros = slice_in_matrix(data, 9, 10, 43, 45)  # J44 -> 45
        log("message -- fetch groups [done]")

        log("message -- build_message")
        msg = build_msg(dico, jour, name, zeus, brief, inscrit, role, commentaire, Sanglier, Grizzli, Taureau, Coyote, Crocodile, Aligator, Albatros, Harfang)
        log("message -- build_message [done]")

    log("message [done]")
    return msg


def jourPage(page):
    """
    est appellé par le bot
    retourne le mots écrit en position A1 du tableau
    """
    wks = sh[page]  # ouvre la page correspondante
    nom = wks.get_values("A1", "A2")  # lit le titre
    return nom[0][0]


def addUser(user, id):
    """
    est appellé par le bot
    ajoute un utilisateur 'user' dans le dico avec l'id 'id'
    """
    wks = sh[10]  # ouvre la page Technique

    name = wks.get_values("D1", "D2")  # lit le titre
    # print(name)

    if name == [["Détails techniques (ne PAS toucher)"]]:
        cont = True
        i = 7
        while cont:
            i = i + 1
            case = "B" + str(i)
            contenue = wks.get_values(case, case)
            # print(case, ":", contenue)

            if contenue == [[""]]:
                cont = False
            elif case == "B200":
                return -1

        range = "B" + str(i)
        text = [[str(user)]]
        wks.update_values(range, text)

        range = "C" + str(i)
        text = [[str(id)]]
        wks.update_values(range, text)

        date(user)

    return 0


def remUser(id):
    """
    est appellé par le bot
    enlève un utilisateur dans le dico
    """
    dico = init()  # initialise dico
    user = str(id)  # récupère l'id de l'utilisateur

    LigneVide = [["", "", "", "", "", "", "", "", "", "", "", "", "", ""]]

    wks = sh[10]  # ouvre la page Technique

    name = wks.get_values("D1", "D2")  # lit le titre
    # print(name)

    if name == [["Détails techniques (ne PAS toucher)"]]:
        if user in dico[1]:
            pos = dico[1].index(user)  # recupère la position de l'id de l'utilisateur
            ln = pos + 8
            area = "B" + str(ln) + "O" + str(ln)
            # userLn = wks.get_values(rangeB, rangeO)
            wks.update_values(area, LigneVide)
    return 0


def missionName(jour):
    """
    est appellé par le bot
    renvoie le nom de la mission
    """
    page = jourTransfo(jour)  # transforme le jour en numéro de pag
    wks = sh[page]  # lecture du document du jour
    nom = wks.get_values("D1", "D2")  # lit le titre
    # print(nom)
    return nom[0][0]

def missionOrgaName(jour):
    """
    est appellé par le bot
    renvoie le nom de l'organisateur de la mission
    """
    page = jourTransfo(jour)  # transforme le jour en numéro de pag
    wks = sh[page]  # lecture du document du jour
    nom = wks.get_values("E3", "E3")  # lit le nom
    # print(nom)
    return nom[0][0]


def orga(jour):
    """
    Organise la page du jours dans l'ordre des roles
    """
    page = jourTransfo(jour)  # transforme le jour en numéro de pag
    wks = sh[page]  # lecture du document du jour
    nom = wks.get_values("D1", "D2")  # lit le titre

    if nom != [[""]] and nom != [["Entraînement"]]:
        log("orga -- fetch")
        data = wks.get_values("A1", "O44", include_tailing_empty_rows=True)
        inscrit = slice_in_matrix(data, 1, 2, 16, 40)  # B17 -> 40
        role = slice_in_matrix(data, 2, 3, 16, 40)  # C17 -> 40
        commentaire = slice_in_matrix(data, 3, 4, 16, 40)  # D17 -> 40
        for i in range(len(inscrit)):
            if inscrit[i][0] != "" and role[i][0] == "":
                role[i][0] = "GV"

        Tech = sh[10]  # ouvre la page Technique
        importance = Tech.get_values("Q8", "Q20") + [[""]]
        log("orga -- fetch [done]")

        log("orga -- organize")
        for i in range(len(role)):
            if role[i][0] == "":
                continue
            for j in range(0, i):
                if importance.index(role[j]) > importance.index(role[i]):
                    temp = role[i]
                    role[i] = role[j]
                    role[j] = temp

                    temp = inscrit[i]
                    inscrit[i] = inscrit[j]
                    inscrit[j] = temp

                    temp = commentaire[i]
                    commentaire[i] = commentaire[j]
                    commentaire[j] = temp
        log("orga -- organize [done]")

        log("orga -- update")
        # met à jour le google sheet
        result = []
        for i in range(len(inscrit)):
            result.append(inscrit[i] + role[i] + commentaire[i])
        wks.update_values("B17:D40", result)
        log("orga -- update [done]")

