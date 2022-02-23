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
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(text=f'Invoked by {ctx.author.name} - 👍 {submission.score} - 💬 {submission.num_comments}')
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.display_avatar.url}')
        embed.set_image(url=f'{submission.url}')
        embed.add_field(name='Author', value=f'{submission.author}', inline=False)

        await message.edit(embed=embed)

    @slash_command(name='meme', description='Get a meme from reddit.')
    async def _meme(self, ctx):
        await ctx.defer()

        subreddit = await self.bot.reddit_task.subreddit("memes")
        submission = random.choice([submission async for submission in subreddit.hot(limit=50)])

        embed = discord.Embed(
            colour = self.bot.api_color,
            title = f'{submission.title}',
            description = f"r/{submission.subreddit}"
        )
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(text=f'Invoked by {ctx.author.name} - 👍 {submission.score} - 💬 {submission.num_comments}')
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.display_avatar.url}')
        embed.set_image(url=f'{submission.url}')
        embed.add_field(name='Author', value=f'{submission.author}', inline=False)

        await ctx.respond(embed=embed)

    @commands.command(description='Get a dog from reddit.')
    async def dog(self, ctx):
        message = await ctx.reply('Working...')

        subreddit = await self.bot.reddit_task.subreddit("rarepuppers")
        submission = random.choice([submission async for submission in subreddit.hot(limit=50)])

        embed = discord.Embed(
            colour = self.bot.api_color,
            title = f'{submission.title}',
            description = f"r/{submission.subreddit}"
        )
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(text=f'Invoked by {ctx.author.name} - 👍 {submission.score} - 💬 {submission.num_comments}')
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.display_avatar.url}')
        embed.set_image(url=f'{submission.url}')
        embed.add_field(name='Author', value=f'{submission.author}', inline=False)

        await message.edit(embed=embed)

    @slash_command(name='dog', description='Get a dog from reddit.')
    async def _dog(self, ctx):
        await ctx.defer()

        subreddit = await self.bot.reddit_task.subreddit("rarepuppers")
        submission = random.choice([submission async for submission in subreddit.hot(limit=50)])

        embed = discord.Embed(
            colour = self.bot.api_color,
            title = f'{submission.title}',
            description = f"r/{submission.subreddit}"
        )
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(text=f'Invoked by {ctx.author.name} - 👍 {submission.score} - 💬 {submission.num_comments}')
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.display_avatar.url}')
        embed.set_image(url=f'{submission.url}')
        embed.add_field(name='Author', value=f'{submission.author}', inline=False)

        await ctx.respond(embed=embed)

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
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(text=f'Invoked by {ctx.author.name} - 👍 {submission.score} - 💬 {submission.num_comments}')
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.display_avatar.url}')
        embed.set_image(url=f'{submission.url}')
        embed.add_field(name='Author', value=f'{submission.author}', inline=False)

        await message.edit(embed=embed)

    @slash_command(name='gamingsetup', description='Get a gaming setup from reddit.')
    async def _gamingsetup(self, ctx):
        await ctx.defer()

        subreddit = await self.bot.reddit_task.subreddit("battlestations")
        submission = random.choice([submission async for submission in subreddit.hot(limit=50)])

        embed = discord.Embed(
            colour = self.bot.api_color,
            title = f'{submission.title}',
            description = f"r/{submission.subreddit}"
        )
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(text=f'Invoked by {ctx.author.name} - 👍 {submission.score} - 💬 {submission.num_comments}')
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.display_avatar.url}')
        embed.set_image(url=f'{submission.url}')
        embed.add_field(name='Author', value=f'{submission.author}', inline=False)

        await ctx.respond(embed=embed)
    
    @commands.command(description='Get a gaming setup from reddit.')
    async def jdm(self, ctx):
        message = await ctx.reply('Working...')

        subreddit = await self.bot.reddit_task.subreddit("jdm")
        submission = random.choice([submission async for submission in subreddit.hot(limit=50)])

        embed = discord.Embed(
            colour = self.bot.api_color,
            title = f'{submission.title}',
            description = f"r/{submission.subreddit}"
        )
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(text=f'Invoked by {ctx.author.name} - 👍 {submission.score} - 💬 {submission.num_comments}')
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.display_avatar.url}')
        embed.set_image(url=f'{submission.url}')
        embed.add_field(name='Author', value=f'{submission.author}', inline=False)

        await message.edit(embed=embed)
    
    @slash_command(name='jdm', description='Get a gaming setup from reddit.')
    async def _jdm(self, ctx):
        await ctx.defer()

        subreddit = await self.bot.reddit_task.subreddit("jdm")
        submission = random.choice([submission async for submission in subreddit.hot(limit=50)])

        embed = discord.Embed(
            colour = self.bot.api_color,
            title = f'{submission.title}',
            description = f"r/{submission.subreddit}"
        )
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(text=f'Invoked by {ctx.author.name} - 👍 {submission.score} - 💬 {submission.num_comments}')
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.display_avatar.url}')
        embed.set_image(url=f'{submission.url}')
        embed.add_field(name='Author', value=f'{submission.author}', inline=False)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Reddit(bot))
