import discord
from discord.ext import commands
from discord import app_commands
import os
import datetime

# --- Intents ---
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Szerver és rang ---
GUILD_ID = 1463251661421285388  # a te szervered ID-ja
STAFF_ROLE_NAME = "Staff"

# --- Staff check ---
def is_staff(interaction: discord.Interaction):
    return any(role.name == STAFF_ROLE_NAME for role in interaction.user.roles)

# --- AFK tároló ---
afk_users = {}  # {user_id: reason}

# --- On ready ---
@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=guild)
    print(f"Bot ONLINE: {bot.user}")
    print("Slash parancsok szinkronizálva a szerverre!")

# --- Kick ---
@bot.tree.command(name="kick", description="Kickeld a felhasználót")
@app_commands.describe(user="Kirúgandó user", reason="Indok")
async def kick(interaction: discord.Interaction, user: discord.Member, reason: str = "Nincs megadva"):
    if not is_staff(interaction):
        return await interaction.response.send_message("❌ Nincs jogosultságod.", ephemeral=True)
    await user.kick(reason=reason)
    await interaction.response.send_message(f"👢 {user.mention} kickelve.\n**Ok:** {reason}")

# --- Ban ---
@bot.tree.command(name="ban", description="Bannold a felhasználót")
@app_commands.describe(user="Kitiltható user", reason="Indok")
async def ban(interaction: discord.Interaction, user: discord.Member, reason: str = "Nincs megadva"):
    if not is_staff(interaction):
        return await interaction.response.send_message("❌ Nincs jogosultságod.", ephemeral=True)
    await user.ban(reason=reason)
    await interaction.response.send_message(f"🔨 {user.mention} bannolva.\n**Ok:** {reason}")

# --- Timeout ---
@bot.tree.command(name="timeout", description="Timeout felhasználó")
@app_commands.describe(user="User", minutes="Perc", reason="Indok")
async def timeout(interaction: discord.Interaction, user: discord.Member, minutes: int, reason: str = "Nincs megadva"):
    if not is_staff(interaction):
        return await interaction.response.send_message("❌ Nincs jogosultságod.", ephemeral=True)
    duration = datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)
    await user.timeout(duration, reason=reason)
    await interaction.response.send_message(f"⏳ {user.mention} timeoutolva {minutes} percre.\n**Ok:** {reason}")

# --- Untimeout ---
@bot.tree.command(name="untimeout", description="Timeout levétele")
@app_commands.describe(user="User")
async def untimeout(interaction: discord.Interaction, user: discord.Member):
    if not is_staff(interaction):
        return await interaction.response.send_message("❌ Nincs jogosultságod.", ephemeral=True)
    await user.timeout(None)
    await interaction.response.send_message(f"✅ {user.mention} timeout feloldva.")

# --- AFK ---
@bot.tree.command(name="afk", description="AFK mód bekapcsolása")
@app_commands.describe(reason="Indok, miért AFK vagy")
async def afk(interaction: discord.Interaction, reason: str = "Nincs megadva"):
    afk_users[interaction.user.id] = reason
    await interaction.response.send_message(f"✅ {interaction.user.mention} AFK mód bekapcsolva.\n**Ok:** {reason}", ephemeral=True)

# --- AFK figyelés ---
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    # Ha valaki AFK-ban ír, üzenetben figyelmeztetjük
    if message.author.id in afk_users:
        del afk_users[message.author.id]  # AFK státusz automatikusan törlődik
        await message.channel.send(f"✅ {message.author.mention}, visszatértél AFK-ból.")
    # Ha valaki AFK user-t pingel
    for user_id, reason in afk_users.items():
        if message.guild.get_member(user_id) in message.mentions:
            await message.channel.send(f"ℹ️ {message.author.mention}, {message.guild.get_member(user_id).mention} AFK: {reason}")

    await bot.process_commands(message)

# --- Bot indítása ---
bot.run(os.getenv("TOKEN"))
