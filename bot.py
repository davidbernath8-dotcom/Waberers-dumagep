import discord
from discord.ext import commands
import os

TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)


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


# ===== DM =====
@bot.tree.command(name="dm", description="Bot DM-et küld")
async def dm(interaction: discord.Interaction, user: discord.User, text: str):
    try:
        await user.send(text)
        await interaction.response.send_message("✅ DM elkuldve", ephemeral=True)
    except:
        await interaction.response.send_message("❌ Nem tud DM-et küldeni", ephemeral=True)


bot.run(TOKEN)
