# Startup timer
import time
startup_time = time.time()

import disnake
from disnake.ext import commands
import json
import os
from typing import Dict
from localization import Localization
from config import Config
from logger import Logger
from disnake import OptionChoice, OptionType

# Global aid objects
conf = Config()
l10n = Localization(conf.get("localization_code"))
log = Logger.getInstance(verbose=conf.get("log_verb_level"), debug=conf.get("log_debug"), file_path=conf.get("log_path"))
    
# Get Discord token from file
TOKEN = ""
token_path = os.path.join(os.path.dirname(__file__), 'token.txt')
with open(token_path, 'r') as token_file:
    TOKEN = token_file.read().strip()

def load_reactions_data():
    """
    comment me in english
    """
    log.write(l10n.get("loading_reactions_data"), status=5, level=4)
    try:
        with open(conf.get("reactions_path"), 'r') as file:
            log.write(l10n.get("loading_reactions_data"), status=5, level=5)
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        log.write(l10n.get("json_decode_error", exception=e), status=2, level=2)
        return {}
    
reactions_data = load_reactions_data()

# Discord intents
intents = disnake.Intents.all()

# Create Bot
bot = commands.Bot(command_prefix=conf.get("cmd_prefix"), intents=intents, activity=disnake.Game(name=conf.get("game_activity")))

@bot.event
async def on_ready():
    """
    comment me in english
    """
    log.write(l10n.get("is_running", name=bot.user, seconds=round(time.time()-startup_time, 1)), status=6, level=2)

@bot.slash_command(name = l10n.get("cmd_reactions"), description=l10n.get("cmd_reactions_description"))
@commands.has_permissions(manage_messages = True, manage_channels = True)
async def reactions(
    ctx,
    channel: disnake.TextChannel = commands.Param(name = l10n.get("channel_select"), description = l10n.get("channel_select_description")),
    action: str = commands.Param(
        choices=[
            OptionChoice(name=l10n.get("add"), value=l10n.get("add")),
            OptionChoice(name=l10n.get("remove"), value=l10n.get("remove"))
        ],
        name = l10n.get("action"), 
        description = l10n.get("action_description")
    ),
    emoji: str = commands.Param(name = l10n.get("emoji"), description = l10n.get("emoji_description"))
):
    """
    comment me in english
    """
    if action == l10n.get("add"):
        if emoji not in reactions_data.get(str(channel.id), {}).get('emojis', []):
            reactions_data.setdefault(str(channel.id), {}).setdefault('emojis', {})[emoji] = True
            await ctx.send(l10n.get("cmd_reaction_was_added", name=emoji, channel=channel.mention), ephemeral=True)
        else:
            reactions_data[str(channel.id)]['emojis'][emoji] = True
            await ctx.send(l10n.get("cmd_reaction_was_added", name=emoji, channel=channel.mention), ephemeral=True)
    elif action == l10n.get("remove"):
        if emoji in reactions_data.get(str(channel.id), {}).get('emojis', []):
            reactions_data[str(channel.id)]['emojis'][emoji] = False
            await ctx.send(l10n.get("cmd_reaction_was_removed", name=emoji, channel=channel.mention), ephemeral=True)
        else:
            await ctx.send(l10n.get("cmd_reaction_not_exist", name=emoji, channel=channel.mention), ephemeral=True)

    with open('reactions.json', 'w') as file:
        json.dump(reactions_data, file, indent=4)

@bot.slash_command(name = l10n.get("cmd_threads"), description=l10n.get("cmd_threads_description"))
@commands.has_permissions(manage_messages = True, manage_channels = True)
async def threads(
    ctx,
    channel: disnake.TextChannel = commands.Param(name = l10n.get("channel_select"), description = l10n.get("channel_select_description")),
    action: str = commands.Param(
        choices=[
            OptionChoice(name=l10n.get("add"), value=l10n.get("add")),
            OptionChoice(name=l10n.get("remove"), value=l10n.get("remove"))
        ],
        name = l10n.get("action"), 
        description = l10n.get("action_description")
    ),
    name: str = commands.Param(name = l10n.get("name"), description = l10n.get("name_description"))
):
    """
    comment me in english
    """
    thread_data = load_thread_data()

    if action == l10n.get("add"):
        thread_data.setdefault(str(channel.id), {}).setdefault('threads', {})[name] = True
        save_thread_data(thread_data)

        await ctx.send(l10n.get("cmd_threads_was_added", channel=channel), ephemeral=True)
    elif action == l10n.get("remove"):
        thread_data.setdefault(str(channel.id), {}).setdefault('threads', {})[name] = False
        save_thread_data(thread_data)

        await ctx.send(l10n.get("cmd_threads_was_removed", channel=channel), ephemeral=True)

@bot.event
async def on_message(message):
    """
    comment me in english
    """
    log.write(l10n.get("new_message", id=message.channel.id), status=5, level=7)
    reactions_data = load_reactions_data()
    thread_data = load_thread_data()

    channel_id = str(message.channel.id)
    if channel_id in reactions_data:
        for emoji, should_react in reactions_data[channel_id].get('emojis', {}).items():
            if should_react and not (message.author.bot or message.is_system()):
                await message.add_reaction(emoji)
        return

    if channel_id in thread_data:
        for thread_name, should_create in thread_data[str(message.channel.id)].get('threads', {}).items():
            if should_create:
                thread = await message.create_thread(name=thread_name)

                welcome_message = await thread.send(f".")

                await welcome_message.delete()

def load_thread_data():
    """
    comment me in english
    """
    log.write(l10n.get("loading_threads_data"), status=5, level=4)
    try:
        with open(conf.get("thread_path"), 'r') as file:
            log.write(l10n.get("loaded_threads_data"), status=5, level=5)
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        log.write(l10n.get("json_decode_error", exception=e), status=2, level=2)
        return {}

def save_thread_data(thread_data):
    """
    comment me in english
    """
    log.write(l10n.get("saving_threads_data"), status=5, level=4)
    try:
        with open(conf.get("thread_path"), 'w') as file:
            json.dump(thread_data, file, indent=4)
    except Exception as e:
        log.write(l10n.get("saving_error", exception=e), status=2, level=2)
        return {}

def display_welcome(displayed = conf.get("welcome")):
    """
    comment me in english
    """
    if displayed:
        log.write(l10n.get("welcome"), status=0, level=3, log_header=False)

def display_debug():
    log.write(l10n.get("current_loc", locale=conf.get("localization_code")), status=5, level=5)
    log.write(l10n.get("current_ext", folder=conf.get("extension_path")), status=5, level=5)
    log.write(l10n.get("current_ffm", ffmpeg=conf.get("ffmpeg_path")), status=5, level=5)
    log.write(l10n.get("current_pre", prefix=conf.get("cmd_prefix")), status=5, level=5)

def load_extensions():
    """
    comment me in english
    """
    for filename in os.listdir(conf.get("extension_path")):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

# Entry point
if __name__ == "__main__":
    display_welcome()
    display_debug()
    load_extensions()
    bot.run(TOKEN)