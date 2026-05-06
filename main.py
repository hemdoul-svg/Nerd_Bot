# ==============================
# IMPORTS
# ==============================

import discord
from discord import app_commands
import random
import datetime
import json
import os
from dotenv import load_dotenv # ça sert à garder le Token en .env .
load_dotenv ()
token= os.getenv("TOKEN")

# ==============================
# CONFIGURATION DU BOT
# ==============================

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# permet d'utiliser les commandes /
tree = app_commands.CommandTree(client)

# ==============================
# DEMARRAGE DU BOT
# ==============================

@client.event
async def on_ready():
    await tree.sync()
    print(f"Bot connecté en tant que {client.user}")

# ==============================
# COMMANDE /regles
# ==============================

@tree.command(name="regles", description="Affiche les règles du serveur")
async def regles(interaction: discord.Interaction):

    texte = (
        "📜 **RÈGLES DU SERVEUR**\n\n"
        "1. Respecter les autres\n"
        "2. Pas de spam\n"
        "3. Pas d'insultes\n"
        "4. Amuse-toi 🤓"
    )

    await interaction.response.send_message(texte)

# ==============================
# COMMANDE FUN : /coinflip
# ==============================

@tree.command(name="coinflip", description="Pile ou face")
async def coinflip(interaction: discord.Interaction):

    resultat = random.choice(["Pile", "Face"])

    await interaction.response.send_message(f"🪙 Résultat : **{resultat}**")

# ==============================
# COMMANDE FUN : /fact
# ==============================

@tree.command(name="fact", description="Fait geek aléatoire")
async def fact(interaction: discord.Interaction):

    facts = [
        "Le premier bug informatique était un vrai insecte 🐛",
        "Minecraft a été créé par Notch",
        "Le premier disque dur faisait plus de 1 tonne",
        "Le premier site web existe encore",
        "Le langage Python a été créé en 1991"
    ]

    await interaction.response.send_message(random.choice(facts))

# ==============================
# COMMANDE FUN : /iq
# ==============================

@tree.command(name="iq", description="Test IQ aléatoire")
async def iq(interaction: discord.Interaction):

    score = random.randint(70, 160)

    await interaction.response.send_message(f"🧠 Ton IQ : **{score}**")


# ==============================
# COMMANDE /help
# ==============================

@tree.command(name="help", description="Liste des commandes")
async def help(interaction: discord.Interaction):

    message = (
        "**Commandes disponibles :**\n\n"
        "📜 /regles\n"
        "🪙 /coinflip\n"
        "🧠 /iq\n"
        "📚 /fact\n\n"
    )

    await interaction.response.send_message(message)

# ==============================
# LANCEMENT DU BOT
# ==============================


client.run(TOKEN)

