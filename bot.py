import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ----- Ready event -----
@bot.event
async def on_ready():
    print(f"Bot fut: {bot.user} | Csatlakozva {len(bot.guilds)} szerverhez.")
    try:
        synced = await bot.tree.sync()
        print(f"Slash parancsok szinkronizálva: {len(synced)}")
    except Exception as e:
        print(f"Hiba a szinkronizálásnál: {e}")

# ----- /say parancs -----
@bot.tree.command(name="say", description="A bot mond valamit a chatre")
@discord.app_commands.describe(text="A szöveg, amit a bot írjon ki")
async def say(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(text)

# ----- Bot futtatása -----
bot.run(os.getenv("TOKEN"))
