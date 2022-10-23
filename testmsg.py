import secrets

# test si il y a la mention du rôle
# renvoie 1 si oui
# renvoie 0 si non
def mention(msg):
    role = '<@&' + str(secrets.ROLE_ID) + '>'

    msg = msg.split(' ')  # découpe suivant les espaces
    for i in range(len(msg)):  # pour chaque morceau
        if msg[i] == role:  # si le mot est égal à la mention
            return 1  # renvoie 1
    return 0  # renvoie 0

# cherche le jour dans un message
def jour(msg):
    jour = ['planning', 'LUNDI', 'MARDI', 'MERCREDI', 'JEUDI', 'VENDREDI', 'SAMEDI', 'DIMANCHE']  # défini la liste des jours

    njour = 0  # défini une valeur défaut au numéro du jour
    msg = msg.split(' ')  # découpe le message suivant les espaces
    for i in range(0, len(msg)):  # pour chaque morceau
        a = msg[i].upper()  # defini "a" égal au mot en majuscule
        # print(a, type(a), jour)
        if a in jour:  # si "a" est dans la liste
            njour = jour.index(a)  # numéro du jour prend la valeur de l'index du jour dans la liste
            return njour  # renvoie le numéro du jour
    return 0  # renvoie 0

# cherche un mots dans un message et renvoie ca position
def mots(msg, mots):
    msg = msg.split(' ')  # découpe le message suivant les espaces

    for i in range(0, len(msg)):  # pour chaque mots
        a = msg[i].upper()  # defini "a" égal au mot en majuscule
        # print(a, type(a), jour)
        if a == mots.upper():  # si "a" est dans la liste
            return i  # renvoie le numéro du jour
    return -1 # renvoie 0

