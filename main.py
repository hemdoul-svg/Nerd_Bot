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
        "Le langage Python a été créé en 1991",
        "Lamig a déja était gentil avec quelqu'un ,c'était en 2020..."
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
# CLASH NERD 1v1 AVEC POPUP
# ==============================

clash_data = {}

# ---------- MODAL ----------
class ClashModal(discord.ui.Modal):

    def __init__(self, duel_id, user):
        super().__init__(title="⚔️ Ton clash nerd")
        self.duel_id = duel_id
        self.user = user

        self.phrase = discord.ui.TextInput(
            label="Ton clash",
            placeholder="Écris ton meilleur roast nerd...",
            max_length=200
        )

        self.add_item(self.phrase)

    async def on_submit(self, interaction: discord.Interaction):

        duel = clash_data[self.duel_id]
        duel["phrases"][interaction.user.id] = self.phrase.value

        await interaction.response.send_message("✅ Clash enregistré !", ephemeral=True)

        # Si les 2 joueurs ont répondu
        if len(duel["phrases"]) == 2:

            user1, user2 = duel["players"]

            p1 = duel["phrases"][user1.id]
            p2 = duel["phrases"][user2.id]

            score1 = calculate_score(p1)
            score2 = calculate_score(p2)

            if score1 > score2:
                winner = user1
            elif score2 > score1:
                winner = user2
            else:
                winner = None

            result = "🤝 ÉGALITÉ !" if winner is None else f"🏆 {winner.mention} gagne !"

            await interaction.channel.send(
                f"⚔️ **CLASH NERD FINAL** ⚔️\n\n"
                f"{user1.mention} : {p1} ({score1} pts)\n"
                f"{user2.mention} : {p2} ({score2} pts)\n\n"
                f"{result}"
            )

            # reset duel
            del clash_data[self.duel_id]


# ---------- BOUTON ----------
class ClashView(discord.ui.View):

    def __init__(self, duel_id, challenger, opponent):
        super().__init__(timeout=60)
        self.duel_id = duel_id
        self.challenger = challenger
        self.opponent = opponent

    @discord.ui.button(label="Accepter le duel ⚔️", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user != self.opponent:
            return await interaction.response.send_message("❌ Ce n'est pas ton duel", ephemeral=True)

        await interaction.response.send_message("⚔️ Duel accepté ! Check tes popups", ephemeral=True)

        # popup challenger
        await self.challenger.send_modal(ClashModal(self.duel_id, self.challenger))

        # popup opponent
        await interaction.followup.send_modal(ClashModal(self.duel_id, self.opponent))


# ---------- COMMANDE ----------
@tree.command(name="clash", description="Clash nerd 1v1 ⚔️")
async def clash(interaction: discord.Interaction, opponent: discord.Member):

    duel_id = str(interaction.id)

    clash_data[duel_id] = {
        "players": [interaction.user, opponent],
        "phrases": {}
    }

    await interaction.response.send_message(
        f"⚔️ {interaction.user.mention} défie {opponent.mention} !\n"
        f"Clique sur le bouton pour accepter !",
        view=ClashView(duel_id, interaction.user, opponent)
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
