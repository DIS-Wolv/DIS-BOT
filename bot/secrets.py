from json import load
from os import getenv

from dotenv import load_dotenv

load_dotenv()
sectets_fname = getenv("SECRETS_FILE")
if not sectets_fname:
    raise EnvironmentError("SECRETS_FILE not set")

with open(sectets_fname) as f:
    secrets_json = load(f)

try:
    CLIENT_ID = secrets_json["CLIENT_ID"]
    CLIENT_SECRET = secrets_json["CLIENT_SECRET"]
    BOT_TOKEN = secrets_json["BOT_TOKEN"]
    CHANNEL_ID = secrets_json["CHANNEL_ID"]
    LOG_CHANNEL_ID = secrets_json["LOG_CHANNEL_ID"]
    SERVER_ID = secrets_json["SERVER_ID"]
    ROLE_ID = secrets_json["ROLE_ID"]
    FNG_ROLE_ID = secrets_json["FNG_ROLE_ID"]
    LINKS = secrets_json["LINKS"]
    DIS_EMOTE_ID = secrets_json["DIS_EMOTE_ID"]
    CDG_EMOTE_ID = secrets_json["CDG_EMOTE_ID"]
    CDE_EMOTE_ID = secrets_json["CDE_EMOTE_ID"]
    MED_EMOTE_ID = secrets_json["MED_EMOTE_ID"]
    GV_EMOTE_ID = secrets_json["GV_EMOTE_ID"]
    MINI_EMOTE_ID = secrets_json["MINI_EMOTE_ID"]
    KART_DLC_EMOTE_ID = secrets_json["KART_DLC_EMOTE_ID"]
    HELI_DLC_EMOTE_ID = secrets_json["HELI_DLC_EMOTE_ID"]
    MARK_DLC_EMOTE_ID = secrets_json["MARK_DLC_EMOTE_ID"]
    APEX_DLC_EMOTE_ID = secrets_json["APEX_DLC_EMOTE_ID"]
    JETS_DLC_EMOTE_ID = secrets_json["JETS_DLC_EMOTE_ID"]
    TANKS_DLC_EMOTE_ID = secrets_json["TANKS_DLC_EMOTE_ID"]
    LOW_DLC_EMOTE_ID = secrets_json["LOW_DLC_EMOTE_ID"]
    GBMOB_DLC_EMOTE_ID = secrets_json["GBMOB_DLC_EMOTE_ID"]
    CONTACT_DLC_EMOTE_ID = secrets_json["CONTACT_DLC_EMOTE_ID"]
    PRAIRIEFIRE_DLC_EMOTE_ID = secrets_json["PRAIRIEFIRE_DLC_EMOTE_ID"]
    WESTERNSAHARA_DLC_EMOTE_ID = secrets_json["WESTERNSAHARA_DLC_EMOTE_ID"]
    PhraseDAttente = secrets_json["PhraseDAttente"]
except KeyError as e:
    raise EnvironmentError(f"Key {e} not found in secrets file")
