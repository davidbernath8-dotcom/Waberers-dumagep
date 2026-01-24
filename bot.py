import discord
from discord.ext import commands
from discord import app_commands
import os

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

GUILD_ID = 1463251661421285388  # szerver ID
STAFF_ROLE_NAME = "Staff"      # staff rang neve

def is_staff(interaction: discord.Interaction):
    return any(role.name == STAFF_ROLE_NAME for role in interaction.user.roles)

@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=guild)
    print("Mod bot ONLINE")

# --- BAN ---
@bot.tree.command(name="ban", description="Felhasználó kitiltása")
@app_commands.describe(user="Kitiltható user", reason="Indok")
async def ban(interaction: discord.Interaction, user: discord.Member, reason: str = "Nincs megadva"):
    if not is_staff(interaction):
        return await interaction.response.send_message("❌ Nincs jogosultságod.", ephemeral=True)

    await user.ban(reason=reason)
    await interaction.response.send_message(f"🔨 {user.mention} bannolva.\n**Ok:** {reason}")

# --- KICK ---
@bot.tree.command(name="kick", description="Felhasználó kirúgása")
async def kick(interaction: discord.Interaction, user: discord.Member, reason: str = "Nincs megadva"):
    if not is_staff(interaction):
        return await interaction.response.send_message("❌ Nincs jogosultságod.", ephemeral=True)

    await user.kick(reason=reason)
    await interaction.response.send_message(f"👢 {user.mention} kickelve.\n**Ok:** {reason}")

# --- TIMEOUT ---
@bot.tree.command(name="timeout", description="Timeout adása")
@app_commands.describe(minutes="Percben")
async def timeout(interaction: discord.Interaction, user: discord.Member, minutes: int, reason: str = "Nincs megadva"):
    if not is_staff(interaction):
        return await interaction.response.send_message("❌ Nincs jogosultságod.", ephemeral=True)

    duration = discord.utils.utcnow() + discord.timedelta(minutes=minutes)
    await user.timeout(duration, reason=reason)
    await interaction.response.send_message(f"⏳ {user.mention} timeoutolva {minutes} percre.\n**Ok:** {reason}")

# --- UNTIMEOUT ---
@bot.tree.command(name="untimeout", description="Timeout levétele")
async def untimeout(interaction: discord.Interaction, user: discord.Member):
    if not is_staff(interaction):
        return await interaction.response.send_message("❌ Nincs jogosultságod.", ephemeral=True)

    await user.timeout(None)
    await interaction.response.send_message(f"✅ {user.mention} timeout feloldva.")

bot.run(os.getenv("TOKEN"))
discord.py>=2.0.0
