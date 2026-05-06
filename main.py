# ==============================
# IMPORTS
# ==============================

import discord
from discord import app_commands
import random
import datetime
import os
from dotenv import load_dotenv # ça sert à garder le Token en .env .
load_dotenv ()
TOKEN= os.getenv("TOKEN")

if TOKEN is None:
    raise Exception("TOKEN manquant")
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
    print("Commandes synchronisées")
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

#===============================
# Commande: /clash
#===============================

@tree.command(name="clash", description="Clash nerd entre 2 joueurs ⚔️")
async def clash(
    interaction: discord.Interaction,
    opponent: discord.Member,
    phrase1: str,
    phrase2: str
):

    def style(text):
        prefixes = ["DEBUG:", "AI SAYS:", "KERNEL:"]
        suffixes = ["💀", "🤖", "⚡"]
        return f"{random.choice(prefixes)} {text} {random.choice(suffixes)}"

    c1 = style(phrase1)
    c2 = style(phrase2)

    score1 = calculate_score(phrase1)
    score2 = calculate_score(phrase2)

    if score1 > score2:
        winner = interaction.user
    elif score2 > score1:
        winner = opponent
    else:
        winner = None

    result = "🤝 ÉGALITÉ !" if winner is None else f"🏆 Gagnant : {winner.mention}"

    await interaction.response.send_message(
        f"⚔️ **CLASH NERD DUEL** ⚔️\n\n"
        f"👤 {interaction.user.mention} : {c1} — {score1} pts\n"
        f"👤 {opponent.mention} : {c2} — {score2} pts\n\n"
        f"{result}"
    )



#===============================
# SYSTEME DE SCORING
#===============================
 
nerd_words = [
    "python", "bug", "cpu", "ram", "code", "debug",
    "linux", "algorithm", "server", "gpu", "compile","windows","ordinateur","gpu"
]

def calculate_score(text):
    text = text.lower()

    score = 20  # base

    for word in nerd_words:
        if word in text:
            score += 10

    score += min(len(text) // 5, 20)
    score += random.randint(0, 30)

    return score


# ==============================
# LANCEMENT DU BOT
# ==============================


client.run(TOKEN)
