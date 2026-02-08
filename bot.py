import discord
from discord.ext import commands
import os
import random

TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== IDE ÍROD MAJD A VÁLASZOKAT =====
DM_AUTO_RESPONSES = [
    "Ezért hagyott el apád...",
    "Te most kajak nekem ugrálsz? ",
    "Jólvan meleg hajlamú.",
    "JÓÓ,Ne itt ugassál!" ,
    "Mondtam valamit te 2fogú! ",
    "Mi nem volt érthető?",
]

# ===== READY =====
@bot.event
async def on_ready():
    print("Bot online:", bot.user)
    try:
        await bot.tree.sync()
        print("Slash synced")
    except Exception as e:
        print("Sync error:", e)

# ===== SAY =====
@bot.tree.command(name="say", description="Bot kiír szöveget")
async def say(interaction: discord.Interaction, text: str):
    await interaction.response.send_message("✅ Elkuldve", ephemeral=True)
    await interaction.channel.send(text)

# ===== DM COMMAND =====
@bot.tree.command(name="dm", description="Bot DM-et küld")
async def dm(interaction: discord.Interaction, user: discord.User, text: str):
    try:
        await user.send(text)
        await interaction.response.send_message("✅ DM elkuldve", ephemeral=True)
    except:
        await interaction.response.send_message("❌ Nem tud DM-et küldeni", ephemeral=True)

# ===== DM AUTO REPLY =====
@bot.event
async def on_message(message):

    # Bot ne válaszoljon magának
    if message.author.bot:
        return

    # Ha DM-ben írnak a botnak
    if isinstance(message.channel, discord.DMChannel):

        reply = random.choice(DM_AUTO_RESPONSES)
        await message.channel.send(reply)

    await bot.process_commands(message)

# ===== RUN =====
bot.run(TOKEN)
