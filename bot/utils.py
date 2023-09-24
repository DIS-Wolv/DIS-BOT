"""Utils for the bot."""
from datetime import datetime
from bot.secrets import ROLE_ID


def mention(msg):
    """
    test si il y a la mention du rôle
    renvoie
     1 si oui
     0 si non
    """
    role = "<@&" + str(ROLE_ID) + ">"
    if role in msg:  # si la mention est dans le message
        return 1
    return 0


def jour(msg):
    """cherche le jour dans un message"""
    jours = [
        "planning",
        "LUNDI",
        "MARDI",
        "MERCREDI",
        "JEUDI",
        "VENDREDI",
        "SAMEDI",
        "DIMANCHE",
    ]

    msg_upper = msg.upper()
    for i, j in enumerate(jours):
        if j in msg_upper:
            return i
    if f" {jours} " in msg.upper():  # si la mention est dans le message
        return 1
    return 0


def mots(msg, mot):
    """cherche un mot dans un message et renvoie sa position"""
    mots_upper_list = msg.upper().split(" ")
    mot_upper = mot.upper()

    for i, todo in enumerate(mots_upper_list):
        if todo == mot_upper:
            return i
    return -1


def log(msg: str) -> None:
    """Log infos."""
    print(datetime.now(), msg)
