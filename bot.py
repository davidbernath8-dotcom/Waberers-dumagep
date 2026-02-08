import discord
from discord.ext import commands
import os
import random

# TOKEN környezeti változóból
TOKEN = os.environ["TOKEN"]

# Intents beállítás
intents = discord.Intents.default()
intents.message_content = True  # kell, hogy DM-eket is olvasson

# Bot létrehozása
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== IDE ÍROD MAJD A VÁLASZOKAT =====
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
]

# ===== READY =====
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
    await interaction.response.send_message("✅ Elkuldve", ephemeral=True)  # csak a parancs használó látja
    await interaction.channel.send(text)

# ===== DM PARANCS =====
@bot.tree.command(name="dm", description="Bot DM-et küld egy felhasználónak")
async def dm(interaction: discord.Interaction, user: discord.User, text: str):
    try:
        await user.send(text)
        await interaction.response.send_message("✅ DM elkuldve", ephemeral=True)
    except:
        await interaction.response.send_message("❌ Nem tud DM-et küldeni", ephemeral=True)

# ===== DM AUTO REPLY =====
@bot.event
async def on_message(message):
    if message.author.bot:
        return  # bot ne válaszoljon magának

    if isinstance(message.channel, discord.DMChannel):
        reply = random.choice(DM_AUTO_RESPONSES)
        await message.channel.send(reply)

    await bot.process_commands(message)

# ===== BOT RUN =====
bot.run(TOKEN)
