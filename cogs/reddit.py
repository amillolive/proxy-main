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
from discord_components import *

if __name__ == '__main__':
    os.system('python main.py')

class Reddit(commands.Cog, description='Public commands. Anyone can use these!'):
    def __init__(self, bot):
        self.bot = bot
        print('Reddit Active')

    @commands.command(description='Get a meme from reddit.')
    async def meme(self, ctx):
        message = await ctx.reply('Working...')

        subreddit = await self.bot.reddit_task.subreddit("memes")
        submission = random.choice([submission async for submission in subreddit.hot(limit=50)])

        embed = discord.Embed(
            colour = self.bot.api_color,
            title = f'{submission.title}',
            description = f"r/{submission.subreddit}"
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Invoked by {ctx.author.name}')
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_image(url=f'{submission.url}')
        embed.add_field(name='Author', value=f'{submission.author}', inline=True)
        embed.add_field(name='Upvotes', value=f'{submission.score}')
        
        await message.edit(embed=embed)

    @commands.command(description='Get a dog from reddit.')
    async def dogs(self, ctx):
        message = await ctx.reply('Working...')

        subreddit = await self.bot.reddit_task.subreddit("rarepuppers")
        submission = random.choice([submission async for submission in subreddit.hot(limit=50)])

        embed = discord.Embed(
            colour = self.bot.api_color,
            title = f'{submission.title}',
            description = f"r/{submission.subreddit}"
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Invoked by {ctx.author.name}')
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_image(url=f'{submission.url}')
        embed.add_field(name='Author', value=f'{submission.author}', inline=True)
        embed.add_field(name='Upvotes', value=f'{submission.score}')
        
        await message.edit(embed=embed)

    @commands.command(description='Get a gaming setup from reddit.')
    async def gamingsetup(self, ctx):
        message = await ctx.reply('Working...')

        subreddit = await self.bot.reddit_task.subreddit("battlestations")
        submission = random.choice([submission async for submission in subreddit.hot(limit=50)])

        embed = discord.Embed(
            colour = self.bot.api_color,
            title = f'{submission.title}',
            description = f"r/{submission.subreddit}"
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Invoked by {ctx.author.name}')
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_image(url=f'{submission.url}')
        embed.add_field(name='Author', value=f'{submission.author}', inline=True)
        embed.add_field(name='Upvotes', value=f'{submission.score}')
        
        await message.edit(embed=embed)

def setup(bot):
    bot.add_cog(Reddit(bot))
