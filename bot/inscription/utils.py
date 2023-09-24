from bot.inscription.google import sh
from bot.tracing import TRACER


@TRACER.start_as_current_span("bot.inscription.utils.init")
def init():
    """
    est appellé pour initialiser dico
    retourne dico
    """
    # selection de la fiche technique
    wks = sh[10]
    # création et complétion du dico
    dico = ["nom", "ID"]

    read = wks.get_values("B8", "B600")  # lit les pseudos
    dico[0] = read  # met les pseudos dans la première colonne de dico

    read = wks.get_values("C8", "C600")  # lis les ID
    for i in range(0, len(read)):
        read[i] = read[i][0]
    dico[1] = read  # met les IDs dans la 2e colonne de dico
    # print("dico initialisé")
    # print(dico)
    return dico


def jourTransfo(jour):
    """
    est appellé par les autres fonctions
    transforme le jour en numéro de page
    retourne le numéro de la page
    """
    if jour <= 5:  # de lundi a Vendredi le numéro du jour = numéro de la page
        page = jour
    elif jour == 6:  # décalage du a la page samedi aprem
        page = 7
    elif jour == 7:  # décalage du a la page dimanche aprem
        page = 9
    else:
        page = 0

    return page


def IdToUser(ID, dico):
    """
    transforme un ID en username
    """
    # dico = init()  # initialise dico
    user = str(ID)  # récupère l'id de l'utilisateur
    if user in dico[1]:
        pos = dico[1].index(user)
        return dico[0][pos][0]
    else:
        return False


def UserToID(user, dico):
    """
    transforme un username en ID
    """
    # dico = init()  # initialise dico
    user = [str(user)]  # récupère l'id de l'utilisateur
    if user in dico[0]:
        pos = dico[0].index(user)
        return dico[1][pos]
    else:
        return False


def slice_in_matrix(
    matrix: list[list], xmin: int, xmax: int, ymin: int, ymax: int
) -> list[list]:
    """Slice a matrix."""
    return [row[xmin:xmax] for row in matrix[ymin:ymax]]
