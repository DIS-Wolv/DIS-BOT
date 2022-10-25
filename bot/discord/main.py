import discord
from discord.ext import tasks
from discord.ext import commands
from datetime import datetime
import time
import random

# ressource
from bot import secrets
from bot import inscription
from bot import utils
from bot.utils import log
from bot.sources import new_member_msg

# définition du bot
intents = discord.Intents.all()
intents.members = True
bot = discord.Client(intents=intents)

# création d'une variable de type message
message = discord.abc.Messageable
# création d'une variable de type membre
member = discord.member
# liste emoji
emote = [
    secrets.DIS_EMOTE_ID,
    secrets.CDG_EMOTE_ID,
    secrets.CDE_EMOTE_ID,
    secrets.MED_EMOTE_ID,
    secrets.MINI_EMOTE_ID,
]

global loopS
loopS = -1


# event quand le bot est lancé
@bot.event
async def on_ready():
    print("le bot est connecté")  # affiche dans la console que le bot est démarré
    # inscription.orga(3)
    await RandomActivity()
    # activity = discord.Game(name="Attendre")
    # await bot.change_presence(activity=activity)
    await startloop(datetime.now().minute + 1)

    # print('q')


# démarre les évenement répétitif a
async def startloop(m=45):
    global loopS
    logchannel = bot.get_channel(secrets.LOG_CHANNEL_ID)
    if loopS < 0:
        # time.sleep(((m - datetime.now().minute) * 60 - datetime.now().second))
        loop.start()  # démarre la boucle des événements répétitifs
        reponse = ":white_check_mark: Redémarage des évènements répétitifs a : " + str(
            datetime.now().minute
        )
    else:
        reponse = ":x: Les évènements répétitifs sont déjà lancé et executé a HH:"
        if loopS < 10:
            reponse = reponse + "0" + str(loopS)
        else:
            reponse = reponse + str(loopS)
    await logchannel.send(reponse)  # envoie un message


# event quand un nouveau joueur
@bot.event
async def on_member_join(member):
    # vérification du pseudo a venir
    print("new member: ", member)  # affiche un message dans la console

    await SetActivity("Acceuillir " + str(member.display_name))

    logchannel = bot.get_channel(secrets.LOG_CHANNEL_ID)
    await member.send(
        new_member_msg()
    )  # mp le nouveaux avec le message dans new_member_msg.txt

    msg = "Message d'acceuil envoyé à \"" + str(member.display_name) + '"'
    await logchannel.send(msg)

    # Editing role
    server_id = secrets.SERVER_ID  # id du serveur
    role_id = secrets.FNG_ROLE_ID  # id du role FNG
    server = bot.get_guild(server_id)  # recupère le serveur
    role = discord.utils.get(
        server.roles, id=role_id
    )  # defini l'objet role avec les bon attribue
    await member.add_roles(role)  # assigne au nouveaux le role


@bot.event
async def on_member_remove(member):
    print(member, "a leave")

    logchannel = bot.get_channel(secrets.LOG_CHANNEL_ID)
    msg = '"' + str(member.display_name) + '" à deserté'
    await logchannel.send(msg)
    # print(member.id)
    inscription.remUser(member.id)


