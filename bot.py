import discord
from discord.ext import commands
from discord import app_commands
import os

# ================= INTENTS =================

intents = discord.Intents.default()
intents.message_content = True

# ================= BOT =================

bot = commands.Bot(command_prefix="!", intents=intents)


# ================= READY + SYNC =================

@bot.event
async def on_ready():
    print(f"✅ Bot online: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Slash parancs sync: {len(synced)} db")
    except Exception as e:
        print("❌ Sync hiba:", e)


# ================= SAY COMMAND =================

@bot.tree.command(name="say", description="Bot üzenetet küld")
@app_commands.describe(
    szoveg="Mit írjon ki a bot",
    reply_message_id="(Opcionális) Üzenet ID amire replyoljon"
)
async def say(
    interaction: discord.Interaction,
    szoveg: str,
    reply_message_id: str | None = None
):

    try:

        # ===== REPLY HA VAN MESSAGE ID =====
        if reply_message_id:

            try:
                msg = await interaction.channel.fetch_message(int(reply_message_id))

                await msg.reply(
                    szoveg,
                    mention_author=False
                )

            except:
                await interaction.channel.send(szoveg)

        # ===== SIMA ÜZENET =====
        else:
            await interaction.channel.send(szoveg)

        # ===== EPHEMERAL RESPONSE =====
        await interaction.response.send_message(
            "✅ Üzenet elküldve",
            ephemeral=True
        )

    except Exception as e:
        await interaction.response.send_message(
            f"❌ Hiba: {e}",
            ephemeral=True
        )


# ================= RUN =================

bot.run(os.environ["TOKEN"])
