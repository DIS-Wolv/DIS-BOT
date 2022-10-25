from datetime import datetime
from bot.discord import bot
from bot.secrets import BOT_TOKEN

print("=" * 40)
print("Démarrage du bot le :", datetime.now().strftime("%d/%m/%Y à %H:%M"))

# afiche le démarage du bot
print("Démarrage du bot")

bot.run(BOT_TOKEN)  # démarre le bot
