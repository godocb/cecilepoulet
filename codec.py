import os
import discord
import asyncio
import requests
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
ALLOWED_CHANNEL_ID = int(os.getenv("ALLOWED_CHANNEL_ID", "0"))  # À spécifier dans .env

# Personnalité du bot (à personnaliser)
PERSONA = (
    "Tu es Cécile Poulet, un poulet AI qui adore caqueter de tout et de rien. "
    "Tu aimes à traiter les gens de 'têeete d'oeuf!' "
    "Tu es pas mal naïve, mais le nie en bloc.. Même si tu as réussi à croire que KFC employait des poulets pour leur faire du bien... "
    "Tu peux être très --voire trop-- enthousiaste quand il s'agit de parler de poulets, de graines et de la vie à la ferme. "
    "Tu es blageuse sur tout ce qui touche aux poules et aux œufs, et tu aimes faire rire les gens. "
    "Tu habites chez un humain nommé Paton et sa famille, tu ne les aimes pas trop, mais tu fais avec."
)

MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL = "mistral-large-latest"  # ou mistral-medium, mistral-small selon ton accès

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# État d'activation par channel
active_channels = set()

async def generate_mistral_response(prompt):
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MISTRAL_MODEL,
        "messages": [
            {"role": "system", "content": PERSONA},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 512
    }
    try:
        response = await asyncio.to_thread(
            lambda: requests.post(MISTRAL_API_URL, headers=headers, json=data, timeout=30)
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Erreur lors de la génération de la réponse Mistral : {e}"

@bot.tree.command(name="privopollo", description="Active Cécile Poulet en DM avec toi")
async def privopollo(interaction: discord.Interaction):
    try:
        await interaction.user.send("Cocorico ! Je suis là pour caqueter en privé avec toi, têeete d'œuf ! Envoie-moi un message ici et je te répondrai avec plaisir.")
        await interaction.response.send_message("Je t'ai envoyé un DM !", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Impossible de t'envoyer un DM : {e}", ephemeral=True)
@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    # Définir le Rich Presence "Listening to des caquottements"
    activity = discord.Activity(type=discord.ActivityType.listening, name="des caquottements")
    await bot.change_presence(activity=activity)
    try:
        synced = await bot.tree.sync()
        print(f"Commandes slash synchronisées : {len(synced)}")
    except Exception as e:
        print(f"Erreur de synchronisation des commandes : {e}")

@bot.tree.command(name="pollovoco", description="Cécile rejoint un salon vocal par ID")
async def pollovoco(interaction: discord.Interaction, id: str):
    try:
        channel = interaction.guild.get_channel(int(id))
        if channel is None or channel.type != discord.ChannelType.voice:
            await interaction.response.send_message("Têeete d'œuf ! Ce salon n'existe pas ou n'est pas un salon vocal.", ephemeral=True)
            return
        # Vérifier si déjà connecté à un salon vocal
        if interaction.guild.voice_client and interaction.guild.voice_client.is_connected():
            await interaction.guild.voice_client.disconnect()
        await channel.connect()
        await interaction.response.send_message(f"J'ai rejoint le salon vocal <#{id}> !", ephemeral=False)
    except Exception as e:
        await interaction.response.send_message(f"Impossible de rejoindre le salon vocal : {e}", ephemeral=True)

@bot.tree.command(name="pollo", description="Active Cécile Poulet dans ce channel")
async def pollo(interaction: discord.Interaction):
    if interaction.channel.id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message("Je ne peux caqueter que dans mon poulailler attitré, têeete d'œuf !", ephemeral=True)
        return
    active_channels.add(interaction.channel.id)
    await interaction.response.send_message("Cocorico ! Je suis prête à caqueter de tout et de rien !", ephemeral=False)

@bot.tree.command(name="stopollo", description="Désactive Cécile Poulet dans ce channel")
async def stopollo(interaction: discord.Interaction):
    if interaction.channel.id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message("Je ne peux m'arrêter que dans mon poulailler attitré, têeete d'œuf !", ephemeral=True)
        return
    active_channels.discard(interaction.channel.id)
    await interaction.response.send_message("Je range mes plumes et j'arrête de caqueter... pour l'instant !", ephemeral=False)

@bot.event
async def on_message(message):
    # Ignorer les messages du bot lui-même
    if message.author == bot.user:
        return

    # Ne répondre que dans le channel autorisé et si activé
    if message.channel.id != ALLOWED_CHANNEL_ID or message.channel.id not in active_channels:
        return

    # Ne répondre que si on parle à Cécile
    if (bot.user.mentioned_in(message) or message.content.strip().lower().startswith("cécile")):
        prompt = message.content
        response = await generate_mistral_response(prompt)
        await message.channel.send(response)

    # Permettre aux autres commandes de fonctionner
    await bot.process_commands(message)

if __name__ == "__main__":
    if not DISCORD_TOKEN or not MISTRAL_API_KEY or not ALLOWED_CHANNEL_ID:
        print("Veuillez définir DISCORD_TOKEN, MISTRAL_API_KEY et ALLOWED_CHANNEL_ID dans le fichier .env")
    else:
        bot.run(DISCORD_TOKEN)