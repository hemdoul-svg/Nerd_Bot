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
# CLASH NERD FINAL ⚔️
# ==============================

clash_data = {}

# ---------- MODAL ----------
class ClashModal(discord.ui.Modal):

    def __init__(self, duel_id):
        super().__init__(title="⚔️ Écris ton clash")
        self.duel_id = duel_id

        self.phrase = discord.ui.TextInput(
            label="Ton clash nerd",
            placeholder="Ex: Ton CPU chauffe plus qu’un grille-pain 💀",
            max_length=200
        )

        self.add_item(self.phrase)

    async def on_submit(self, interaction: discord.Interaction):

        duel = clash_data[self.duel_id]

        # sauvegarde phrase
        duel["phrases"][interaction.user.id] = self.phrase.value

        await interaction.response.send_message(
            "✅ Clash envoyé !",
            ephemeral=True
        )

        # si les 2 ont répondu
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

            result = (
                "🤝 ÉGALITÉ !"
                if winner is None
                else f"🏆 {winner.mention} gagne le clash !"
            )

            await interaction.channel.send(
                f"⚔️ **CLASH NERD FINAL** ⚔️\n\n"
                f"👤 {user1.mention}\n"
                f"💬 {p1}\n"
                f"📊 Score : {score1}\n\n"
                f"👤 {user2.mention}\n"
                f"💬 {p2}\n"
                f"📊 Score : {score2}\n\n"
                f"{result}"
            )

            # supprime duel
            del clash_data[self.duel_id]


# ---------- BOUTONS ÉCRIRE ----------
class WriteView(discord.ui.View):

    def __init__(self, duel_id):
        super().__init__(timeout=120)
        self.duel_id = duel_id

    @discord.ui.button(label="✍️ Écrire mon clash", style=discord.ButtonStyle.blurple)
    async def write_clash(self, interaction: discord.Interaction, button: discord.ui.Button):

        duel = clash_data[self.duel_id]

        # vérifie joueur
        if interaction.user not in duel["players"]:
            return await interaction.response.send_message(
                "❌ Tu n'es pas dans ce duel",
                ephemeral=True
            )

        # déjà répondu
        if interaction.user.id in duel["phrases"]:
            return await interaction.response.send_message(
                "❌ Tu as déjà envoyé ton clash",
                ephemeral=True
            )

        # ouvre popup
        await interaction.response.send_modal(
            ClashModal(self.duel_id)
        )


# ---------- BOUTON ACCEPTER ----------
class AcceptView(discord.ui.View):

    def __init__(self, duel_id, challenger, opponent):
        super().__init__(timeout=60)

        self.duel_id = duel_id
        self.challenger = challenger
        self.opponent = opponent

    @discord.ui.button(label="⚔️ Accepter le duel", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):

        # seul l’adversaire peut accepter
        if interaction.user != self.opponent:
            return await interaction.response.send_message(
                "❌ Ce n'est pas ton duel",
                ephemeral=True
            )

        await interaction.response.send_message(
            "⚔️ Duel accepté !\n\n"
            "Les 2 joueurs doivent maintenant cliquer sur le bouton ci-dessous pour écrire leur clash.",
            view=WriteView(self.duel_id)
        )


# ---------- COMMANDE ----------
@tree.command(name="clash", description="Clash nerd 1v1 ⚔️")
async def clash(interaction: discord.Interaction, opponent: discord.Member):

    # empêche se clash soi-même
    if opponent == interaction.user:
        return await interaction.response.send_message(
            "❌ Tu ne peux pas te clash toi-même",
            ephemeral=True
        )

    duel_id = str(interaction.id)

    clash_data[duel_id] = {
        "players": [interaction.user, opponent],
        "phrases": {}
    }

    await interaction.response.send_message(
        f"⚔️ {interaction.user.mention} défie {opponent.mention} !\n\n"
        f"{opponent.mention}, clique sur le bouton pour accepter le duel.",
        view=AcceptView(
            duel_id,
            interaction.user,
            opponent
        )
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