# event quand messsage
@bot.event
async def on_message(message):
    # print(message.channel.type)
    if str(message.channel.type) == "text":
        # print(type(message.channel.type), message.channel.type, "== 'text'")
        print(
            message.channel.name,
            ">",
            message.author.display_name,
            ":",
            str(message.content),
        )  # affiche le message dans la console content
    else:
        # print(type(message.channel.type),message.channel.type, "!= 'text'")
        print(
            "DM >", message.author.display_name, ":", message.content
        )  # affiche le message dans la console
    if message.channel.id == secrets.CHANNEL_ID:
        # print(message.channel.id, secrets.CHANNEL_ID)
        if utils.mention(message.content) == 1:  # si le message contient la mention
            jour = utils.jour(
                message.content
            )  # regarde si il y a un jour dans le message
            # print("Ajout des reaction sur le message de ", jour)
            if jour != 0:  # si oui
                # print("REACTION!!!!!!!")
                await message.add_reaction(
                    "<:cdg:" + str(secrets.CDG_EMOTE_ID) + ">"
                )  # ajoute les réactions d'inscriptions
                await message.add_reaction(
                    "<:cde:" + str(secrets.CDE_EMOTE_ID) + ">"
                )  # ajoute les réactions d'inscriptions
                await message.add_reaction(
                    "<:medecin:" + str(secrets.MED_EMOTE_ID) + ">"
                )  # ajoute les réactions d'inscriptions
                await message.add_reaction(
                    "<:mg:" + str(secrets.MINI_EMOTE_ID) + ">"
                )  # ajoute les réactions d'inscriptions
                await message.add_reaction(
                    "<:DIS:" + str(secrets.DIS_EMOTE_ID) + ">"
                )  # ajoute les réactions d'inscriptions
                await message.add_reaction(
                    str("❌")
                )  # ajoute les réactions d'inscriptions

    elif message.channel.id == secrets.LOG_CHANNEL_ID and message.author.id != int(
        secrets.CLIENT_ID
    ):  # COMMANDE
        # dans le channel de log pas par le bot
        test = utils.mots(message.content, "update")
        if test != -1:  # si le message comptient "update"
            log = bot.get_channel(secrets.LOG_CHANNEL_ID)  # recupère le cannal de log
            await log.send(
                "Début de la mise à jour des messages"
            )  # envoie un message dans les logs

            await appelMessage()  # appel la fonction de creation de message

        test = utils.mots(
            message.content, "planning"
        )  # si le message comptient "planning"
        if test != -1:
            reponse = ""
            await message.channel.send(
                "Vérification du planning ..."
            )  # envoie un message
            # crée une liste correcte et une liste de récupération des valeurs
            jour = [
                "Lundi",
                "Mardi",
                "Mercredi",
                "Jeudi",
                "Vendredi",
                "Samedi",
                "Dimanche",
            ]
            retour = ["", "", "", "", "", "", ""]

            for i in range(1, 8):  # recupère les valeurs
                retour[i - 1] = inscription.jourPage(inscription.jourTransfo(i))

            # affiche un retour
            # print(retour, jour)
            val = True
            reponse = ":grey_question:\t\tNom du jour \tNom sur la page\n"
            for i in range(7):
                if jour[i] == retour[i]:
                    reponse = reponse + ":white_check_mark:" + "\t\t"
                else:
                    reponse = reponse + ":x:" + "\t\t"
                    val = False
                reponse = reponse + jour[i] + "\t\t\t" + retour[i] + "\n"

            if val:
                reponse = reponse + "\n:white_check_mark: Planning OK"
            else:
                reponse = reponse + "\n:x: Erreur Planning"

            await message.channel.send(reponse)  # envoie le message

        test = utils.mots(message.content, "clear")
        if test != -1:
            jour = utils.jour(
                message.content
            )  # regarde si il y a un jour dans le message
            if jour != 0:  # si le message contient la mention
                msg = "Nettoyage du jour : " + str(jour)
                await message.channel.send(msg)  # envoie un message
                inscription.clear(jour)
                await message.channel.send("Nettoyage terminé")  # envoie un message

        test = utils.mots(message.content, "addUser")
        if test == 0:
            msg = message.content
            msg = msg.split(" ")
            if len(msg) >= 2:
                reponse = "Ajout en cours"
                await message.channel.send(reponse)  # envoie un message
                inscription.addUser(msg[1], msg[2])

            # print(msg)

            reponse = (
                ':white_check_mark: Ajout de "'
                + msg[1]
                + "\" avec l'id ``"
                + msg[2]
                + "``"
            )
            await message.channel.send(reponse)  # envoie un message

        test = utils.mots(message.content, "loop")
        if test != -1:
            global loopS
            if loopS < 00:
                msg = message.content
                msg = msg.split(" ")
                print(msg)
                if len(msg) > 2:
                    reponse = (
                        ":white_check_mark: Redémarage des évènements répétitifs a : "
                        + msg[1]
                    )
                    await message.channel.send(reponse)  # envoie un message
                    await startloop(msg[1])
                else:
                    reponse = ":white_check_mark: Redémarage des évènements répétitifs"
                    await message.channel.send(reponse)  # envoie un message
                    await startloop()
            else:
                reponse = (
                    ":x: Les évènements répétitifs sont déjà lancé et executé a HH:"
                )
                if loopS < 10:
                    reponse = reponse + "0" + str(loopS)
                else:
                    reponse = reponse + str(loopS)
                await message.channel.send(reponse)  # envoie un message

        test = utils.mots(message.content, "stop")
        if test != -1:
            print(
                "Arret du bot manuel le : ",
                datetime.now().day,
                "/",
                datetime.now().month,
                "/",
                datetime.now().year,
                "à",
                datetime.now().hour,
                "h",
                datetime.now().minute,
                "par",
                message.author.display_name,
            )
            loop.cancel()
            await message.channel.send("Arret du Bot")
            await bot.logout()

        test = utils.mots(message.content, "statut")
        if test == 0:
            reponse = "Changement du statut"
            await message.channel.send(reponse)  # envoie un message
            msg = message.content
            msg = msg.split(" ")
            statut = ""
            print(msg, len(msg))
            for i in range(1, len(msg)):
                statut = statut + msg[i] + " "

            await SetActivity(statut)

            reponse = (
                ":white_check_mark: changement du statut pour ``Joue à " + statut + "``"
            )
            await message.channel.send(reponse)  # envoie un message

        test = utils.mots(message.content, "live")
        if test == 0:
            reponse = "Changement du statut"
            await message.channel.send(reponse)  # envoie un message
            msg = message.content
            msg = msg.split(" ")

            statut = ""
            print(msg, len(msg))
            for i in range(2, len(msg)):
                statut = statut + msg[i] + " "

            activity = discord.Streaming(name=statut, url=msg[1])
            await bot.change_presence(activity=activity)

            reponse = (
                ":white_check_mark: changement du statut pour ``Stream " + statut + "``"
            )
            await message.channel.send(reponse)  # envoie un message

        test = utils.mots(message.content, "acceuil")
        if test == 0:
            msgcont = message.content.split(" ")
            if len(msgcont) == 2:
                serv = bot.get_guild(secrets.SERVER_ID)
                member = serv.get_member(int(msgcont[1]))
                # print(member.display_name)
                # await member.send(new_member_msg())
                await on_member_join(member)

        test = utils.mots(
            message.content, "randomstatus"
        )  # si le message comptient "RandomStatus"
        if test != -1:
            statut = await RandomActivity()
            reponse = (
                ":white_check_mark: changement du statut pour ``Joue à " + statut + "``"
            )
            await message.channel.send(reponse)  # envoie un message

    test0 = utils.mots(message.content, "sondage")
    test1 = utils.mots(message.content, "réaction")
    test2 = utils.mots(message.content, "dlc")
    # print(test0, test1, test2)
    if test0 != -1 and test1 != -1 and test2 != -1:
        # print("Ajout des reactionsDLC")
        await message.add_reaction(
            "<:karts:" + str(secrets.KART_DLC_EMOTE_ID) + ">"
        )  # ajoute les réactions d'inscriptions
        await message.add_reaction(
            "<:heli:" + str(secrets.HELI_DLC_EMOTE_ID) + ">"
        )  # ajoute les réactions d'inscriptions
        await message.add_reaction(
            "<:marksmen:" + str(secrets.MARK_DLC_EMOTE_ID) + ">"
        )  # ajoute les réactions d'inscriptions
        await message.add_reaction(
            "<:apex:" + str(secrets.APEX_DLC_EMOTE_ID) + ">"
        )  # ajoute les réactions d'inscriptions
        await message.add_reaction(
            "<:jets:" + str(secrets.JETS_DLC_EMOTE_ID) + ">"
        )  # ajoute les réactions d'inscriptions
        await message.add_reaction(
            "<:tanks:" + str(secrets.TANKS_DLC_EMOTE_ID) + ">"
        )  # ajoute les réactions d'inscriptions
        await message.add_reaction(
            "<:lawOfWar:" + str(secrets.LOW_DLC_EMOTE_ID) + ">"
        )  # ajoute les réactions d'inscriptions
        await message.add_reaction(
            "<:globalMobilization:" + str(secrets.GBMOB_DLC_EMOTE_ID) + ">"
        )  # ajoute les réactions d'inscriptions
        await message.add_reaction(
            "<:contact:" + str(secrets.CONTACT_DLC_EMOTE_ID) + ">"
        )  # ajoute les réactions d'inscriptions
        await message.add_reaction(
            "<:PrairieFire:" + str(secrets.PRAIRIEFIRE_DLC_EMOTE_ID) + ">"
        )  # ajoute les réactions d'inscriptions
        await message.add_reaction(
            "<:WesternSahara:" + str(secrets.WESTERNSAHARA_DLC_EMOTE_ID) + ">"
        )


