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

class Mod(commands.Cog, description='Moderation commands. Only mods can use these.'):
    def __init__(self, bot):
        self.bot = bot
        print('Mod Active')

    @commands.command(description='Set the muterole for the guild.')
    @commands.has_permissions(manage_messages=True)
    async def muterole(self, ctx, role : MXRoleConverter):
        data = await self.bot.mute_roles.find(ctx.guild.id)

        if not data or "role_id" not in data:
            data = {"_id": ctx.guild.id, "role_id": role.id}

        data["role_id"] = role.id
        await self.bot.mute_roles.upsert(data)

        await ctx.reply(f"The mute role has been changed to `{role}`. If you couldn't use the mute commands before, you should be able to now.")

    @commands.command(description='Mute a member. Must have set the muterole.')
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member : commands.MemberConverter, *, reason=None):
        data = await self.bot.mute_roles.find(ctx.guild.id)

        if not data or "role_id" not in data:
            await ctx.reply("You haven't set a mute role. Refer to the help command to set a mute role.")
            return

        muted_role_id = data["role_id"]
        muted_role = ctx.guild.get_role(muted_role_id)

        await member.add_roles(muted_role, reason=reason)

        embed = discord.Embed(
            title = 'Muted Member',
            description = 'This task was completed without any errors.',
            colour = self.bot.mod_color
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.display_avatar.url}')
        embed.set_footer(text='Invoked by {ctx.author.name}')

        if ctx.guild.icon:
            embed.set_thumbnail(url=f'{ctx.guild.icon.url}')

        embed.add_field(name='Member', value=f'{member}', inline=True)
        embed.add_field(name='Reason', value=f'{reason}', inline=True)

        await ctx.reply(embed=embed)

    @commands.command(description='Temporarily mute a member. Must have set the muterole.')
    @commands.has_permissions(manage_messages=True)
    async def tempmute(self, ctx, member : commands.MemberConverter, duration : MXDurationConverter):
        multiplier = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        amount, unit = duration

        data = await self.bot.mute_roles.find(ctx.guild.id)

        if not data or "role_id" not in data:
            await ctx.reply("You haven't set a mute role. Refer to the help command to set a mute role.")
            return

        muted_role_id = data["role_id"]
        muted_role = ctx.guild.get_role(muted_role_id)

        await member.add_roles(muted_role)

        embed = discord.Embed(
            title = 'Muted Member',
            description = 'This task was completed without any errors.',
            colour = self.bot.mod_color
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.display_avatar.url}')
        embed.set_footer(text=f'Invoked by {ctx.author.name}')

        if ctx.guild.icon:
            embed.set_thumbnail(url=f'{ctx.guild.icon.url}')

        embed.add_field(name='Member', value=f'{member}', inline=True)
        embed.add_field(name='Duration', value=f'{amount}{unit}', inline=True)

        await ctx.reply(embed=embed)
        await asyncio.sleep(amount * multiplier[unit])
        await member.remove_roles(muted_role)

    @commands.command(description='Unute a member. Must have set the muterole.')
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member : commands.MemberConverter, *, reason=None):
        data = await self.bot.mute_roles.find(ctx.guild.id)

        if not data or "role_id" not in data:
            await ctx.reply("You haven't set a mute role. Refer to the help command to set a mute role.")
            return

        muted_role_id = data["role_id"]
        muted_role = ctx.guild.get_role(muted_role_id)

        await member.remove_roles(muted_role)

        embed = discord.Embed(
            title = 'Unmuted Member',
            description = 'This task was completed without any errors.',
            colour = self.bot.mod_color
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.display_avatar.url}')
        embed.set_footer(text=f'Invoked by {ctx.author.name}')

        if ctx.guild.icon:
            embed.set_thumbnail(url=f'{ctx.guild.icon.url}')

        embed.add_field(name='Member', value=f'{member}', inline=True)
        embed.add_field(name='Reason', value=f'{reason}', inline=True)

        await ctx.reply(embed=embed)

    @commands.command(aliases=['clear'], description='Purge a certain amount of messages.')
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount : int):
        await ctx.channel.purge(limit = amount + 1)
        await ctx.reply('This task was completed without any errors.', delete_after=5)

    @commands.command(description='Kick a member from the server.')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : commands.MemberConverter, *, reason=None):
        await ctx.guild.kick(member, reason=reason)

        embed = discord.Embed(
            title = 'Kicked Member',
            description = 'This task was completed without any errors.',
            colour = self.bot.mod_color
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.display_avatar.url}')
        embed.set_footer(text=f'Invoked by {ctx.author.name}')

        if ctx.guild.icon:
            embed.set_thumbnail(url=f'{ctx.guild.icon.url}')

        embed.add_field(name='Member', value=f'{member}', inline=True)
        embed.add_field(name='Reason', value=f'{reason}', inline=True)

        await ctx.reply(embed=embed)

    @commands.command(description='Ban a member from the server.')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : commands.UserConverter, *, reason=None):
        await ctx.guild.ban(member, reason=reason)

        embed = discord.Embed(
            title = 'Banned Member',
            description = 'This task was completed without any errors.',
            colour = self.bot.mod_color
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.display_avatar.url}')
        embed.set_footer(text=f'Invoked by {ctx.author.name}')

        if ctx.guild.icon:
            embed.set_thumbnail(url=f'{ctx.guild.icon.url}')

        embed.add_field(name='Member', value=f'{member}', inline=True)
        embed.add_field(name='Reason', value=f'{reason}', inline=True)

        await ctx.reply(embed=embed)

    @commands.command(description='Temporarily ban a member from the server.')
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, member : commands.UserConverter, duration : MXDurationConverter):

        multiplier = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        amount, unit = duration

        await ctx.guild.ban(member)
        embed = discord.Embed(
            title = 'Banned Member',
            description = 'This task was completed without any errors.',
            colour = self.bot.mod_color
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.display_avatar.url}')
        embed.set_footer(text=f'Invoked by {ctx.author.name}')

        if ctx.guild.icon:
            embed.set_thumbnail(url=f'{ctx.guild.icon.url}')

        embed.add_field(name='Member', value=f'{member}', inline=True)
        embed.add_field(name='Duration', value=f'{amount}{unit}', inline=True)

        await ctx.reply(embed=embed)
        await asyncio.sleep(amount * multiplier[unit])
        await ctx.guild.unban(member)

    @commands.command(description='Unban a member from the server.')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member : commands.UserConverter, reason=None):
        await ctx.guild.unban(member, reason=reason)

        embed = discord.Embed(
            title = 'Unbanned Member',
            description = 'This task was completed without any errors.',
            colour = self.bot.mod_color
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.display_avatar.url}')
        embed.set_footer(text=f'Invoked by {ctx.author.name}')

        if ctx.guild.icon:
            embed.set_thumbnail(url=f'{ctx.guild.icon.url}')

        embed.add_field(name='Member', value=f'{member}', inline=True)
        embed.add_field(name='Reason', value=f'{reason}', inline=True)

        await ctx.reply(embed=embed)

    @commands.command(description='Set the server prefix.')
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, *, prefix):
        data = await self.bot.prefixes.find(ctx.guild.id)

        if not data or "prefix" not in data:
            data = {"_id": ctx.guild.id, "prefix": prefix}

        data["prefix"] = prefix
        await self.bot.prefixes.upsert(data)

        await ctx.reply(f"This servers prefix has been changed to | `{prefix}` | enjoy!")

    @commands.command(description='Lock a channel.')
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel : commands.TextChannelConverter = None):
        message = await ctx.reply('Working...')

        if channel is None:
            channel = ctx.channel

        overwrites = {}

        for role in ctx.guild.roles:
            overwrites[role] = discord.PermissionOverwrite(
                send_messages=False
            )

        await channel.edit(overwrites=overwrites, reason=f'Locked channel {channel.name}.')

        await message.edit(content=f'Successfully locked {channel.mention}. Refer to the unlock command to unlock this channel.')

    @commands.command(description='Unlock a channel.')
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel : commands.TextChannelConverter = None):
        message = await ctx.reply('Working...')

        if channel is None:
            channel = ctx.channel

        overwrites = {}

        for role in ctx.guild.roles:
            overwrites[role] = discord.PermissionOverwrite(
                send_messages=True
            )

        await channel.edit(overwrites=overwrites, reason=f'Unlocked channel {channel.name}.')

        await message.edit(content=f'Successfully unlocked {channel.mention}. Refer to the lock command to lock this channel.')

    @commands.group(description='Give a member a role./Take away a members role.', invoke_without_command=True)
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, member : commands.MemberConverter, *, role : MXRoleConverter):
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.reply(f'Removed `{role.name}` from `{member.name}`.')
        else:
            await member.add_roles(role)
            await ctx.reply(f'Gave `{role.name}` to `{member.name}`.')

    @role.command(description='Give everyone in the guild a role.')
    @commands.has_permissions(manage_roles=True)
    async def all(self, ctx, role : MXRoleConverter):
        msg = await ctx.reply('Working...  (This may take a while depending on your server size.)')

        for member in ctx.guild.members:
            try:
                await member.add_roles(role)
            except:
                pass

        await msg.edit(content='Complete!')

    @role.command(name='in', description='Give members in a role another role.')
    @commands.has_permissions(manage_roles=True)
    async def _in(self, ctx, role1 : commands.RoleConverter, role2 : commands.RoleConverter):
        msg = await ctx.reply('Working...  (This may take a while depending on the amount of members in the role.)')

        for member in role1.members:
            try:
                await member.add_roles(role2)
            except:
                pass

        await msg.edit(content='Complete!')

    @commands.group(description='Root command for log management.', invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def log(self, ctx):
        pass

    @log.command(description='Set a logging channel. Logs will not be saved if a channel is not set.')
    @commands.has_permissions(manage_guild=True)
    async def set(self, ctx, channel : commands.TextChannelConverter):
        data = await self.bot.log_channels.find(ctx.guild.id)

        if not data or "channel" not in data:
            data = {"_id": ctx.guild.id, "channel": channel.id}
            await self.bot.log_channels.upsert(data)

        else:
            data["channel"] = channel.id
            await self.bot.log_channels.upsert(data)

        await ctx.reply(f'Congrats! I am now able to log all events to {channel.mention}! If you wish to disable logging refer to the `disable` subcommand in the help command.')

    @log.command(description='Remove logging from the guild.')
    @commands.has_permissions(manage_guild=True)
    async def disable(self, ctx):
        data = await self.bot.log_channels.find(ctx.guild.id)

        if not data or "channel" not in data:
            await ctx.reply('Logging is already disabled in this server.')

        else:
            await self.bot.log_channels.delete(data)
            await ctx.reply('Logging has been disabled. If you ever wish to re-enable it you can refer to the `set` subcommand in the help command.')

def setup(bot):
    bot.add_cog(Mod(bot))
