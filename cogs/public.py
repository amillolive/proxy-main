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

if __name__ == '__main__':
    os.system('python main.py')

class Public(commands.Cog, description='Public commands. Anyone can use these!'):
    def __init__(self, bot):
        self.bot = bot
        print('Public Active')

    @commands.command(description='Get a list of members in a role.')
    async def members(self, ctx, *, role : MXRoleConverter):
        embeds = []

        fields = 0
        current = discord.Embed(
            title = f'Members in {role}',
            description = 'This task was completed successfully',
            colour = self.bot.utils_color
        )
        current.set_author(name=f'{ctx.guild}', icon_url=f'{ctx.guild.icon_url}')
        current.timestamp = datetime.datetime.utcnow()
        current.set_footer(text=f'Invoked by {ctx.author.name}.')

        for member in role.members:
            fields += 1
            if fields == 25:
                embeds.append(current)
                current = discord.Embed(
                    title = f'Members in {role}',
                    description = 'This task was completed successfully',
                    colour = self.bot.utils_color
                )
                current.set_footer(text=f'Invoked by {ctx.author.name}.')
                current.set_author(name=f'{ctx.guild}', icon_url=f'{ctx.guild.icon_url}')
                current.timestamp = datetime.datetime.utcnow()
                fields = 0
                continue
            current.add_field(name=str(member.top_role), value=f'`User` {member.mention} \n `Tag` {member}', inline=True)

        if not embeds:
            embeds.append(current)

        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()

    @commands.command(description='Get a meme from reddit.')
    async def meme(self, ctx):
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
        await ctx.reply(embed=embed)

    @commands.command(description='Create a temporary voice channel for yourself.')
    async def createvoice(self, ctx, *, name):
        category = ctx.channel.category
        overwrites = {
            ctx.author: discord.PermissionOverwrite(
                connect=True,
                speak=True,
                mute_members=True,
                deafen_members=True,
                manage_channels=True,
                manage_permissions=True,
                move_members=True
            ),
            ctx.guild.default_role: discord.PermissionOverwrite(
                connect=False,
                speak=False,
                mute_members=False,
                deafen_members=False,
                manage_channels=False,
                manage_permissions=False
            )
        }
        channel = await ctx.guild.create_voice_channel(name=name, overwrites=overwrites, category=category, reason=f'Private voice for {ctx.author}.')
        self.bot.private_vc.append(channel.id)
        print(self.bot.private_vc)
        await ctx.reply('Private voice channel created.')
        return

    @commands.command(description='Have the bot repeat what you say.')
    async def echo(self, ctx, *, message : commands.clean_content):
        await ctx.reply(message)

    @commands.command(description='Flip a coin.')
    async def coinflip(self, ctx):
        n = random.randint(0, 1)
        await ctx.reply("Heads!" if n == 1 else "Tails!")

    @commands.command(description='Check the bots latency.')
    async def ping(self, ctx):
        await ctx.reply(f'**Pong**! {round(self.bot.latency * 1000)}ms')

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

    @commands.command(description='Get a dog from reddit.')
    async def dogs(self, ctx):
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
        await ctx.reply(embed=embed)

    @commands.command(description='Get a gaming setup from reddit.')
    async def gamingsetup(self, ctx):
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
        await ctx.reply(embed=embed)

    @commands.command(aliases=['whois'], description='Get info about a user.')
    async def userinfo(self, ctx, member : commands.MemberConverter = None):
        if member is None:
            member = ctx.author

        embed = discord.Embed(
            colour = self.bot.utils_color,
            title = 'User Information',
            description = "This task was completed without any errors."
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Invoked by {ctx.author.name}')
        embed.set_author(name=f'{member}', icon_url=f'{member.avatar_url}')
        embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
        embed.add_field(name='User', value=f'{member.mention}', inline=True)
        embed.add_field(name='ID', value=f'{member.id}', inline=False)
        embed.add_field(name='Bot', value=f'{member.bot}', inline=True)
        embed.add_field(name='Top Role', value=f'{member.top_role.mention}', inline=True)
        embed.add_field(name='Status', value=f'{member.status}', inline=True)
        embed.add_field(name='Activity', value=f'{member.activity}', inline=True)
        embed.add_field(name='Created At', value=f'{member.created_at.strftime("%m/%d/%Y %H:%M:%S")}', inline=False)
        embed.add_field(name='Joined At', value=f'{member.joined_at.strftime("%m/%d/%Y %H:%M:%S")}', inline=False)
        embed.add_field(name='Boosted', value=bool(member.premium_since), inline=True)

        await ctx.reply(embed=embed)

    @commands.command(description='Get info about a server.')
    async def serverinfo(self, ctx):
        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

        embed = discord.Embed(
            colour = self.bot.utils_color,
            title = 'Server Information',
            description = "This task was completed without any errors."
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Invoked by {ctx.author.name}')
        embed.set_author(name=f'{ctx.guild}', icon_url=f'{ctx.guild.icon_url}')
        embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
        embed.add_field(name='Guild', value=f'{ctx.guild.name}', inline=True)
        embed.add_field(name='Region', value=f'{ctx.guild.region}', inline=True)
        embed.add_field(name='ID', value=f'{ctx.guild.id}', inline=False)
        embed.add_field(name='Created At', value=f'{ctx.guild.created_at.strftime("%m/%d/%Y %H:%M:%S")}', inline=False)
        embed.add_field(name='Members', value=len(ctx.guild.members), inline=True)
        embed.add_field(name='Humans', value=len(list(filter(lambda m: not m.bot, ctx.guild.members))), inline=True)
        embed.add_field(name='Bots', value=len(list(filter(lambda m: m.bot, ctx.guild.members))), inline=True)
        embed.add_field(name='Ban Count', value=len(await ctx.guild.bans()), inline=True)
        embed.add_field(name='Statuses', value=f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", inline=False)
        embed.add_field(name='Text Channels', value=len(ctx.guild.text_channels), inline=True)
        embed.add_field(name='Voice Channels', value=len(ctx.guild.voice_channels), inline=True)
        embed.add_field(name='Categories', value=len(ctx.guild.categories), inline=True)
        embed.add_field(name='Roles', value=len(ctx.guild.roles), inline=True)
        embed.add_field(name='Invites', value=len(await ctx.guild.invites()), inline=True)

        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Public(bot))
