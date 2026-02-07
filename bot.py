import discord
from discord.ext import commands
import os

TOKEN = os.environ["TOKEN"]   # Railway env variable

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bejelentkezve mint: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Szinkronizált slash parancsok: {len(synced)}")
    except Exception as e:
        print(e)

@bot.tree.command(name="say", description="A bot kiír egy szöveget")
async def say(interaction: discord.Interaction, szoveg: str):
    await interaction.response.send_message(szoveg)

bot.run(TOKEN)
