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

class Utils(commands.Cog, description='Utils commands. Used mainly for gathering and sending info.'):
    def __init__(self, bot):
        self.bot = bot
        print('Utils Active')

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
        current.set_thumbnail(url=f'{self.bot.user.avatar_url}')

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
                current.set_thumbnail(url=f'{self.bot.user.avatar_url}')
                current.timestamp = datetime.datetime.utcnow()
                fields = 0
                continue
            current.add_field(name=str(member.top_role), value=f'`User` {member.mention} \n `Tag` {member}', inline=True)

        if not embeds:
            embeds.append(current)

        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()

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

    @commands.command(description='Check the bots latency.')
    async def ping(self, ctx):
        await ctx.reply(f'**Pong**! {round(self.bot.latency * 1000)}ms')

    @commands.command(description='Send a guild message to members in a role.')
    @commands.has_permissions(mention_everyone=True)
    async def msgrole(self, ctx, Role : discord.Role, *, input):
        message = await ctx.reply('Working...')

        success = 0
        fail = 0
        total = 0

        embed = discord.Embed(
            title = 'Guild Mail',
            description = f'{input}',
            colour = self.bot.utils_color
        )

        embed.set_footer(text=f'Invoked by {ctx.author.name}, for {Role}')
        embed.set_author(name=f'{ctx.guild}', icon_url=f'{ctx.guild.icon_url}')
        embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')

        for member in Role.members:
            total += 1
            try:
                await member.send(embed=embed)
                success += 1
            except:
                fail += 1

        embed = discord.Embed(
            title = 'Task Completed',
            colour = self.bot.utils_color,
            description = 'This task was completed without any errors.'
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.add_field(name='Total', value=f'{total}', inline=True)
        embed.add_field(name='Success', value=f'{success}', inline=True)
        embed.add_field(name='Failed', value=f'{fail}', inline=True)
        embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
        embed.set_footer(text=f'Invoked by {ctx.author.name}, for {Role}')

        await message.edit(embed=embed)

def setup(bot):
    bot.add_cog(Utils(bot))
