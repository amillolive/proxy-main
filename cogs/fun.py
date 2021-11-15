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

class Fun(commands.Cog, description='Public commands. Anyone can use these!'):
    def __init__(self, bot):
        self.bot = bot
        print('Fun Active')

    @commands.command(description='Have the bot repeat what you say.')
    async def echo(self, ctx, *, message : commands.clean_content):
        await ctx.reply(message)

    @slash_command(name='echo', description='Have the bot repeat what you say.')
    async def _echo(self, ctx, *, message : commands.clean_content):
        await ctx.send(message)

    @commands.command(description='Flip a coin.')
    async def coinflip(self, ctx):
        embed = discord.Embed(
            title = 'Coinflip',
            description = 'You flipped a coin.',
            colour = self.bot.main_color
        )

        n = random.randint(0, 1)

        if n == 1:
            embed.add_field(name='Heads!', value='The coin landed on heads.', inline=False)
        else:
            embed.add_field(name='Tails!', value='The coin landed on tails.', inline=False)

        await ctx.reply(embed=embed)

    @slash_command(name='coinflip', description='Flip a coin.')
    async def _coinflip(self, ctx):
        embed = discord.Embed(
            title = 'Coinflip',
            description = 'You flipped a coin.',
            colour = self.bot.main_color
        )

        n = random.randint(0, 1)

        if n == 1:
            embed.add_field(name='Heads!', value='The coin landed on heads.', inline=False)
        else:
            embed.add_field(name='Tails!', value='The coin landed on tails.', inline=False)

        await ctx.reply(embed=embed)

    @commands.command(name='8ball', description='Ask the magical 8ball a question.')
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes, most definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]

        embed = discord.Embed(
            title = 'Magical 8ball',
            description = 'You asked the magical 8ball a question.',
            colour = self.bot.main_color
        )
        embed.add_field(name='Question', value=f'{question}', inline=False)
        embed.add_field(name='Answer', value=f'{random.choice(responses)}', inline=False)

        await ctx.reply(embed=embed)

    @slash_command(name='8ball', description='Ask the magical 8ball a question.')
    async def _ball(self, ctx, *, question):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes, most definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]

        embed = discord.Embed(
            title = 'Magical 8ball',
            description = 'You asked the magical 8ball a question.',
            colour = self.bot.main_color
        )
        embed.add_field(name='Question', value=f'{question}', inline=False)
        embed.add_field(name='Answer', value=f'{random.choice(responses)}', inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))
