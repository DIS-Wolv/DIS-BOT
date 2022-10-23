import pygsheets
import secrets
from sources import *
from datetime import datetime

# autorisation
gc = pygsheets.authorize(service_file='bot-dis-318119-b1d3fcbed6d4.json')
# gc = pygsheets.authorize(client_secret='bot-dis-318119-b1d3fcbed6d4.json')

# ouverture du google sheet
sh = gc.open('Planning')

# jourNom est un tableau contenant les jours
jourNom = ["", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# est appellé pour initialiser dico
# retourne dico
def init():
    # selection de la fiche technique
    wks = sh[10]
    # création et complétion du dico
    dico = ["nom", "ID"]

    read = wks.get_values('B8', 'B200')  # lit les pseudos
    dico[0] = read  # met les pseudos dans la première colonne de dico

    read = wks.get_values('C8', 'C200')  # lis les ID
    for i in range(0, len(read)):
        read[i] = read[i][0]
    dico[1] = read  # met les IDs dans la 2e colonne de dico
    # print("dico initialisé")
    # print(dico)
    return dico

# est appellé par les autres fonctions
# transforme le jour en numéro de page
# retourne le numéro de la page
def jourTransfo(jour):
    if jour <= 5:  # de lundi a Vendredi le numéro du jour = numéro de la page
        page = jour
    elif jour == 6:  # décalage du a la page samedi aprem
        page = 7
    elif jour == 7:  # décalage du a la page dimanche aprem
        page = 9
    else:
        page = 0

    return page

# est appellé par le bot
#   user = utilisateur souhaité
#   dlc = n° du dlc (commence a 0)
#   state = etat souhaité (1 = ajout, autre = suppression)
def stateDLC(user, dlc, state):
    dico = init()
    user = str(user)

    wks = sh[10]  # ouvre la page Technique

    name = wks.get_values('D1', 'D2')  # lit le titre
    # print(name)

    colone = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']

    if name == [['Détails techniques (ne PAS toucher)']]:

        if user in dico[1]:
            pos = dico[1].index(user) + 8

            if state == 1:
                DLC = [['V']]
            else:
                DLC = [['']]

            plage = colone[dlc] + str(pos)
            # print(plage)
            wks.update_values(plage, DLC)

            # date(user)

            return 1
        else:
            return 2
    else:
        return -1

def add(user: int, jour, rolevoulue=['']):
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

        nom = wks.get_values('D1', 'D2')  # lit le titre

        if nom != [['Entraînement']]:
            inscrit = wks.get_values('B17', 'B40')  # récupère les inscrits
            role = wks.get_values('C17', 'C40')  # recupère les roles
        else:
            inscrit = wks.get_values('B8', 'B31')  # récupère les inscrits
            role = wks.get_values('C8', 'C31')  # recupère les roles
        # print(inscrit, role)

        while len(inscrit) > len(role):
            role.append(['GV'])

        # test si l'utilisateur est deja inscrit
        if usern in inscrit:  # si l'utilisateur est inscrit
            return 0  # sort de la fonction
        else:  # sinon

            ins = True  # défini l'utilisateur comme à inscrire
            # cherche une place dans la liste des inscrits
            for i in range(len(inscrit)):  # pour chaque élément des inscrits
                if inscrit[i] == ['']:  # si il y a une place
                    if ins:  # si l'utilisateur est a inscrire
                        inscrit[i] = usern  # inscrit l'utilisateur
                        role[i] = rolevoulue  # defini son role
                        ins = False  # défini l'utilisateur comme inscrit

            # si pas de place, se rajoute a la fin
            if ins:  # si utilisateur toujours a inscrire
                inscrit.append(usern)  # ajoute l'utilisateur a la fin
                role.append(rolevoulue)  # defini son role

            # print(inscrit, role)
            if nom != [['Entraînement']]:
                wks.update_values('B17:B40', inscrit)  # met à jour le google sheet
                wks.update_values('C17:C40', role)  # met à jour la liste des roles
            else:
                wks.update_values('B8:B31', inscrit)  # met à jour le google sheet
                wks.update_values('C8:C31', role)  # met à jour la liste des roles

            # print("utilisateur inscrit")
            date(user)

            return 1  # sort de la fonction
    else:
        # print("Erreur : user n'est pas dans le dico")
        return 2  # sort de la fonction

# mise a jour de la date sur la fiche technique
def date(user):
    dico = init()  # initialise dico
    user = str(user)  # récupère l'id de l'utilisateur

    pos = dico[1].index(user)
    tech = sh[10]
    Date = tech.get_values('O8', 'O200')
    Date[pos] = [str(datetime.now().day) + "/" + str(datetime.now().month) + "/" + str(datetime.now().year)]
    tech.update_values('O8:O200', Date)

# est appellé par le bot
# deincrit utilisateur au jour demandé
# return 0 si deja désincrit
# return 1 si succès
# return 2 si échec
def remove(user, jour):
    dico = init()  # initialise dico
    user = str(user)  # récupère l'id de l'utilisateur

    if (user in dico[1]) and jour != 0:  # si l'id de l'utilisateur est dans la 2e colonne du dico et que le jour est valide
        pos = dico[1].index(user)  # recupère la position de l'id de l'utilisateur
        usern = dico[0][pos]  # récupère le nom de l'utilisateur
        # print(user, "est à la position", pos, "et correspond à", usern)

        page = 0
        page = jourTransfo(jour)  # transforme le jour en numéro de page

        wks = sh[page]  # lecture du document du jour

        nom = wks.get_values('D1', 'D2')  # lit le titre

        if nom != [['Entraînement']]:
            inscrit = wks.get_values('B17', 'B40')  # récupère les inscrits
            role = wks.get_values('C17', 'C40')  # recupère les roles
            commentaire = wks.get_values('D17', 'D40')  # recupère les commentaires
        else:
            inscrit = wks.get_values('B8', 'B31')  # récupère les inscrits
            role = wks.get_values('C8', 'C31')  # recupère les roles
            commentaire = wks.get_values('D8', 'D31')  # recupère les commentaires

        # print(inscrit)

        if usern in inscrit:  # si l'utilisateur est inscrit

            # cherche dans la liste des inscrits
            for i in range(0, len(inscrit)):  # parcours la liste des inscrits
                if inscrit[i] == usern:  # si on est a la position de l'utilisateur
                    inscrit[i] = ['']  # suprime l'utilisateur
                    if len(role) > i:
                        role[i] = ['']  # supprime son role souhaité
                    if len(commentaire) > i:
                        commentaire[i] = ['']  # supprime son commentaire

            if nom != [['Entraînement']]:
                wks.update_values('B17:B40', inscrit)  # met à jour la liste des inscrits
                wks.update_values('C17:C40', role)  # met à jour la liste des roles
                wks.update_values('D17:D40', commentaire)  # met à jour la liste des commentaires
            else:
                wks.update_values('B8:B31', inscrit)  # met à jour la liste des inscrits
                wks.update_values('C8:C31', role)  # met à jour la liste des roles

            # print("utilisateur désinscrit")
            date(user)
            return 1  # sort de la fonction

        else:  # si l'utilisateur n'est pas dans la liste des inscrits
            # print("utilistateur", usern, "est déjà désinscrit")
            return 0  # sort de la fonction

    else:  # si l'utilisateur n'est pas dans dico ou le jour est incorrect
        # print("Erreur : user n'est pas dans le dico")
        return 2  # sort de la fonction

# est appellé par le bot
# deincrit tous les utilisateurs au jour demandé
# supprime aussi le nom de la mission, du Zeus, et le brief
def clear(jour):
    page = 0
    page = jourTransfo(jour)  # transforme le jour en page
    print("Nettoyage de la page", page, "correspondant à", jourNom[jour])
    wks = sh[page]  # ouvre la page correspondante

    liste15 = [[''], [''], [''], [''], [''], [''], [''], [''], [''], [''], [''], [''], [''], [''], ['']]  # crée une liste vide
    liste10 = [[''], [''], [''], [''], [''], [''], [''], [''], [''], ['']]

    nom = wks.get_values('D1', 'D2')  # lit le titre
    # print(nom)
    if nom != [['Entraînement']]:
        # Titre
        wks.update_values('D1', [['']])
        # Zeus
        wks.update_values('E3', [['']])
        # Brief
        wks.update_values('B7', [['']])

    clearJoueur(jour)

    print("Nettoyage done")
    # met un message dans la console indiquant la page et le jour nettoyé
    

# est appellé par le bot et la fonction clear
# deincrit tous les utilisateurs au jour demandé
def clearJoueur(jour):
    page = 0
    page = jourTransfo(jour)  # transforme le jour en page
    print("Nettoyage des inscrit de la page", page, "correspondant à", jourNom[jour])
    wks = sh[page]  # ouvre la page correspondante

    liste15 = [[''], [''], [''], [''], [''], [''], [''], [''], [''], [''], [''], [''], [''], [''], ['']]  # crée une liste vide
    liste10 = [[''], [''], [''], [''], [''], [''], [''], [''], [''], ['']]

    nom = wks.get_values('D1', 'D2')  # lit le titre
    if nom != [['Entraînement']]:
        # liste des joueurs
        wks.update_values('B17:B32', liste15)
        wks.update_values('B32:B47', liste10)
        # liste des roles
        wks.update_values('C17:C32', liste15)
        wks.update_values('C32:C47', liste10)
        # liste des comantaires
        wks.update_values('D17:D32', liste15)
        wks.update_values('D32:D47', liste10)

        # sanglier
        wks.update_values('G19:G33', liste15)
        # grizzli
        wks.update_values('J19:J33', liste15)

        # Albatros
        wks.update_values('M21:M24', [[''], [''], [''], ['']])
        # Harfang
        wks.update_values('M27:M30', [[''], [''], [''], ['']])

        # CROCODILE
        wks.update_values('G37:G39', [[''], [''], ['']])
        # ALIGATOR
        wks.update_values('J37:J39', [[''], [''], ['']])
    else:
        # liste des joueurs
        wks.update_values('B8:B22', liste15)
        wks.update_values('B23:B38', liste15)
        # liste des commentaires
        wks.update_values('C8:C22', liste15)
        wks.update_values('C23:C38', liste15)

        # gerant module 1
        wks.update_values('G13', [['']])
        # liste des incrits Module 1
        wks.update_values('F16:F25', liste10)
        # liste des affectation Module 1
        wks.update_values('G16:G25', liste10)

        # gerant module 2
        wks.update_values('J13', [['']])
        # liste des incrits Module 2
        wks.update_values('I16:I25', liste10)
        # liste des affectation Module 2
        wks.update_values('J16:J25', liste10)

        # gerant module 3
        wks.update_values('M13', [['']])
        # liste des incrits Module 3
        wks.update_values('L16:L25', liste10)
        # liste des affectation Module 3
        wks.update_values('M16:M25', liste10)

# est appellé par le bot
# retourne 0 si pas de missions
# retourne msg si il y a une mission
def message(jour):
    orga(jour)
    page = jourTransfo(jour)  # transforme le jour en page
    wks = sh[page]  # ouvre la page

    name = wks.get_values('D1', 'D2')  # lit le titre
    # print("jour", jour, "page", page, "name", name)

    zeus = wks.get_values('E3', 'E3')  # lit le zeus
    brief = wks.get_values('B7', 'B7')  # lit le brief

    # print("inscrit : ", inscrit[0])
    # print("role : ", role[0])

    if name == [['Entraînement']]:
        inscrit = wks.get_values('B8', 'B31')  # récupère les inscrits
        role = wks.get_values('C8', 'C31')  # recupère les roles

        while len(inscrit) > len(role):
            role.append(['GV'])

        msg = "<@&" + str(secrets.ROLE_ID) + "> **" + name[0][0] + "** " + jourNom[jour] + \
              " soir : \nLe drill est la clef, venez vous entraîner ! \nInscrivez vous en réagissant ou directement " \
              "sur le planning : " + secrets.LINKS[jour]
        return msg  # renvoie le message
    elif name[0][0] == '':  # si pas de mission
        # print("pas de mission")
        return 0  # renvoie 0
    
    else:
        inscrit = wks.get_values('B17', 'B40')
        role = wks.get_values('C17', 'C40')
        commentaire = wks.get_values('D17', 'D40')

        Sanglier = wks.get_values('G19', 'G33')             # lit le groupe sanglier (G19:G33)
        Grizzli = wks.get_values('J19', 'J33')              # lit le groupe Grizzli (J19:J33)
        Albatros = wks.get_values('M21', 'M24')             # lit le groupe Albatros (M21:M24)
        Harfang = wks.get_values('M27', 'M30')              # lit le groupe Harfang (M27:M30)
        Crocodile = wks.get_values('G37', 'G39')            # lit le groupe Crocodile (G37:G39)
        Aligator = wks.get_values('J37', 'J39')             # lit le groupe Aligator (J37:J39)

        while len(inscrit) > len(role):
            role.append(['GV'])

        # print(name)
        # crée le message d'annonce
        msg = "<@&" + str(secrets.ROLE_ID) + "> **" + name[0][0] + "** organisée par __" 
        if UserToID(zeus[0][0]) != False:
            msg += "<@" + UserToID(zeus[0][0]) + ">"
        else:
            msg += zeus[0][0]

        msg += "__ " + jourNom[jour] + " soir, à 20h45, voici le briefing : ```" + brief[0][0] + "\n```Inscrivez vous en réagissant ou directement sur le planning : " \
            + secrets.LINKS[jour]

        Sanglier += [[''], [''], [''], [''], [''], [''], [''], [''], [''], [''], [''], [''], [''], ['']]
        Grizzli += [[''], [''], [''], [''], [''], [''], [''], [''], [''], [''], [''], [''], [''], ['']]
        Albatros += [[''], [''], [''], ['']]
        Harfang += [[''], [''], [''], ['']]
        Crocodile += [[''], [''], ['']]
        Aligator += [[''], [''], ['']]

        SanglierA = False
        for i in Sanglier:
            if i != ['']:
                SanglierA = True

        GrizzliA = False
        for i in Grizzli:
            if i != ['']:
                GrizzliA = True

        AlbatrosA = False
        for i in Albatros:
            if i != ['']:
                AlbatrosA = True

        HarfangA = False
        for i in Harfang:
            if i != ['']:
                HarfangA = True

        CrocodileA = False
        for i in Crocodile:
            if i != ['']:
                CrocodileA = True

        AligatorA = False
        for i in Aligator:
            if i != ['']:
                AligatorA = True
        
        if SanglierA or GrizzliA or AlbatrosA or HarfangA or CrocodileA or AligatorA:
            # print("Affectation :")
            #msg = "<@&" + str(secrets.ROLE_ID) + "> Voici les affectation pour se soir : \n"
            if SanglierA:
                msg += "\n**Sanglier :**"
                msg += "\n*Blanc :*"        #Blanc
                if Sanglier[0] != ['']:
                    if UserToID(Sanglier[0][0]) != False:
                        msg += "\n\t <:cdg:" + str(secrets.CDG_EMOTE_ID) + ">\t<@" + UserToID(Sanglier[0][0]) + ">"
                    else:
                        msg += "\n\t <:cdg:" + str(secrets.CDG_EMOTE_ID) + ">\t" + Sanglier[0][0]

                if Sanglier[1] != ['']:
                    if UserToID(Sanglier[1][0]) != False:
                        msg += "\n\t <:medecin:" + str(secrets.MED_EMOTE_ID) + ">\t<@" + UserToID(Sanglier[1][0]) + ">"
                    else:
                        msg += "\n\t <:medecin:" + str(secrets.MED_EMOTE_ID) + ">\t" + Sanglier[1][0]

                if Sanglier[2] != ['']:
                    if UserToID(Sanglier[2][0]) != False:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Sanglier[2][0]) + ">"
                    else:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Sanglier[2][0]

                if Sanglier[3] != ['']:
                    if UserToID(Sanglier[3][0]) != False:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Sanglier[3][0]) + ">"
                    else:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Sanglier[3][0]

                if Sanglier[4] != [''] or Sanglier[5] != [''] or Sanglier[6] != [''] or Sanglier[7] != ['']:
                    msg += "\n*Bleu :*"         #Bleu
                    if Sanglier[4] != ['']:
                        if UserToID(Sanglier[4][0]) != False:
                            msg += "\n\t <:cde:" + str(secrets.CDE_EMOTE_ID) + ">\t<@" + UserToID(Sanglier[4][0]) + ">"
                        else:
                            msg += "\n\t <:cde:" + str(secrets.CDE_EMOTE_ID) + ">\t" + Sanglier[4][0]

                    if Sanglier[5] != ['']:
                        if UserToID(Sanglier[5][0]) != False:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Sanglier[5][0]) + ">"
                        else:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Sanglier[5][0]
                    if Sanglier[6] != ['']:
                        if UserToID(Sanglier[6][0]) != False:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Sanglier[6][0]) + ">"
                        else:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Sanglier[6][0]

                    if Sanglier[7] != ['']:
                        if UserToID(Sanglier[7][0]) != False:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Sanglier[7][0]) + ">"
                        else:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Sanglier[7][0]

                if Sanglier[8] != [''] or Sanglier[9] != [''] or Sanglier[10] != [''] or Sanglier[11] != ['']:
                    msg += "\n*Vert :*"         # Vert
                    if Sanglier[8] != ['']:
                        if UserToID(Sanglier[8][0]) != False:
                            msg += "\n\t <:cde:" + str(secrets.CDE_EMOTE_ID) + ">\t<@" + UserToID(Sanglier[8][0]) + ">"
                        else:
                            msg += "\n\t <:cde:" + str(secrets.CDE_EMOTE_ID) + ">\t" + Sanglier[8][0]

                    if Sanglier[9] != ['']:
                        if UserToID(Sanglier[9][0]) != False:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Sanglier[9][0]) + ">"
                        else:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Sanglier[9][0]

                    if Sanglier[10] != ['']:
                        if UserToID(Sanglier[10][0]) != False:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Sanglier[10][0]) + ">"
                        else:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Sanglier[10][0]

                    if Sanglier[11] != ['']:
                        if UserToID(Sanglier[11][0]) != False:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Sanglier[11][0]) + ">"
                        else:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Sanglier[11][0]


                if Sanglier[12] != [''] or Sanglier[13] != ['']:
                    msg += "\n*Rouge :*"    # Rouge
                    if Sanglier[12] != ['']:
                        if UserToID(Sanglier[12][0]) != False:
                            msg += "\n\t <:cde:" + str(secrets.CDE_EMOTE_ID) + ">\t<@" + UserToID(Sanglier[12][0]) + ">"
                        else:
                            msg += "\n\t <:cde:" + str(secrets.CDE_EMOTE_ID) + ">\t" + Sanglier[12][0]

                    if Sanglier[13] != ['']:
                        if UserToID(Sanglier[13][0]) != False:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Sanglier[13][0]) + ">"
                        else:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Sanglier[13][0]

                if Sanglier[14] != ['']:
                    if UserToID(Sanglier[14][0]) != False:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Sanglier[14][0]) + ">"
                    else: 
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Sanglier[14][0]

            # print("Sanglier OK")

            if GrizzliA:
                msg += "\n**Grizzli :**"
                msg += "\n*Blanc :*"        #Blanc
                if Grizzli[0] != ['']:
                    if UserToID(Grizzli[0][0]) != False:
                        msg += "\n\t <:cdg:" + str(secrets.CDG_EMOTE_ID) + ">\t<@" + UserToID(Grizzli[0][0]) + ">"
                    else:
                        msg += "\n\t <:cdg:" + str(secrets.CDG_EMOTE_ID) + ">\t" + Grizzli[0][0]

                if Grizzli[1] != ['']:
                    if UserToID(Grizzli[1][0]) != False:
                        msg += "\n\t <:medecin:" + str(secrets.MED_EMOTE_ID) + ">\t<@" + UserToID(Grizzli[1][0]) + ">"
                    else:
                        msg += "\n\t <:medecin:" + str(secrets.MED_EMOTE_ID) + ">\t" + Grizzli[1][0]

                if Grizzli[2] != ['']:
                    if UserToID(Grizzli[2][0]) != False:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Grizzli[2][0]) + ">"
                    else:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Grizzli[2][0]

                if Grizzli[3] != ['']:
                    if UserToID(Grizzli[3][0]) != False:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Grizzli[3][0]) + ">"
                    else:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Grizzli[3][0]

                if Grizzli[4] != [''] or Grizzli[5] != [''] or Grizzli[6] != [''] or Grizzli[7] != ['']:
                    msg += "\n*Bleu :*"         #Bleu
                    if Grizzli[4] != ['']:
                        if UserToID(Grizzli[4][0]) != False:
                            msg += "\n\t <:cde:" + str(secrets.CDE_EMOTE_ID) + ">\t<@" + UserToID(Grizzli[4][0]) + ">"
                        else:
                            msg += "\n\t <:cde:" + str(secrets.CDE_EMOTE_ID) + ">\t" + Grizzli[4][0]

                    if Grizzli[5] != ['']:
                        if UserToID(Grizzli[5][0]) != False:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Grizzli[5][0]) + ">"
                        else:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Grizzli[5][0]
                    if Grizzli[6] != ['']:
                        if UserToID(Grizzli[6][0]) != False:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Grizzli[6][0]) + ">"
                        else:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Grizzli[6][0]

                    if Grizzli[7] != ['']:
                        if UserToID(Grizzli[7][0]) != False:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Grizzli[7][0]) + ">"
                        else:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Grizzli[7][0]

                if Grizzli[8] != [''] or Grizzli[9] != [''] or Grizzli[10] != [''] or Grizzli[11] != ['']:
                    msg += "\n*Vert :*"         # Vert
                    if Grizzli[8] != ['']:
                        if UserToID(Grizzli[8][0]) != False:
                            msg += "\n\t <:cde:" + str(secrets.CDE_EMOTE_ID) + ">\t<@" + UserToID(Grizzli[8][0]) + ">"
                        else:
                            msg += "\n\t <:cde:" + str(secrets.CDE_EMOTE_ID) + ">\t" + Grizzli[8][0]

                    if Grizzli[9] != ['']:
                        if UserToID(Grizzli[9][0]) != False:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Grizzli[9][0]) + ">"
                        else:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Grizzli[9][0]

                    if Grizzli[10] != ['']:
                        if UserToID(Grizzli[10][0]) != False:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Grizzli[10][0]) + ">"
                        else:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Grizzli[10][0]

                    if Grizzli[11] != ['']:
                        if UserToID(Grizzli[11][0]) != False:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Grizzli[11][0]) + ">"
                        else:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Grizzli[11][0]


                if Grizzli[12] != [''] or Grizzli[13] != ['']:
                    msg += "\n*Rouge :*"    # Rouge
                    if Grizzli[12] != ['']:
                        if UserToID(Grizzli[12][0]) != False:
                            msg += "\n\t <:cde:" + str(secrets.CDE_EMOTE_ID) + ">\t<@" + UserToID(Grizzli[12][0]) + ">"
                        else:
                            msg += "\n\t <:cde:" + str(secrets.CDE_EMOTE_ID) + ">\t" + Grizzli[12][0]

                    if Grizzli[13] != ['']:
                        if UserToID(Grizzli[13][0]) != False:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Grizzli[13][0]) + ">"
                        else:
                            msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Grizzli[13][0]

                if Grizzli[14] != ['']:
                    if UserToID(Grizzli[14][0]) != False:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Grizzli[14][0]) + ">"
                    else: 
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Grizzli[14][0]
            # print("Grizzli OK")

            if AlbatrosA:
                msg += "\n\n**Albatros :**"
                if Albatros[0] != ['']: 
                    if UserToID(Albatros[0][0]) != False:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID)+ ">\t<@" + UserToID(Albatros[0][0]) + ">"
                    else:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID)+ ">\t" + Albatros[0][0]
                if Albatros[1] != ['']:
                    if UserToID(Albatros[1][0]) != False:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID)+ ">\t<@" + UserToID(Albatros[1][0]) + ">"
                    else:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID)+ ">\t" + Albatros[1][0]
                if Albatros[2] != ['']:
                    if UserToID(Albatros[2][0]) != False:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID)+ ">\t<@" + UserToID(Albatros[2][0]) + ">"
                    else:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID)+ ">\t" + Albatros[2][0]
                if Albatros[3] != ['']:
                    if UserToID(Albatros[3][0]) != False:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID)+ ">\t<@" + UserToID(Albatros[3][0]) + ">"
                    else:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID)+ ">\t" + Albatros[3][0]
            # print("Albatros OK")

            if HarfangA:
                msg += "\n\n**Harfang :**"
                if Harfang[0] != ['']: 
                    if UserToID(Harfang[0][0]) != False:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID)+ ">\t<@" + UserToID(Harfang[0][0]) + ">"
                    else:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID)+ ">\t" + Harfang[0][0]
                if Harfang[1] != ['']:
                    if UserToID(Harfang[1][0]) != False:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID)+ ">\t<@" + UserToID(Harfang[1][0]) + ">"
                    else:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID)+ ">\t" + Harfang[1][0]
                if Harfang[2] != ['']:
                    if UserToID(Harfang[2][0]) != False:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID)+ ">\t<@" + UserToID(Harfang[2][0]) + ">"
                    else:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID)+ ">\t" + Harfang[2][0]
                if Harfang[3] != ['']:
                    if UserToID(Harfang[3][0]) != False:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID)+ ">\t<@" + UserToID(Harfang[3][0]) + ">"
                    else:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID)+ ">\t" + Harfang[3][0]
            # print("Harfang OK")

            if CrocodileA:
                msg += "\n\n**Crocodile :**"
                if Crocodile[0] != ['']:
                    if UserToID(Crocodile[0][0]) != False:
                        msg += "\n\t <:cdg:" + str(secrets.CDG_EMOTE_ID) + ">\t<@" + UserToID(Crocodile[0][0]) + ">"
                    else:
                        msg += "\n\t <:cdg:" + str(secrets.CDG_EMOTE_ID) + ">\t" + Crocodile[0][0]
                if Crocodile[1] != ['']:
                    if UserToID(Crocodile[1][0]) != False:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Crocodile[1][0]) + ">"
                    else:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Crocodile[1][0]
                if Crocodile[2] != ['']:
                    if UserToID(Crocodile[2][0]) != False:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Crocodile[2][0]) + ">"
                    else:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Crocodile[2][0]
            # print("Crotodile OK")

            if AligatorA:
                msg += "\n\n**Aligator :**"
                if Aligator[0] != ['']:
                    if UserToID(Aligator[0][0]) != False:
                        msg += "\n\t <:cdg:" + str(secrets.CDG_EMOTE_ID) + ">\t<@" + UserToID(Aligator[0][0]) + ">"
                    else:
                        msg += "\n\t <:cdg:" + str(secrets.CDG_EMOTE_ID) + ">\t" + Aligator[0][0]
                if Aligator[1] != ['']:
                    if UserToID(Aligator[1][0]) != False:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Aligator[1][0]) + ">"
                    else:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Aligator[1][0]
                if Aligator[2] != ['']:
                    if UserToID(Aligator[2][0]) != False:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t<@" + UserToID(Aligator[2][0]) + ">"
                    else:
                        msg += "\n\t <:DIS:" + str(secrets.DIS_EMOTE_ID) + ">\t" + Aligator[2][0]
            # print("Aligator OK")

        msg = msg + "\n**" + str(len(inscrit) - inscrit.count([''])) + " Joueurs**"

        for i in range(len(inscrit)):
            affecter = True #le personnelle est considéré comme affecté
            if Sanglier.count(inscrit[i]) == 0 and Grizzli.count(inscrit[i]) == 0 and \
                    Albatros.count(inscrit[i]) == 0  and Harfang.count(inscrit[i]) == 0 and \
                    Crocodile.count(inscrit[i]) == 0 and Aligator.count(inscrit[i]) == 0:   #si dans aucun groupe 
                affecter = False        #considéré comme non affecté

            if inscrit[i] != [''] and affecter == False:
                if role[i][0] == 'CDG':
                    msg += '\n\t<:cdg:' + str(secrets.CDG_EMOTE_ID) + '> '
                    if UserToID(zeus[0][0]) != False:
                        msg += "<@" + UserToID(inscrit[i][0]) + ">"
                    else:
                        msg += inscrit[i][0]

                    if len(commentaire) > i:
                        if commentaire[i][0] != '':
                            msg += " (" + commentaire[i][0] + ")"
                elif role[i][0] == 'CDE':
                    msg += '\n\t<:cde:' + str(secrets.CDE_EMOTE_ID) + '> '
                    if UserToID(zeus[0][0]) != False:
                        msg += "<@" + UserToID(inscrit[i][0]) + ">"
                    else:
                        msg += inscrit[i][0]

                    if len(commentaire) > i:
                        if commentaire[i][0] != '':
                            msg += " (" + commentaire[i][0] + ")"
                elif role[i][0] == 'Médecin':
                    msg += '\n\t<:medecin:' + str(secrets.MED_EMOTE_ID) + '> '
                    if UserToID(zeus[0][0]) != False:
                        msg += "<@" + UserToID(inscrit[i][0]) + ">"
                    else:
                        msg += inscrit[i][0]
                        
                    if len(commentaire) > i:
                        if commentaire[i][0] != '':
                            msg += " (" + commentaire[i][0] + ")"
                elif role[i][0] == 'Minimi':
                    msg += '\n\t<:mg:' + str(secrets.MINI_EMOTE_ID) + '> '
                    if UserToID(zeus[0][0]) != False:
                        msg += "<@" + UserToID(inscrit[i][0]) + ">"
                    else:
                        msg += inscrit[i][0]
                        
                    if len(commentaire) > i:
                        if commentaire[i][0] != '':
                            msg += " (" + commentaire[i][0] + ")"
                elif role[i][0] == 'GV':
                    msg += '\n\t<:DIS:' + str(secrets.DIS_EMOTE_ID) + '> '
                    if UserToID(zeus[0][0]) != False:
                        msg += "<@" + UserToID(inscrit[i][0]) + ">"
                    else:
                        msg += inscrit[i][0]
                        
                    if len(commentaire) > i:
                        if commentaire[i][0] != '':
                            msg += " (" + commentaire[i][0] + ")"
                else:
                    msg += '\n\t<:DIS:' + str(secrets.DIS_EMOTE_ID) + '> '
                    if UserToID(zeus[0][0]) != False:
                        msg += "<@" + UserToID(inscrit[i][0]) + ">"
                    else:
                        msg += inscrit[i][0]                    
                    
                    msg += " (" + role[i][0]
                    if len(commentaire) > i:
                        if commentaire[i][0] != '':
                            msg += ", " + commentaire[i][0]
                    msg += ")" 

        return msg  # renvoie le message

