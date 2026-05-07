# ==============================
# IMPORTS
# ==============================

import discord
from discord import app_commands
import random
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise Exception("TOKEN manquant")

# ==============================
# SYSTEME DE SCORING (IMPORTANT)
# ==============================

nerd_words = [
    "python", "bug", "cpu", "ram", "code", "debug",
    "linux", "algorithm", "server", "gpu", "compile",
    "windows", "ordinateur"
]

def calculate_score(text):
    text = text.lower()

    score = 20

    for word in nerd_words:
        if word in text:
            score += 10

    score += min(len(text) // 5, 20)
    score += random.randint(0, 30)

    return score


# ==============================
# CONFIG BOT
# ==============================

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ==============================
# READY
# ==============================

@client.event
async def on_ready():
    if not hasattr(client, "synced"):
        await tree.sync()
        client.synced = True
        print("Commandes synchronisées")

    print(f"Bot connecté : {client.user}")


# ==============================
# COMMANDES BASIQUES
# ==============================

@tree.command(name="regles", description="Règles du serveur")
async def regles(interaction: discord.Interaction):
    await interaction.response.send_message(
        "📜 RÈGLES :\n1. Respect\n2. Pas spam\n3. Amuse-toi 🤓\n4. Soyer Nerd🤓"
    )


@tree.command(name="coinflip", description="Pile ou face")
async def coinflip(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(["Pile🪙", "Face🪙"]))


@tree.command(name="iq", description="Test IQ")
async def iq(interaction: discord.Interaction):
    await interaction.response.send_message(f"IQ : {random.randint(-160,160)}")


@tree.command(name="fact", description="Fact geek")
async def fact(interaction: discord.Interaction):
    facts = [
    "Le premier bug informatique était un insecte 🐛",
    "Minecraft a été créé par Notch",
    "Le langage Python date de 1991",
    "Le CPU exécute des milliards d’opérations par seconde",
    "Linux est utilisé sur la majorité des serveurs",
    "Les GPU sont plus rapides que les CPU pour l’IA",
    "Le premier ordinateur occupait une pièce entière",
    "Lamig a déjà été gentil avec quelqu'un, c'était en 2020..."
]
    await interaction.response.send_message(random.choice(facts))

@tree.command(name="help", description="Liste des commandes")
async def help(interaction: discord.Interaction):

    message = (
        "**Commandes disponibles :**\n\n"
        "📜 /regles → règles du serveur\n"
        "🪙 /coinflip → pile ou face\n"
        "🧠 /iq → test IQ\n"
        "📚 /fact → facts nerd\n"
        "⚔️ /clash → duel nerd 1v1\n"
    )

    await interaction.response.send_message(message)

    
# ==============================
# CLASH NERD 1V1 ⚔️
# ==============================

clash_data = {}


# ---------- MODAL ----------
class ClashModal(discord.ui.Modal):

    def __init__(self, duel_id):
        super().__init__(title="⚔️ Clash nerd")
        self.duel_id = duel_id

        self.phrase = discord.ui.TextInput(
            label="Ton clash",
            max_length=200
        )

        self.add_item(self.phrase)

    async def on_submit(self, interaction: discord.Interaction):

        if self.duel_id not in clash_data:
            return await interaction.response.send_message("❌ Duel expiré", ephemeral=True)

        duel = clash_data[self.duel_id]
        duel["phrases"][interaction.user.id] = self.phrase.value

        await interaction.response.send_message("✅ Clash enregistré", ephemeral=True)

        # si 2 réponses
        if len(duel["phrases"]) == 2:

            user1, user2 = duel["players"]

            p1 = duel["phrases"][user1.id]
            p2 = duel["phrases"][user2.id]

            s1 = calculate_score(p1)
            s2 = calculate_score(p2)

            if s1 > s2:
                winner = user1
            elif s2 > s1:
                winner = user2
            else:
                winner = None

            result = "🤝 ÉGALITÉ !" if winner is None else f"🏆 {winner.mention} gagne !"

            await interaction.channel.send(
                f"⚔️ CLASH FINAL ⚔️\n\n"
                f"{user1.mention}: {p1} ({s1})\n"
                f"{user2.mention}: {p2} ({s2})\n\n"
                f"{result}"
            )

            del clash_data[self.duel_id]


# ---------- VIEW ----------
class WriteView(discord.ui.View):

    def __init__(self, duel_id):
        super().__init__(timeout=120)
        self.duel_id = duel_id

    @discord.ui.button(label="✍️ Écrire mon clash", style=discord.ButtonStyle.blurple)
    async def write(self, interaction: discord.Interaction, button: discord.ui.Button):

        duel = clash_data.get(self.duel_id)

        if not duel:
            return await interaction.response.send_message("❌ Duel expiré", ephemeral=True)

        if interaction.user not in duel["players"]:
            return await interaction.response.send_message("❌ Pas dans le duel", ephemeral=True)

        if interaction.user.id in duel["phrases"]:
            return await interaction.response.send_message("❌ Déjà répondu", ephemeral=True)

        await interaction.response.send_modal(ClashModal(self.duel_id))


class AcceptView(discord.ui.View):

    def __init__(self, duel_id, challenger, opponent):
        super().__init__(timeout=60)
        self.duel_id = duel_id
        self.challenger = challenger
        self.opponent = opponent

    @discord.ui.button(label="⚔️ Accepter", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user != self.opponent:
            return await interaction.response.send_message("❌ Pas ton duel", ephemeral=True)

        await interaction.response.send_message(
            "⚔️ Duel accepté ! Cliquez pour écrire votre clash",
            view=WriteView(self.duel_id)
        )


# ---------- COMMANDE CLASH ----------
@tree.command(name="clash", description="Clash nerd 1v1 ⚔️")
async def clash(interaction: discord.Interaction, opponent: discord.Member):

    if opponent == interaction.user:
        return await interaction.response.send_message("❌ Impossible", ephemeral=True)

    duel_id = str(interaction.id)

    clash_data[duel_id] = {
        "players": [interaction.user, opponent],
        "phrases": {}
    }

    await interaction.response.send_message(
        f"⚔️ {interaction.user.mention} vs {opponent.mention}",
        view=AcceptView(duel_id, interaction.user, opponent)
    )


# ==============================
# RUN
# ==============================

client.run(TOKEN)
