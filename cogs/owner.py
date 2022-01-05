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
from .views.views import InviteView, SpotifyView
from .classes import MXRoleConverter
from .classes import MXDurationConverter

if __name__ == '__main__':
    os.system('python main.py')

class Owner(commands.Cog, description='Owner commands. Only the developer can use these.'):
    def __init__(self, bot):
        self.bot = bot
        print('Owner Active')

    @commands.group(description='Leave a guild. Only the dev can use this.', invoke_without_command=True)
    @commands.is_owner()
    async def guild(self, ctx):
        pass

    @guild.command(description='Leave a guild that the bot is in.')
    @commands.is_owner()
    async def leave(self, ctx, guild : discord.Guild):
        guild.leave

        embed = discord.Embed(
            colour = self.bot.utils_color,
            title = 'Left Guild',
            description = "This task was completed without any errors."
        )
        embed.set_footer(text=f'Invoked by {ctx.author.name}')
        embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.display_avatar.url}')
        embed.add_field(name='Guild', value=f'`{guild.name} ({guild.id})`', inline=False)

        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(Owner(bot))
