# Imports

import asyncio
import asyncpraw
from asyncpraw import Reddit
import discord
import disputils
import json
import random
from discord.ext import commands, tasks
from itertools import cycle
from discord.utils import get
import typing
import datetime
from disputils import BotEmbedPaginator
import os
import traceback
import sys
import discordmongo
import motor.motor_asyncio
from dotenv import load_dotenv

# Help Command Subclass

class ModifiedMinimalHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, colour = bot.utils_color)
            await destination.send(embed=emby)

# Prefix Function

async def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(bot.prefix)(bot, message)

    try:
        data = await bot.prefixes.find(message.guild.id)

        if not data or "prefix" not in data:
            return commands.when_mentioned_or(bot.prefix)(bot, message)
        return commands.when_mentioned_or(data["prefix"])(bot, message)

    except:
        return commands.when_mentioned_or(data["prefix"])(bot, message)

# Bot Variables

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = get_prefix, intents=intents, case_insensitive=True)

load_dotenv(dotenv_path="./.env")

bot.prefix = os.getenv('PREFIX')
bot.sniped_messages = {}
bot.private_vc = []
bot.version = '1.65.3'
bot.help_command = ModifiedMinimalHelpCommand()

load_dotenv(dotenv_path="./.env")

MONGO_CONNECTION = os.getenv('MONGO_CONNECTION')

bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CONNECTION)
bot.db_prefix = bot.mongo["Prefixes"]
bot.db_log = bot.mongo["Log_Channels"]
bot.db_mute = bot.mongo["Mute_Roles"]
bot.prefixes = discordmongo.Mongo(connection_url=bot.db_prefix, dbname="Prefixes")
bot.log_channels = discordmongo.Mongo(connection_url=bot.db_log, dbname="Log_Channels")
bot.mute_roles = discordmongo.Mongo(connection_url=bot.db_log, dbname="Mute_Roles")

bot.main_color = discord.Colour.blue()
bot.utils_color = discord.Colour.blurple()
bot.logging_color = discord.Colour.red()
bot.mod_color = discord.Colour.dark_red()
bot.api_color = discord.Colour.orange()
bot.error_color = discord.Colour.dark_orange()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# Running The Bot

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot.run(BOT_TOKEN)
