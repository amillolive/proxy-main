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
from .classes import MXRoleConverter
from .classes import MXDurationConverter

if __name__ == '__main__':
    os.system('python main.py')

class Owner(commands.Cog, description='Owner commands. Only the developer can use these.'):
    def __init__(self, bot):
        self.bot = bot
        print('Owner Active')

    @commands.command(description='Leave a guild. Only the dev can use this.')
    async def leaveg(self, ctx, guild : discord.Guild):
        if not commands.is_owner():
            return
        else:
            guild.leave
            await ctx.reply(f'Left guild {guild.name}.')

def setup(bot):
    bot.add_cog(Owner(bot))