# quand une réaction est ajoutée
@bot.event
async def on_raw_reaction_add(payload):
    log("on_raw_reaction_add")
    guild = bot.get_guild(
        payload.guild_id
    )  # recupère le pool d'utilisateurs qui on réagi
    user = await guild.fetch_member(
        payload.user_id
    )  # recupère l'utilisateur qui a réagi

    channel = await bot.fetch_channel(payload.channel_id)  # recupère le channel
    message = await channel.fetch_message(
        payload.message_id
    )  # récupère le message en question
    # print(payload.emoji)

    if (
        payload.channel_id == secrets.CHANNEL_ID and str(user.id) != secrets.CLIENT_ID
    ):  # si la réaction est dans le channel souhaité
        # print(payload.emoji.id)
        jour = utils.jour(message.content)  # recupère le jour du message
        # print(user.display_name, "a réagit : ", payload.emoji)
        if (
            payload.emoji.id in emote and jour != 0
        ):  # si l'emote est une des emotes souhaitées et qu'il y a un jour sur le message
            # print(payload.emoji.id)
            log("  appelInscription")
            await appelInscription(
                user, payload.emoji.id, jour
            )  # appel la fonction pour incrire l'utilisateur
            log("  end appelInscription")

        if str(payload.emoji) == str("❌") and jour != 0:
            print("desinscription")
            statut = inscription.remove(user.id, jour)  # éssaye désinscrire la personne

            if statut == 0:
                err = ""
            elif statut == 1:  # "Vous avez été désinscrit avec succès"
                err = ""
            elif statut == 2:
                err = (
                    user.display_name
                    + " (Id = `"
                    + str(user.id)
                    + "`) n'a pas pu etre désinscrit"
                )
            elif statut == -1:
                err = ""
            else:
                err = (
                    "ERREUR Inscription : "
                    + user.display_name
                    + " id `"
                    + str(user.id)
                    + "`"
                )

            if (
                str(user.id) != secrets.CLIENT_ID and err != ""
            ):  # si l'utilisateur n'est pas le bot
                # await user.send(msg)  # mp la personne avec le message
                logchannel = bot.get_channel(secrets.LOG_CHANNEL_ID)
                await logchannel.send(err)

        await updateMessage(message)  # met a jour la liste des inscrits

    test0 = utils.mots(message.content, "SONDAGE")
    test1 = utils.mots(message.content, "RÉACTION")
    test2 = utils.mots(message.content, "DLC")
    if (
        test0 != -1
        and test1 != -1
        and test2 != -1
        and str(user.id) != secrets.CLIENT_ID
    ):
        await appelDLC(user, payload.emoji.id, 1)
    log("end on_raw_reaction_add")


