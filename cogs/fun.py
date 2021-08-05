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
from .classes import MXRoleConverter
from .classes import MXDurationConverter
import motor.motor_asyncio

class Fun(commands.Cog, description='Public commands. Anyone can use these!'):
    def __init__(self, bot):
        self.bot = bot
        print('Fun Active')

    @commands.command(description='Have the bot repeat what you say.')
    async def echo(self, ctx, *, message : commands.clean_content):
        await ctx.reply(message)

    @commands.command(description='Flip a coin.')
    async def coinflip(self, ctx):
        n = random.randint(0, 1)
        await ctx.reply("Heads!" if n == 1 else "Tails!")

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

        await ctx.send(f'**Question**: {question}\n**Answer**: {random.choice(responses)}')

def setup(bot):
    bot.add_cog(Fun(bot))
