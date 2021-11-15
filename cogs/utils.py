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

        if ctx.guild.icon:
            current.set_author(name=f'{ctx.guild}', icon_url=f'{ctx.guild.icon.url}')
        else:
            current.set_author(name=f'{ctx.guild}', icon_url=ctx.author.display_avatar.url)

        current.timestamp = datetime.datetime.utcnow()
        current.set_footer(text=f'Invoked by {ctx.author.name}.')
        current.set_thumbnail(url=f'{self.bot.user.display_avatar.url}')

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

                if ctx.guild.icon:
                    current.set_author(name=f'{ctx.guild}', icon_url=f'{ctx.guild.icon.url}')
                else:
                    current.set_author(name=f'{ctx.guild}', icon_url=f'{ctx.author.display_avatar.url}')

                current.set_thumbnail(url=f'{self.bot.user.display_avatar.url}')
                current.timestamp = datetime.datetime.utcnow()
                fields = 0
                continue
            current.add_field(name=f'{member.top_role}', value=f'`User` {member.mention} \n `Tag` {member}', inline=True)

        if not current.fields:
            embed = discord.Embed(
                title = 'No members found',
                description = f'No members were found in {role}.',
                colour = self.bot.utils_color
            )
            embed.set_footer(text=f'Invoked by {ctx.author.name}.')

            if ctx.guild.icon:
                embed.set_author(name=f'{ctx.guild}', icon_url=f'{ctx.guild.icon.url}')
            else:
                embed.set_author(name=f'{ctx.guild}', icon_url=f'{ctx.author.display_avatar.url}')

            embed.set_thumbnail(url=f'{self.bot.user.display_avatar.url}')
            embed.timestamp = datetime.datetime.utcnow()

            await ctx.reply(embed=embed)
            return

        if not embeds:
            embeds.append(current)

        paginator = PycordUtils.Pagination.AutoEmbedPaginator(ctx)
        await paginator.run(embeds)

    @commands.command(aliases=['whois'], description='Get info about a user.')
    async def userinfo(self, ctx, member : commands.MemberConverter = None):
        message = await ctx.reply('Working...')

        if member is None:
            member = ctx.author

        embed = discord.Embed(
            colour = self.bot.utils_color,
            title = 'User Information',
            description = "This task was completed without any errors."
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Invoked by {ctx.author.name}')
        embed.set_author(name=f'{member}', icon_url=f'{member.display_avatar.url}')
        embed.set_thumbnail(url=f'{self.bot.user.display_avatar.url}')
        embed.add_field(name='User', value=f'{member.mention}', inline=False)
        embed.add_field(name='ID', value=f'{member.id}', inline=False)
        embed.add_field(name='Bot', value=f'{member.bot}', inline=False)
        embed.add_field(name='Top Role', value=f'{member.top_role.mention}', inline=False)
        embed.add_field(name='Status', value=f'{member.status}', inline=False)

        try:
            embed.add_field(name='Activity', value=f'{member.activity.name}', inline=False)
        except:
            embed.add_field(name='Activity', value='None', inline=False)

        embed.add_field(name='Created At', value=f'{member.created_at.strftime("%m/%d/%Y %H:%M:%S")}', inline=False)
        embed.add_field(name='Joined At', value=f'{member.joined_at.strftime("%m/%d/%Y %H:%M:%S")}', inline=False)
        embed.add_field(name='Boosted', value=bool(member.premium_since), inline=False)

        for activity in member.activities:
            if isinstance(activity, discord.Spotify):
                await message.edit(embed=embed, view=SpotifyView(ctx, member))
                return

        await message.edit(embed=embed)

    @slash_command(name='userinfo', description='Get info about a user.')
    async def _userinfo(self, ctx, member : commands.MemberConverter = None):
        if member is None:
            member = ctx.author

        embed = discord.Embed(
            colour = self.bot.utils_color,
            title = 'User Information',
            description = "This task was completed without any errors."
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Invoked by {ctx.author.name}')
        embed.set_author(name=f'{member}', icon_url=f'{member.display_avatar.url}')
        embed.set_thumbnail(url=f'{self.bot.user.display_avatar.url}')
        embed.add_field(name='User', value=f'{member.mention}', inline=False)
        embed.add_field(name='ID', value=f'{member.id}', inline=False)
        embed.add_field(name='Bot', value=f'{member.bot}', inline=False)
        embed.add_field(name='Top Role', value=f'{member.top_role.mention}', inline=False)
        embed.add_field(name='Status', value=f'{member.status}', inline=False)

        try:
            embed.add_field(name='Activity', value=f'{member.activity.name}', inline=False)
        except:
            embed.add_field(name='Activity', value='None', inline=False)

        embed.add_field(name='Created At', value=f'{member.created_at.strftime("%m/%d/%Y %H:%M:%S")}', inline=False)
        embed.add_field(name='Joined At', value=f'{member.joined_at.strftime("%m/%d/%Y %H:%M:%S")}', inline=False)
        embed.add_field(name='Boosted', value=bool(member.premium_since), inline=False)

        for activity in member.activities:
            if isinstance(activity, discord.Spotify):
                await message.edit(embed=embed, view=SpotifyView(ctx, member))
                return

        await ctx.send(embed=embed)

    @commands.command(description='Get info about a server.')
    async def serverinfo(self, ctx):
        message = await ctx.reply('Working...')

        statuses = [len(list(filter(lambda m: f'{m.status}' == "online", ctx.guild.members))),
                    len(list(filter(lambda m: f'{m.status}' == "idle", ctx.guild.members))),
                    len(list(filter(lambda m: f'{m.status}' == "dnd", ctx.guild.members))),
                    len(list(filter(lambda m: f'{m.status}' == "offline", ctx.guild.members)))]

        embed = discord.Embed(
            colour = self.bot.utils_color,
            title = 'Server Information',
            description = "This task was completed without any errors."
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Invoked by {ctx.author.name}')

        if ctx.guild.icon:
            embed.set_author(name=f'{ctx.guild}', icon_url=f'{ctx.guild.icon.url}')
        else:
            embed.set_author(name=f'{ctx.guild}', icon_url=None)

        embed.set_thumbnail(url=f'{self.bot.user.display_avatar.url}')
        embed.add_field(name='Guild', value=f'{ctx.guild.name}', inline=False)
        embed.add_field(name='Region', value=f'{ctx.guild.region}', inline=False)
        embed.add_field(name='ID', value=f'{ctx.guild.id}', inline=False)
        embed.add_field(name='Created At', value=f'{ctx.guild.created_at.strftime("%m/%d/%Y %H:%M:%S")}', inline=False)
        embed.add_field(name='Members', value=len(ctx.guild.members), inline=False)
        embed.add_field(name='Humans', value=len(list(filter(lambda m: not m.bot, ctx.guild.members))), inline=False)
        embed.add_field(name='Bots', value=len(list(filter(lambda m: m.bot, ctx.guild.members))), inline=False)
        embed.add_field(name='Ban Count', value=len(await ctx.guild.bans()), inline=False)
        embed.add_field(name='Statuses', value=f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", inline=False)
        embed.add_field(name='Text Channels', value=len(ctx.guild.text_channels), inline=False)
        embed.add_field(name='Voice Channels', value=len(ctx.guild.voice_channels), inline=False)
        embed.add_field(name='Categories', value=len(ctx.guild.categories), inline=False)
        embed.add_field(name='Roles', value=len(ctx.guild.roles), inline=False)
        embed.add_field(name='Invites', value=len(await ctx.guild.invites()), inline=False)
        embed.add_field(name='Boost Count', value=f'{ctx.guild.premium_subscription_count}', inline=False)
        embed.add_field(name='Boost Tier', value=f'Level {ctx.guild.premium_tier}')

        await message.edit(embed=embed)

    @slash_command(name='serverinfo', description='Get info about a server.')
    async def _serverinfo(self, ctx):
        statuses = [len(list(filter(lambda m: f'{m.status}' == "online", ctx.guild.members))),
                    len(list(filter(lambda m: f'{m.status}' == "idle", ctx.guild.members))),
                    len(list(filter(lambda m: f'{m.status}' == "dnd", ctx.guild.members))),
                    len(list(filter(lambda m: f'{m.status}' == "offline", ctx.guild.members)))]

        embed = discord.Embed(
            colour = self.bot.utils_color,
            title = 'Server Information',
            description = "This task was completed without any errors."
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Invoked by {ctx.author.name}')

        if ctx.guild.icon:
            embed.set_author(name=f'{ctx.guild}', icon_url=f'{ctx.guild.icon.url}')
        else:
            embed.set_author(name=f'{ctx.guild}')

        embed.set_thumbnail(url=f'{self.bot.user.display_avatar.url}')
        embed.add_field(name='Guild', value=f'{ctx.guild.name}', inline=False)
        embed.add_field(name='Region', value=f'{ctx.guild.region}', inline=False)
        embed.add_field(name='ID', value=f'{ctx.guild.id}', inline=False)
        embed.add_field(name='Created At', value=f'{ctx.guild.created_at.strftime("%m/%d/%Y %H:%M:%S")}', inline=False)
        embed.add_field(name='Members', value=len(ctx.guild.members), inline=False)
        embed.add_field(name='Humans', value=len(list(filter(lambda m: not m.bot, ctx.guild.members))), inline=False)
        embed.add_field(name='Bots', value=len(list(filter(lambda m: m.bot, ctx.guild.members))), inline=False)
        embed.add_field(name='Ban Count', value=len(await ctx.guild.bans()), inline=False)
        embed.add_field(name='Statuses', value=f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", inline=False)
        embed.add_field(name='Text Channels', value=len(ctx.guild.text_channels), inline=False)
        embed.add_field(name='Voice Channels', value=len(ctx.guild.voice_channels), inline=False)
        embed.add_field(name='Categories', value=len(ctx.guild.categories), inline=False)
        embed.add_field(name='Roles', value=len(ctx.guild.roles), inline=False)
        embed.add_field(name='Invites', value=len(await ctx.guild.invites()), inline=False)
        embed.add_field(name='Boost Count', value=f'{ctx.guild.premium_subscription_count}', inline=False)
        embed.add_field(name='Boost Tier', value=f'Level {ctx.guild.premium_tier}')

        await ctx.send(embed=embed)

    @commands.command(description='Check the bots latency status.')
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)

        embed = discord.Embed(
            colour = self.bot.utils_color,
            title = 'Pong!',
            description = f'{latency}ms'
        )

        await ctx.reply(embed=embed)

    @slash_command(name='ping', description='Check the bots latency status.')
    async def _ping(self, ctx):
        latency = round(self.bot.latency * 1000)

        embed = discord.Embed(
            colour = self.bot.utils_color,
            title = 'Pong!',
            description = f'{latency}ms'
        )

        await ctx.send(embed=embed)

    @commands.command(description='Send a guild message to members in a role.')
    @commands.has_permissions(mention_everyone=True)
    async def msgrole(self, ctx, Role : discord.Role, *, input):
        message = await ctx.reply('Working...')

        start_time = datetime.datetime.now()

        total = 0
        success = 0
        fail = 0

        embed = discord.Embed(
            title = 'Guild Mail',
            description = f'{input}',
            colour = self.bot.utils_color
        )

        embed.set_footer(text=f'Invoked by {ctx.author}, for {Role}')

        if ctx.guild.icon:
            embed.set_author(name=f'{ctx.guild}', icon_url=f'{ctx.guild.icon.url}')
        else:
            embed.set_author(name=f'{ctx.guild}', icon_url=None)

        embed.set_thumbnail(url=f'{self.bot.user.display_avatar.url}')

        for member in Role.members:
            total += 1
            try:
                await member.send(embed=embed)
                success += 1
            except:
                fail += 1

        end_time = datetime.datetime.now()

        time = round((end_time - start_time).total_seconds(), 2)

        embed = discord.Embed(
            title = 'Task Completed',
            colour = self.bot.utils_color,
            description = 'This task was completed without any errors.'
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.add_field(name='Total Messages', value=f'{total}', inline=True)
        embed.add_field(name='Sent Messages', value=f'{success}', inline=True)
        embed.add_field(name='Blocked Messages', value=f'{fail}', inline=True)
        embed.add_field(name='Duration', value=f'{time}s', inline=True)
        embed.set_thumbnail(url=f'{self.bot.user.display_avatar.url}')
        embed.set_footer(text=f'Invoked by {ctx.author}, for {Role}')

        await message.edit(embed=embed)

    @commands.command(description='Invite the bot!')
    async def invite(self, ctx):
        embed = discord.Embed(
            title = 'Link Generated.',
            colour = self.bot.utils_color,
            description = 'Before you invite the bot, please take a few moments to read the field below.'
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.add_field(name='Thank you!', value=f"This bot is a project I made for myself and I'm glad you want to invite it to your server, it means the world. This bot has been improving at the same rate as my skillset. Each new skill I learn, I try and apply it to the bot. Once again. Thanks. Enjoy!", inline=True)
        embed.set_thumbnail(url=f'{self.bot.user.display_avatar.url}')
        embed.set_footer(text=f'Invoked by {ctx.author.name}')

        await ctx.send(embed=embed, view=InviteView())

    @slash_command(name='invite', description='Invite the bot!')
    async def _invite(self, ctx):
        embed = discord.Embed(
            title = 'Link Generated.',
            colour = self.bot.utils_color,
            description = 'Before you invite the bot, please take a few moments to read the field below.'
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.add_field(name='Thank you!', value=f"This bot is a project I made for myself and I'm glad you want to invite it to your server, it means the world. This bot has been improving at the same rate as my skillset. Each new skill I learn, I try and apply it to the bot. Once again. Thanks. Enjoy!", inline=True)
        embed.set_thumbnail(url=f'{self.bot.user.display_avatar.url}')
        embed.set_footer(text=f'Invoked by {ctx.author.name}')

        await ctx.send(embed=embed, view=InviteView())

def setup(bot):
    bot.add_cog(Utils(bot))
