import pygsheets
from os import getenv

from dotenv import load_dotenv

load_dotenv()
service_file = getenv("GOOGLE_API_KEY_FILE")
if not service_file:
    raise EnvironmentError("GOOGLE_API_KEY_FILE not set")

# autorisation
gc = pygsheets.authorize(service_file=service_file)

# ouverture du google sheet
sh = gc.open("Planning")
