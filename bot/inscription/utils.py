from bot.inscription.google import sh
from bot.tracing import TRACER
from opentelemetry import trace


@TRACER.start_as_current_span("bot.inscription.utils.init")
def init():
    """
    est appellé pour initialiser dico
    retourne dico

    dico = [
        [["pseudo1"], ["pseudo2"]],
        ["ID1", "ID2"]
    ]
    """
    dico = [[], []]

    # lis dans Technique
    read = sh[10].get_values("B8", "C600")

    for line in read:
        # each line is ["pseudo", "id"]
        dico[0].append([line[0]])
        dico[1].append(line[1])

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