# est appellé par le bot
# retourne le mots écrit en position A1 du tableau
def jourPage(page):
    wks = sh[page]  # ouvre la page correspondante
    nom = wks.get_values('A1', 'A2')  # lit le titre
    return nom[0][0]

# est appellé par le bot
# ajoute un utilisateur dans le dico
def addUser(user, id):
    wks = sh[10]  # ouvre la page Technique

    name = wks.get_values('D1', 'D2')  # lit le titre
    # print(name)

    if name == [['Détails techniques (ne PAS toucher)']]:
        cont = True
        i = 7
        while cont:
            i = i + 1
            case = 'B' + str(i)
            contenue = wks.get_values(case, case)
            # print(case, ":", contenue)

            if contenue == [['']]:
                cont = False
            elif case == "B200":
                return -1

        range = 'B' + str(i)
        text = [[str(user)]]
        wks.update_values(range, text)

        range = 'C' + str(i)
        text = [[str(id)]]
        wks.update_values(range, text)

        date(user)

    return 0

# est appellé par le bot
# enlève un utilisateur dans le dico
def remUser(id):
    dico = init()  # initialise dico
    user = str(id)  # récupère l'id de l'utilisateur

    LigneVide = [['', '', '', '', '', '', '', '', '', '', '', '', '']]

    wks = sh[10]  # ouvre la page Technique

    name = wks.get_values('D1', 'D2')  # lit le titre
    # print(name)

    if name == [['Détails techniques (ne PAS toucher)']]:
        if (user in dico[1]):
            pos = dico[1].index(user)  # recupère la position de l'id de l'utilisateur
            ln = pos + 8
            area = 'B' + str(ln) + 'O' + str(ln)
            # userLn = wks.get_values(rangeB, rangeO)
            wks.update_values(area, LigneVide)
    return 0

