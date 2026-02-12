import discord
from discord.ext import commands
import os
import random

# TOKEN a környezeti változóból (Railway-en így futtatjuk)
TOKEN = os.environ["TOKEN"]

# Intents beállítása
intents = discord.Intents.default()
intents.message_content = True

# Bot létrehozása
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== DM AUTO VÁLASZOK =====
DM_AUTO_RESPONSES = [
    "Ezért hagyott el apád...",
    "Te most kajak nekem ugrálsz?",
    "Jólvan meleg hajlamú.",
    "JÓÓ, Ne itt ugassál!",
    "Mondtam valamit te 2fogú!",
    "Mi nem volt érthető?",
    "Te most komolyan próbálkozol?",
    "Ez volt a legjobb érved?",
    "Próbáld újra, most koncentrálj."
    "Ha az ész wifi lenne, nálad repülő mód van.", 
    "Mondanám, hogy igazad van, de akkor ketten tévednénk.", 
    "Ez most válasz volt, vagy csak hangos gondolkodás?", 
    "Ha ez poén volt, szólj, mikor kell nevetni.",
    "Ha a faszság fájna, te már ordítva fetrengenél.", 
    "Ha ez volt a nagy visszaszólásod, akkor kár volt megszólalni.", 
    "Te nem visszaszólsz, te csak bizonyítod, hogy az evolúció néha félbehagy projekteket.", 
    "Nem az a baj, hogy hülye vagy, hanem hogy magabiztosan csinálod. Kurva veszélyes kombó.",
    "Esküszöm, veled vitatkozni olyan, mintha egy falnak magyaráznék, csak a fal legalább nem okoskodik vissza.", 
]

# ===== READY EVENT =====
@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")
    try:
        await bot.tree.sync()
        print("Slash parancsok szinkronizálva")
    except Exception as e:
        print("Sync error:", e)

# ===== SAY PARANCS =====
@bot.tree.command(name="say", description="Bot kiír szöveget a csatornába")
async def say(interaction: discord.Interaction, text: str):
    await interaction.response.send_message("✅ Küldve!", ephemeral=True)
    await interaction.channel.send(text)

# ===== DM PARANCS =====
@bot.tree.command(name="dm", description="Bot DM-et küld egy felhasználónak")
async def dm(interaction: discord.Interaction, user: discord.User, text: str):
    try:
        await user.send(text)
        await interaction.response.send_message("✅ DM elküldve", ephemeral=True)
    except:
        await interaction.response.send_message("❌ Nem tudtam DM-et küldeni", ephemeral=True)

# ===== DM AUTOMATIKUS VÁLASZ =====
@bot.event
async def on_message(message):
    if message.author.bot:
        return  # bot ne válaszoljon saját magának

    if isinstance(message.channel, discord.DMChannel):
        reply = random.choice(DM_AUTO_RESPONSES)
        await message.channel.send(reply)

    await bot.process_commands(message)

# ===== BOT FUTTATÁS =====
bot.run(TOKEN)
