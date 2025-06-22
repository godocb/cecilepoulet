# Cécile Poulet — Bot Discord Mistral AI

Ce projet est un bot Discord qui intègre le LLM Mistral AI, avec une personnalité personnalisable. Le bot ne répond que dans un channel Discord spécifique, selon l'ID configuré, et adopte la personnalité de "Cécile Poulet".

## Fonctionnalités

- Réponses générées par Mistral AI (API officielle)
- Personnalité configurable (par défaut : Cécile Poulet, IA poulet bienveillante et blagueuse)
- Réponses uniquement dans le channel Discord spécifié
- Réponses uniquement si le bot est mentionné ou si le message commence par "Cécile"
- Réponses uniquement en français
- Commandes slash pour activer/désactiver le bot, DM, et rejoindre un vocal

## Prérequis

- Python 3.8 ou supérieur
- Un serveur Discord et un bot Discord (token requis)
- Une clé API Mistral AI
- L'ID du channel Discord où le bot doit répondre

## Installation

1. **Clone le dépôt ou copie les fichiers dans un dossier.**

2. **Installe les dépendances :**
   ```bash
   pip install discord.py requests python-dotenv
   ```

3. **Crée un fichier `.env` à la racine du projet avec le contenu suivant :**
   ```
   DISCORD_TOKEN=ton_token_discord
   MISTRAL_API_KEY=ta_cle_mistral
   ALLOWED_CHANNEL_ID=123456789012345678
   ```
   - Remplace `ton_token_discord` par le token de ton bot Discord.
   - Remplace `ta_cle_mistral` par ta clé API Mistral.
   - Remplace `123456789012345678` par l'ID du channel Discord autorisé.

4. **Lance le bot :**
   ```bash
   python codec.py
   ```

## Utilisation

- Le bot ne répond que dans le channel dont l'ID est spécifié dans `.env`.
- Il répond uniquement si on le mentionne ou si le message commence par "Cécile".
- Les réponses sont générées par Mistral AI, en suivant la personnalité définie dans le code.
- Utilise les commandes slash `/pollo`, `/stopollo`, `/privopollo`, `/pollovoco` pour contrôler le bot.

## Personnalité

La personnalité du bot est définie dans la variable `PERSONA` du fichier [`codec.py`](codec.py:1).  
Modifie ce texte pour adapter le style, l'humour ou la langue du bot selon tes besoins.

## Fichiers

- [`codec.py`](codec.py:1) — Code source principal du bot Discord
- `.env` — Variables d'environnement (non versionné)
- `readme.md` — Ce fichier
- `example.env` — Exemple de configuration
- `.gitignore` — Fichiers à ignorer par git

## Remarques

- Le bot ignore les messages provenant d'autres channels ou qui ne lui sont pas adressés.
- En cas d'erreur d'API ou de configuration, un message d'erreur sera affiché dans le channel.

---

**Auteur :** Cécile Poulet (et son IA)