# est appellé par le bot
# renvoie le nom de la mission
def missionName(jour):
    page = jourTransfo(jour)  # transforme le jour en numéro de pag
    wks = sh[page]  # lecture du document du jour
    nom = wks.get_values('D1', 'D2')  # lit le titre
    # print(nom)
    return nom[0][0]

# Organise la page du jours dans l'ordre des roles
def orga(jour):
    page = jourTransfo(jour)  # transforme le jour en numéro de pag
    wks = sh[page]  # lecture du document du jour
    nom = wks.get_values('D1', 'D2')  # lit le titre

    if nom != [['']] and nom != [['Entraînement']]:
        inscrit = wks.get_values('B17', 'B40')
        role = wks.get_values('C17', 'C40')
        commentaire = wks.get_values('D17', 'D40')

        Tech = sh[10]  # ouvre la page Technique

        importance = Tech.get_values('Q8', 'Q20')
        importance.append([''])
        # print(importance)

        while len(inscrit) > len(role):
            role.append(['GV'])

        while len(commentaire) < len(inscrit):
            commentaire.append([''])

        for i in range(len(role)):
            for j in range(0, i):
                # print('\t', role[j][0], importance.index(role[j]))
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
            # print(role[i][0], importance.index(role[i]))

        # for i in range(len(inscrit)):
        #     print(inscrit[i][0], ' ', role[i][0])
        # print(inscrit)
        # print(role)
        wks.update_values('B17:B40', inscrit)  # met à jour le google sheet
        wks.update_values('C17:C40', role)  # met à jour la liste des roles
        wks.update_values('D17:D40', commentaire)  # met à jour la liste des roles

#transforme un ID en username
def IdToUser(ID):
    dico = init()  # initialise dico
    user = str(ID)  # récupère l'id de l'utilisateur
    if user in dico[1]:
        pos = dico[1].index(user)
        return dico[0][pos][0]
    else:
        return False

#transforme un username en ID
def UserToID(user):
    dico = init()  # initialise dico
    user = [str(user)]  # récupère l'id de l'utilisateur
    if user in dico[0]:
        pos = dico[0].index(user)
        return dico[1][pos]
    else:
        return False

