import discord
from discord.ext import commands
from discord import app_commands
import os

# ===== INTENTS =====
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# ===== BOT =====
bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ===== READY =====
@bot.event
async def on_ready():
    print(f"Online: {bot.user}")

    try:
        await bot.tree.sync()
        print("Slash commands synced")
    except Exception as e:
        print("Sync error:", e)

# ===== SAY =====
@bot.tree.command(name="say", description="Bot üzenetet küld")
@app_commands.describe(
    text="Szöveg amit kiír a bot",
    reply_message_id="Reply message ID (opcionális)"
)
async def say(interaction: discord.Interaction, text: str, reply_message_id: str = None):

    try:
        await interaction.response.defer(ephemeral=True)

        if reply_message_id:
            try:
                msg = await interaction.channel.fetch_message(int(reply_message_id))
                await msg.reply(text, mention_author=False)
            except:
                await interaction.channel.send(text)
        else:
            await interaction.channel.send(text)

        await interaction.followup.send("✅ Kész", ephemeral=True)

    except Exception as e:
        try:
            await interaction.followup.send(f"Hiba: {e}", ephemeral=True)
        except:
            pass

# ===== DM =====
@bot.tree.command(name="dm", description="Bot DM-et küld valakinek")
@app_commands.describe(
    user="Kinek menjen a DM",
    message="Üzenet szövege"
)
async def dm(interaction: discord.Interaction, user: discord.User, message: str):

    try:
        await interaction.response.defer(ephemeral=True)

        try:
            await user.send(message)
            await interaction.followup.send(f"✅ DM elküldve neki: {user}", ephemeral=True)
        except:
            await interaction.followup.send("❌ Nem tudtam DM-et küldeni (lehet tiltva van).", ephemeral=True)

    except Exception as e:
        try:
            await interaction.followup.send(f"Hiba: {e}", ephemeral=True)
        except:
            pass

# ===== RUN =====
bot.run(os.getenv("TOKEN"))