# Inscrit le joueur en fonction de ca reaction
#   User = ID du joueur
#   emote = ID de l'emote
#   jour = numéro du jour
async def appelInscription(user, emote, jour):
    if str(user.id) == secrets.CLIENT_ID:
        # c le bot :(
        return

    logchannel = bot.get_channel(secrets.LOG_CHANNEL_ID)

    if emote == secrets.DIS_EMOTE_ID:
        statut = inscription.add(user.id, jour, ["GV"])  # essaye d'inscrire la personne
    elif emote == secrets.CDG_EMOTE_ID:
        statut = inscription.add(
            user.id, jour, ["CDG"]
        )  # essaye d'inscrire la personne
    elif emote == secrets.CDE_EMOTE_ID:
        statut = inscription.add(
            user.id, jour, ["CDE"]
        )  # essaye d'inscrire la personne
    elif emote == secrets.MED_EMOTE_ID:
        statut = inscription.add(
            user.id, jour, ["Médecin"]
        )  # essaye d'inscrire la personne
    elif emote == secrets.MINI_EMOTE_ID:
        statut = inscription.add(
            user.id, jour, ["Minimi"]
        )  # essaye d'inscrire la personne
    else:
        statut = inscription.add(user.id, jour)  # essaye d'inscrire la personne

    log(f"    statut {statut}")
    if statut == 0:
        # deja inscrit
        return
    elif statut == 1:
        # succes
        return
    elif statut == 2:  # Utilisateur pas dans la liste
        err = (
            user.display_name
            + " (Id = `"
            + str(user.id)
            + "`) n'a pas pu être inscrit."
        )
        print("Ajout de l'utilisateur : ", user.display_name)
        inscription.addUser(user.display_name, str(user.id))
        print("utilisateur ajouté")
        err += (
            '\n:white_check_mark: Ajout de "'
            + user.display_name
            + "\" avec l'id ``"
            + str(user.id)
            + "``"
        )
    else:
        err = "ERREUR Inscription :" + user.display_name + " id `" + str(user.id) + "`"
        return

    print(err)
    # reinscrit
    await logchannel.send(err)
    await appelInscription(user, emote, jour)


