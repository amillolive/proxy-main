import asyncio
import asyncpraw
from asyncpraw import Reddit
import discord
import json
import random
from discord.ext import commands, tasks
from discord.commands import slash_command
from itertools import cycle
from discord.utils import get
import typing
import datetime
import os
import traceback
import sys
import discordmongo
import motor.motor_asyncio
from discord import Spotify
import PycordUtils
from dotenv import load_dotenv

if __name__ == '__main__':
    os.system('python main.py')

class MXRoleConverter(commands.RoleConverter):
    async def convert(self, ctx, argument):
        role = discord.utils.find(lambda r: argument.lower() in r.name.lower(), ctx.guild.roles)
        if role is None:
            return await super().convert(ctx, argument)
        else:
            return role

class MXDurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
        amount = argument[:-1]
        unit = argument[-1]

        if amount.isdigit() and unit in ['s', 'm', 'h', 'd']:
            return (int(amount), unit)

class Classes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('Classes Active')

def setup(bot):
    bot.add_cog(Classes(bot))
