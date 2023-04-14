from bot import secrets

from bot.inscription.utils import UserToID
from bot.inscription.constants import jourNom

def build_msg(dico, jour, name, zeus, brief, inscrit, role, commentaire, Sanglier, Crocodile, Grizzli, Aligator, Albatros, Harfang):
    """crée le message d'annonce"""
    msg = "<@&" + str(secrets.ROLE_ID) + "> **" + name[0][0] + "** organisée par __"
    if UserToID(zeus[0][0], dico) != False:
        msg += "<@" + UserToID(zeus[0][0], dico) + ">"
    else:
        msg += zeus[0][0]

    msg += (
        "__ "
        + jourNom[jour]
        + " soir, à 20h45, voici le briefing : ```"
        + brief[0][0]
        + "\n```Inscrivez vous en réagissant ou directement sur le planning : "
        + secrets.LINKS[jour]
    )

    Sanglier += [
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
    ]
    Grizzli += [
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
    ]
    Albatros += [[""], [""], [""], [""]]
    Harfang += [[""], [""], [""], [""]]
    Crocodile += [[""], [""], [""]]
    Aligator += [[""], [""], [""]]

    SanglierA = False
    for i in Sanglier:
        if i != [""]:
            SanglierA = True

    GrizzliA = False
    for i in Grizzli:
        if i != [""]:
            GrizzliA = True

    AlbatrosA = False
    for i in Albatros:
        if i != [""]:
            AlbatrosA = True

    HarfangA = False
    for i in Harfang:
        if i != [""]:
            HarfangA = True

    CrocodileA = False
    for i in Crocodile:
        if i != [""]:
            CrocodileA = True

    AligatorA = False
    for i in Aligator:
        if i != [""]:
            AligatorA = True

    if SanglierA or GrizzliA or AlbatrosA or HarfangA or CrocodileA or AligatorA:
        # print("Affectation :")
        # msg = "<@&" + str(secrets.ROLE_ID) + "> Voici les affectation pour se soir : \n"
        if SanglierA:
            msg += "\n**Sanglier :**"
            msg += "\n*Blanc :*"  # Blanc
            if Sanglier[0] != [""]:
                if UserToID(Sanglier[0][0], dico) != False:
                    msg += (
                        "\n\t<:cdg:"
                        + str(secrets.CDG_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Sanglier[0][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:cdg:"
                        + str(secrets.CDG_EMOTE_ID)
                        + ">\t"
                        + Sanglier[0][0]
                    )

            if Sanglier[1] != [""]:
                if UserToID(Sanglier[1][0], dico) != False:
                    msg += (
                        "\n\t<:medecin:"
                        + str(secrets.MED_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Sanglier[1][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:medecin:"
                        + str(secrets.MED_EMOTE_ID)
                        + ">\t"
                        + Sanglier[1][0]
                    )

            if Sanglier[2] != [""]:
                if UserToID(Sanglier[2][0], dico) != False:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Sanglier[2][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t"
                        + Sanglier[2][0]
                    )

            if Sanglier[3] != [""]:
                if UserToID(Sanglier[3][0], dico) != False:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Sanglier[3][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t"
                        + Sanglier[3][0]
                    )

            if (
                Sanglier[4] != [""]
                or Sanglier[5] != [""]
                or Sanglier[6] != [""]
                or Sanglier[7] != [""]
            ):
                msg += "\n*Bleu :*"  # Bleu
                if Sanglier[4] != [""]:
                    if UserToID(Sanglier[4][0], dico) != False:
                        msg += (
                            "\n\t<:cde:"
                            + str(secrets.CDE_EMOTE_ID)
                            + ">\t<@"
                            + UserToID(Sanglier[4][0], dico)
                            + ">"
                        )
                    else:
                        msg += (
                            "\n\t<:cde:"
                            + str(secrets.CDE_EMOTE_ID)
                            + ">\t"
                            + Sanglier[4][0]
                        )

                if Sanglier[5] != [""]:
                    if UserToID(Sanglier[5][0], dico) != False:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t<@"
                            + UserToID(Sanglier[5][0], dico)
                            + ">"
                        )
                    else:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t"
                            + Sanglier[5][0]
                        )
                if Sanglier[6] != [""]:
                    if UserToID(Sanglier[6][0], dico) != False:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t<@"
                            + UserToID(Sanglier[6][0], dico)
                            + ">"
                        )
                    else:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t"
                            + Sanglier[6][0]
                        )

                if Sanglier[7] != [""]:
                    if UserToID(Sanglier[7][0], dico) != False:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t<@"
                            + UserToID(Sanglier[7][0], dico)
                            + ">"
                        )
                    else:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t"
                            + Sanglier[7][0]
                        )

            if (
                Sanglier[8] != [""]
                or Sanglier[9] != [""]
                or Sanglier[10] != [""]
                or Sanglier[11] != [""]
            ):
                msg += "\n*Vert :*"  # Vert
                if Sanglier[8] != [""]:
                    if UserToID(Sanglier[8][0], dico) != False:
                        msg += (
                            "\n\t<:cde:"
                            + str(secrets.CDE_EMOTE_ID)
                            + ">\t<@"
                            + UserToID(Sanglier[8][0], dico)
                            + ">"
                        )
                    else:
                        msg += (
                            "\n\t<:cde:"
                            + str(secrets.CDE_EMOTE_ID)
                            + ">\t"
                            + Sanglier[8][0]
                        )

                if Sanglier[9] != [""]:
                    if UserToID(Sanglier[9][0], dico) != False:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t<@"
                            + UserToID(Sanglier[9][0], dico)
                            + ">"
                        )
                    else:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t"
                            + Sanglier[9][0]
                        )

                if Sanglier[10] != [""]:
                    if UserToID(Sanglier[10][0], dico) != False:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t<@"
                            + UserToID(Sanglier[10][0], dico)
                            + ">"
                        )
                    else:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t"
                            + Sanglier[10][0]
                        )

                if Sanglier[11] != [""]:
                    if UserToID(Sanglier[11][0], dico) != False:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t<@"
                            + UserToID(Sanglier[11][0], dico)
                            + ">"
                        )
                    else:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t"
                            + Sanglier[11][0]
                        )

            if Sanglier[12] != [""] or Sanglier[13] != [""]:
                msg += "\n*Rouge :*"  # Rouge
                if Sanglier[12] != [""]:
                    if UserToID(Sanglier[12][0], dico) != False:
                        msg += (
                            "\n\t<:cde:"
                            + str(secrets.CDE_EMOTE_ID)
                            + ">\t<@"
                            + UserToID(Sanglier[12][0], dico)
                            + ">"
                        )
                    else:
                        msg += (
                            "\n\t<:cde:"
                            + str(secrets.CDE_EMOTE_ID)
                            + ">\t"
                            + Sanglier[12][0]
                        )

                if Sanglier[13] != [""]:
                    if UserToID(Sanglier[13][0], dico) != False:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t<@"
                            + UserToID(Sanglier[13][0], dico)
                            + ">"
                        )
                    else:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t"
                            + Sanglier[13][0]
                        )

            if Sanglier[14] != [""]:
                if UserToID(Sanglier[14][0], dico) != False:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Sanglier[14][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t"
                        + Sanglier[14][0]
                    )
        # print("Sanglier OK")

        if GrizzliA:
            msg += "\n**Grizzli :**"
            msg += "\n*Blanc :*"  # Blanc
            if Grizzli[0] != [""]:
                if UserToID(Grizzli[0][0], dico) != False:
                    msg += (
                        "\n\t<:cdg:"
                        + str(secrets.CDG_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Grizzli[0][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:cdg:"
                        + str(secrets.CDG_EMOTE_ID)
                        + ">\t"
                        + Grizzli[0][0]
                    )

            if Grizzli[1] != [""]:
                if UserToID(Grizzli[1][0], dico) != False:
                    msg += (
                        "\n\t<:medecin:"
                        + str(secrets.MED_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Grizzli[1][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:medecin:"
                        + str(secrets.MED_EMOTE_ID)
                        + ">\t"
                        + Grizzli[1][0]
                    )

            if Grizzli[2] != [""]:
                if UserToID(Grizzli[2][0], dico) != False:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Grizzli[2][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t"
                        + Grizzli[2][0]
                    )

            if Grizzli[3] != [""]:
                if UserToID(Grizzli[3][0], dico) != False:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Grizzli[3][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t"
                        + Grizzli[3][0]
                    )

            if (
                Grizzli[4] != [""]
                or Grizzli[5] != [""]
                or Grizzli[6] != [""]
                or Grizzli[7] != [""]
            ):
                msg += "\n*Bleu :*"  # Bleu
                if Grizzli[4] != [""]:
                    if UserToID(Grizzli[4][0], dico) != False:
                        msg += (
                            "\n\t<:cde:"
                            + str(secrets.CDE_EMOTE_ID)
                            + ">\t<@"
                            + UserToID(Grizzli[4][0], dico)
                            + ">"
                        )
                    else:
                        msg += (
                            "\n\t<:cde:"
                            + str(secrets.CDE_EMOTE_ID)
                            + ">\t"
                            + Grizzli[4][0]
                        )

                if Grizzli[5] != [""]:
                    if UserToID(Grizzli[5][0], dico) != False:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t<@"
                            + UserToID(Grizzli[5][0], dico)
                            + ">"
                        )
                    else:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t"
                            + Grizzli[5][0]
                        )
                if Grizzli[6] != [""]:
                    if UserToID(Grizzli[6][0], dico) != False:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t<@"
                            + UserToID(Grizzli[6][0], dico)
                            + ">"
                        )
                    else:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t"
                            + Grizzli[6][0]
                        )

                if Grizzli[7] != [""]:
                    if UserToID(Grizzli[7][0], dico) != False:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t<@"
                            + UserToID(Grizzli[7][0], dico)
                            + ">"
                        )
                    else:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t"
                            + Grizzli[7][0]
                        )

            if (
                Grizzli[8] != [""]
                or Grizzli[9] != [""]
                or Grizzli[10] != [""]
                or Grizzli[11] != [""]
            ):
                msg += "\n*Vert :*"  # Vert
                if Grizzli[8] != [""]:
                    if UserToID(Grizzli[8][0], dico) != False:
                        msg += (
                            "\n\t<:cde:"
                            + str(secrets.CDE_EMOTE_ID)
                            + ">\t<@"
                            + UserToID(Grizzli[8][0], dico)
                            + ">"
                        )
                    else:
                        msg += (
                            "\n\t<:cde:"
                            + str(secrets.CDE_EMOTE_ID)
                            + ">\t"
                            + Grizzli[8][0]
                        )

                if Grizzli[9] != [""]:
                    if UserToID(Grizzli[9][0], dico) != False:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t<@"
                            + UserToID(Grizzli[9][0], dico)
                            + ">"
                        )
                    else:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t"
                            + Grizzli[9][0]
                        )

                if Grizzli[10] != [""]:
                    if UserToID(Grizzli[10][0], dico) != False:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t<@"
                            + UserToID(Grizzli[10][0], dico)
                            + ">"
                        )
                    else:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t"
                            + Grizzli[10][0]
                        )

                if Grizzli[11] != [""]:
                    if UserToID(Grizzli[11][0], dico) != False:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t<@"
                            + UserToID(Grizzli[11][0], dico)
                            + ">"
                        )
                    else:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t"
                            + Grizzli[11][0]
                        )

            if Grizzli[12] != [""] or Grizzli[13] != [""]:
                msg += "\n*Rouge :*"  # Rouge
                if Grizzli[12] != [""]:
                    if UserToID(Grizzli[12][0], dico) != False:
                        msg += (
                            "\n\t<:cde:"
                            + str(secrets.CDE_EMOTE_ID)
                            + ">\t<@"
                            + UserToID(Grizzli[12][0], dico)
                            + ">"
                        )
                    else:
                        msg += (
                            "\n\t<:cde:"
                            + str(secrets.CDE_EMOTE_ID)
                            + ">\t"
                            + Grizzli[12][0]
                        )

                if Grizzli[13] != [""]:
                    if UserToID(Grizzli[13][0], dico) != False:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t<@"
                            + UserToID(Grizzli[13][0], dico)
                            + ">"
                        )
                    else:
                        msg += (
                            "\n\t<:DIS:"
                            + str(secrets.DIS_EMOTE_ID)
                            + ">\t"
                            + Grizzli[13][0]
                        )

            if Grizzli[14] != [""]:
                if UserToID(Grizzli[14][0], dico) != False:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Grizzli[14][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t"
                        + Grizzli[14][0]
                    )
        # print("Grizzli OK")

        if AlbatrosA:
            msg += "\n\n**Albatros :**"
            if Albatros[0] != [""]:
                if UserToID(Albatros[0][0], dico) != False:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Albatros[0][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t"
                        + Albatros[0][0]
                    )
            if Albatros[1] != [""]:
                if UserToID(Albatros[1][0], dico) != False:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Albatros[1][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t"
                        + Albatros[1][0]
                    )
            if Albatros[2] != [""]:
                if UserToID(Albatros[2][0], dico) != False:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Albatros[2][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t"
                        + Albatros[2][0]
                    )
            if Albatros[3] != [""]:
                if UserToID(Albatros[3][0], dico) != False:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Albatros[3][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t"
                        + Albatros[3][0]
                    )
        # print("Albatros OK")

        if HarfangA:
            msg += "\n\n**Harfang :**"
            if Harfang[0] != [""]:
                if UserToID(Harfang[0][0], dico) != False:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Harfang[0][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t"
                        + Harfang[0][0]
                    )
            if Harfang[1] != [""]:
                if UserToID(Harfang[1][0], dico) != False:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Harfang[1][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t"
                        + Harfang[1][0]
                    )
            if Harfang[2] != [""]:
                if UserToID(Harfang[2][0], dico) != False:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Harfang[2][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t"
                        + Harfang[2][0]
                    )
            if Harfang[3] != [""]:
                if UserToID(Harfang[3][0], dico) != False:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Harfang[3][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t"
                        + Harfang[3][0]
                    )
        # print("Harfang OK")

        if CrocodileA:
            msg += "\n\n**Crocodile :**"
            if Crocodile[0] != [""]:
                if UserToID(Crocodile[0][0], dico) != False:
                    msg += (
                        "\n\t<:cdg:"
                        + str(secrets.CDG_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Crocodile[0][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:cdg:"
                        + str(secrets.CDG_EMOTE_ID)
                        + ">\t"
                        + Crocodile[0][0]
                    )
            if Crocodile[1] != [""]:
                if UserToID(Crocodile[1][0], dico) != False:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Crocodile[1][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t"
                        + Crocodile[1][0]
                    )
            if Crocodile[2] != [""]:
                if UserToID(Crocodile[2][0], dico) != False:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Crocodile[2][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t"
                        + Crocodile[2][0]
                    )
        # print("Crotodile OK")

        if AligatorA:
            msg += "\n\n**Aligator :**"
            if Aligator[0] != [""]:
                if UserToID(Aligator[0][0], dico) != False:
                    msg += (
                        "\n\t<:cdg:"
                        + str(secrets.CDG_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Aligator[0][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:cdg:"
                        + str(secrets.CDG_EMOTE_ID)
                        + ">\t"
                        + Aligator[0][0]
                    )
            if Aligator[1] != [""]:
                if UserToID(Aligator[1][0], dico) != False:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Aligator[1][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t"
                        + Aligator[1][0]
                    )
            if Aligator[2] != [""]:
                if UserToID(Aligator[2][0], dico) != False:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t<@"
                        + UserToID(Aligator[2][0], dico)
                        + ">"
                    )
                else:
                    msg += (
                        "\n\t<:DIS:"
                        + str(secrets.DIS_EMOTE_ID)
                        + ">\t"
                        + Aligator[2][0]
                    )
        # print("Aligator OK")

    msg = msg + "\n**" + str(len(inscrit) - inscrit.count([""])) + " Joueurs**"

    for i in range(len(inscrit)):
        affecter = True  # le personnelle est considéré comme affecté
        if (
            Sanglier.count(inscrit[i]) == 0
            and Grizzli.count(inscrit[i]) == 0
            and Albatros.count(inscrit[i]) == 0
            and Harfang.count(inscrit[i]) == 0
            and Crocodile.count(inscrit[i]) == 0
            and Aligator.count(inscrit[i]) == 0
        ):  # si dans aucun groupe
            affecter = False  # considéré comme non affecté

        if inscrit[i] != [""] and affecter == False:
            if role [i][0] == "CDS":
                msg += "\n\t<:cds:" + str(secrets.CDS_EMOTE_ID) + "> "
                if UserToID(zeus[0][0], dico) != False:
                    msg += "<@" + UserToID(inscrit[i][0], dico) + ">"
                else:
                    msg += inscrit[i][0]

                if len(commentaire) > i:
                    if commentaire[i][0] != "":
                        msg += " (" + commentaire[i][0] + ")"
            elif role[i][0] == "CDG":
                msg += "\n\t<:cdg:" + str(secrets.CDG_EMOTE_ID) + "> "
                if UserToID(zeus[0][0], dico) != False:
                    msg += "<@" + UserToID(inscrit[i][0], dico) + ">"
                else:
                    msg += inscrit[i][0]

                if len(commentaire) > i:
                    if commentaire[i][0] != "":
                        msg += " (" + commentaire[i][0] + ")"
            elif role[i][0] == "CDE":
                msg += "\n\t<:cde:" + str(secrets.CDE_EMOTE_ID) + "> "
                if UserToID(zeus[0][0], dico) != False:
                    msg += "<@" + UserToID(inscrit[i][0], dico) + ">"
                else:
                    msg += inscrit[i][0]

                if len(commentaire) > i:
                    if commentaire[i][0] != "":
                        msg += " (" + commentaire[i][0] + ")"
            elif role[i][0] == "Médecin":
                msg += "\n\t<:medecin:" + str(secrets.MED_EMOTE_ID) + "> "
                if UserToID(zeus[0][0], dico) != False:
                    msg += "<@" + UserToID(inscrit[i][0], dico) + ">"
                else:
                    msg += inscrit[i][0]

                if len(commentaire) > i:
                    if commentaire[i][0] != "":
                        msg += " (" + commentaire[i][0] + ")"
            elif role[i][0] == "Minimi":
                msg += "\n\t<:mg:" + str(secrets.MINI_EMOTE_ID) + "> "
                if UserToID(zeus[0][0], dico) != False:
                    msg += "<@" + UserToID(inscrit[i][0], dico) + ">"
                else:
                    msg += inscrit[i][0]

                if len(commentaire) > i:
                    if commentaire[i][0] != "":
                        msg += " (" + commentaire[i][0] + ")"
            elif role[i][0] == "GV":
                msg += "\n\t<:DIS:" + str(secrets.DIS_EMOTE_ID) + "> "
                if UserToID(zeus[0][0], dico) != False:
                    msg += "<@" + UserToID(inscrit[i][0], dico) + ">"
                else:
                    msg += inscrit[i][0]

                if len(commentaire) > i:
                    if commentaire[i][0] != "":
                        msg += " (" + commentaire[i][0] + ")"
            else:
                msg += "\n\t<:DIS:" + str(secrets.DIS_EMOTE_ID) + "> "
                if UserToID(zeus[0][0], dico) != False:
                    msg += "<@" + UserToID(inscrit[i][0], dico) + ">"
                else:
                    msg += inscrit[i][0]

                msg += " (" + role[i][0]
                if len(commentaire) > i:
                    if commentaire[i][0] != "":
                        msg += ", " + commentaire[i][0]
                msg += ")"

    return msg