# Ajoute le DLC au joueur en fonction de ca reaction
#   User = ID du joueur
#   emote = ID de l'emote
async def appelDLC(user, emote, state):
    logchannel = bot.get_channel(secrets.LOG_CHANNEL_ID)

    if emote == secrets.KART_DLC_EMOTE_ID:
        statut = inscription.stateDLC(user.id, 0, state)
    elif emote == secrets.HELI_DLC_EMOTE_ID:
        statut = inscription.stateDLC(user.id, 1, state)
    elif emote == secrets.MARK_DLC_EMOTE_ID:
        statut = inscription.stateDLC(user.id, 2, state)
    elif emote == secrets.APEX_DLC_EMOTE_ID:
        statut = inscription.stateDLC(user.id, 3, state)
    elif emote == secrets.JETS_DLC_EMOTE_ID:
        statut = inscription.stateDLC(user.id, 4, state)
    elif emote == secrets.TANKS_DLC_EMOTE_ID:
        statut = inscription.stateDLC(user.id, 5, state)
    elif emote == secrets.LOW_DLC_EMOTE_ID:
        statut = inscription.stateDLC(user.id, 6, state)
    elif emote == secrets.GBMOB_DLC_EMOTE_ID:
        statut = inscription.stateDLC(user.id, 7, state)
    elif emote == secrets.CONTACT_DLC_EMOTE_ID:
        statut = inscription.stateDLC(user.id, 8, state)
    elif emote == secrets.PRAIRIEFIRE_DLC_EMOTE_ID:
        statut = inscription.stateDLC(user.id, 9, state)
    elif emote == secrets.WESTERNSAHARA_DLC_EMOTE_ID:
        statut = inscription.stateDLC(user.id, 10, state)

    if statut == 1:  # succes
        err = ""
        await SetActivity("Compter les DLCs de " + user.display_name)
    elif statut == 2:  # Utilisateur pas dans la liste
        err = (
            user.display_name
            + " (Id = `"
            + str(user.id)
            + "`) n'es pas dans la fiche Technique."
        )
        inscription.addUser(user.display_name, str(user.id))
        err += (
            '\n:white_check_mark: Ajout de "'
            + user.display_name
            + "\" avec l'id ``"
            + str(user.id)
            + "``"
        )
    else:
        err = "ERREUR Reaction DLC :" + user.display_name + " id `" + str(user.id) + "`"

    if (
        str(user.id) != secrets.CLIENT_ID and err != ""
    ):  # si l'utilisateur n'est pas le bot
        await logchannel.send(err)
        await appelDLC(user, emote, state)


