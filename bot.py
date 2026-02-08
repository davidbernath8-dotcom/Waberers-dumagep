import discord from discord.ext import commands import os import random

================= CONFIG =================

TOKEN = os.getenv("TOKEN")  # Railway / hosting env TOKEN

DM_AUTO_RESPONSES = [ "Ezért hagyott el apád...", "Te most kajak nekem ugrálsz?", "Jólvan meleg hajlamú.", "JÓÓ, Ne itt ugassál!", "Mondtam valamit te 2fogú!", "Mi nem volt érthető?", "Te most komolyan próbálkozol?", "Ez volt a legjobb érved?", "Próbáld újra, most koncentrálj." ]

================= INTENTS =================

intents = discord.Intents.default() intents.message_content = True intents.dm_messages = True

================= BOT =================

bot = commands.Bot(command_prefix="!", intents=intents)

================= READY =================

@bot.event async def on_ready(): print(f"Bot online: {bot.user}") try: synced = await bot.tree.sync() print(f"Slash parancsok szinkronizálva: {len(synced)} db") except Exception as e: print("Slash sync hiba:", e)

================= SLASH SAY =================

@bot.tree.command(name="say", description="Bot kiír egy szöveget a csatornába") async def say(interaction: discord.Interaction, text: str): await interaction.response.send_message("✅ Elkuldve", ephemeral=True) await interaction.channel.send(text)

================= SLASH DM =================

@bot.tree.command(name="dm", description="Bot DM-et küld egy usernek") async def dm(interaction: discord.Interaction, user: discord.User, text: str): try: await user.send(text) await interaction.response.send_message("✅ DM elkuldve", ephemeral=True) except Exception as e: await interaction.response.send_message("❌ Nem tud DM-et küldeni", ephemeral=True) print("DM hiba:", e)

================= DM AUTO REPLY =================

@bot.event async def on_message(message: discord.Message): if message.author.bot: return

# Ha DM-ben írnak a botnak
if isinstance(message.channel, discord.DMChannel):
    reply = random.choice(DM_AUTO_RESPONSES)
    try:
        await message.channel.send(reply)
    except Exception as e:
        print("DM válasz hiba:", e)

await bot.process_commands(message)

================= RUN =================

if not TOKEN: raise ValueError("TOKEN környezeti változó nincs beállítva!")

bot.run(TOKEN)