# quand une réaction est enlevée
@bot.event
async def on_raw_reaction_remove(payload):
    log("on_raw_reaction_remove")

    guild = bot.get_guild(
        payload.guild_id
    )  # recupère le pool d'utilisateurs qui on réagi
    user = await guild.fetch_member(
        payload.user_id
    )  # recupère l'utilisateur qui a modifié sa réaction

    channel = await bot.fetch_channel(payload.channel_id)  # recupère le channel
    message = await channel.fetch_message(
        payload.message_id
    )  # récupère le message en question
    # print(payload.emoji)

    if (
        payload.channel_id == secrets.CHANNEL_ID
    ):  # si la réaction est dans le channel souhaité
        # print(payload.emoji.id)
        # print (payload.emoji.id, type(payload.emoji.id))

        if payload.emoji.id in emote:  # si l'emote est une des emotes souhaitées
            jour = utils.jour(message.content)  # recupère le jour du message
            # print(user.display_name, "a supprimé : ", payload.emoji)
            statut = inscription.remove(user.id, jour)  # éssaye désinscrire la personne

            err = ""
            # assigne a msg une valeur suivant le resultat de l'incription
            if statut == 0:
                msg = ""  # "Vous êtes déjà désinscrit"
            elif statut == 1:
                msg = ""  # "Vous avez été désinscrit avec succès"
            elif statut == 2:
                msg = ""  # "Vous n'avez pas pu être désinscrit contacter @Wolv#2393 ou un Instructeur"
                err = (
                    user.display_name
                    + " (Id = `"
                    + str(user.id)
                    + "`) n'a pas pu etre désinscrit"
                )
            elif statut == -1:
                msg = ""
                err = ""
            else:
                msg = "ERREUR contacter @Wolv#2393 ou un Instructeur"
                err = (
                    "ERREUR Inscription : "
                    + user.display_name
                    + " id `"
                    + str(user.id)
                    + "`"
                )

            if (
                str(user.id) != secrets.CLIENT_ID and err != ""
            ):  # si l'utilisateur n'est pas le bot
                # await user.send(msg)  # mp la personne avec le message
                logchannel = bot.get_channel(secrets.LOG_CHANNEL_ID)
                await logchannel.send(err)

            # sleep(5)
        await updateMessage(message)  # met a jour la liste des inscrits

    test0 = utils.mots(message.content, "SONDAGE")
    test1 = utils.mots(message.content, "RÉACTION")
    test2 = utils.mots(message.content, "DLC")
    if (
        test0 != -1
        and test1 != -1
        and test2 != -1
        and str(user.id) != secrets.CLIENT_ID
    ):
        await appelDLC(user, payload.emoji.id, 0)


# est appellé par l'ajout ou la suppresion de reaction
# met a jour le message
async def updateMessage(msg):
    log("  updateMessage")
    jourNom = [
        "",
        "Lundi",
        "Mardi",
        "Mercredi",
        "Jeudi",
        "Vendredi",
        "Samedi",
        "Dimanche",
    ]
    jour = utils.jour(msg.content)  # récupère le jours du message

    newmsg = inscription.message(jour)  # crée le nouveau message
    # print("Message : ", newmsg)
    if newmsg != 0:
        if newmsg != msg:  # si le nouveau message est different de l'ancien
            await msg.edit(content=newmsg)  # modifie le message
        # print(jour)
        await SetActivity(
            str(inscription.missionName(jour) + " " + jourNom[jour] + " soir")
        )
    log("  end updateMessage")


# toutes les heures, execute :
@tasks.loop(hours=1.0)
async def loop():
    jourNom = [
        "",
        "Lundi",
        "Mardi",
        "Mercredi",
        "Jeudi",
        "Vendredi",
        "Samedi",
        "Dimanche",
    ]
    global loopS
    day = datetime.now().weekday()  # recupère le numéro du jour de la semaine
    if day == 0:
        day = 7

    hour = datetime.now().hour  # recupère l'heure du système

    loopS = datetime.now().minute
    # print(hour)
    # print(day)
    print(datetime.now().strftime("%d/%m/%Y à %H:%M"))

    channel = bot.get_channel(secrets.CHANNEL_ID)

    if hour <= 2:  # si l'heure est inférieure ou égale a 2
        print("Nettoyage de la page", day, "correspondant à", inscription.jourNom[day])
        print(str(inscription.missionName(day)))
        if inscription.missionName(day) != "":
            await SetActivity("nettoyer le planning")

            if inscription.missionName(day) == "ODD de la semaine !":
                inscription.clearJoueur(day)
                # supprime le message du jour précédant
                async for message in channel.history(
                    limit=7
                ):  # pour les 7 derniers messages
                    jourMsg = utils.jour(message.content)  # recupère le jour du message

                    if jourMsg == day:  # si le message est le message du jour précédant
                        await message.delete()  # supprime le message
            else:
                print("Nettoyage du jour : " + str(day))
                inscription.clear(day)  # nettoie la feuille du jour d'avant
                # supprime le message du jour précédant
                async for message in channel.history(
                    limit=7
                ):  # pour les 7 derniers messages
                    jourMsg = utils.jour(message.content)  # recupère le jour du message

                    if jourMsg == day:  # si le message est le message du jour précédant
                        await message.delete()  # supprime le message
        else:
            print("Pas de nettoyage a faire")
    elif 10 <= hour <= 21:  # si l'heure est entre 10h et 21 h
        await appelMessage()
        # print("appelMessage")

    day = day + 1
    if day == 8:
        day = 1

    if inscription.missionName(day) != "":
        await SetActivity(inscription.missionName(day) + " " + jourNom[day] + " soir")
    elif inscription.missionName(day) == "":
        await RandomActivity()


async def RandomActivity():
    nom = secrets.PhraseDAttente[random.randint(0, (len(secrets.PhraseDAttente) - 1))]
    await SetActivity(nom)
    return nom


# set une activité
async def SetActivity(nom):
    activity = discord.Game(name=nom)
    await bot.change_presence(activity=activity)


# Fonction qui crée et envoie les message pour les 5 prochains jour si il y a lieux
async def appelMessage():
    # met a jour les anciens message
    channel = bot.get_channel(secrets.CHANNEL_ID)  # recupère le cannal du bot
    async for msg in channel.history(limit=7):  # pour les 7 dernier message
        # print("\t", msg.author.id, ":", msg.content)
        if str(msg.author.id) == str(
            secrets.CLIENT_ID
        ):  # si il on été envoyer par le bot
            jour = utils.jour(msg.content)  # récupère le jours du message

            newmsg = inscription.message(jour)  # crée le nouveau message
            if newmsg != msg:  # si le nouveau message est different de l'ancien
                await msg.edit(content=newmsg)  # modifie le message

    # fait les nouveaux message
    day = datetime.now().weekday() + 1  # recupère le numéro du jour de la semaine
    # print("Nous somme le jour numéro ", day)
    channel = bot.get_channel(secrets.CHANNEL_ID)  # recupère le channel du bot
    statut = True  # definie qu'il faut changé le statut

    for i in range(-1, 2):  # sur 3 jours
        target = ((day + i) % 7) + 1  # récupère le numéro du jour
        # print(target)
        msg = inscription.message(target)  # recupère le message d'annonce

        if msg != 0:  # si il y a un message a envoyer = missions
            annonce = True  # défini s'il faut faire une annonce dans le channel
            # print("mission : ", target)

            async for message in channel.history(
                limit=7
            ):  # pour les 7 derniers messages
                jourMsg = utils.jour(
                    message.content
                )  # recupère le jour du message s'il y a

                if jourMsg == target:  # si le jour est le jour de l'annonce voulue
                    annonce = False  # défini que l'annonce est déjà faite
                    # print("annonce deja faite")
            # print(target, annonce)

            if annonce:  # si l'annonce est à faire
                # print(msg)
                print("message pour le jour : ", target)
                await channel.send(msg)  # envoie le message de l'annonce

            if statut:  # si le statut a changé
                statut = False  # définie le statut comme changé
                jourNom = [
                    "",
                    "Lundi",
                    "Mardi",
                    "Mercredi",
                    "Jeudi",
                    "Vendredi",
                    "Samedi",
                    "Dimanche",
                ]

                await SetActivity(
                    inscription.missionName(target) + " " + jourNom[target] + " soir"
                )


# si la boucle est fini
@loop.after_loop
async def Erreur():
    print(
        datetime.now().day,
        "/",
        datetime.now().month,
        "/",
        datetime.now().year,
        "à",
        datetime.now().hour,
        "h",
        datetime.now().minute,
    )
    print("/!\\ Erreur de tache")  # envoie un message dans la console
    logchannel = bot.get_channel(secrets.LOG_CHANNEL_ID)
    global loopS
    loopS = -1
    await logchannel.send(":x: Les évènements répétitifs se sont arrété")
