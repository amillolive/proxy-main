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

class Mod(commands.Cog, description='Moderation commands. Only mods can use these.'):
    def __init__(self, bot):
        self.bot = bot
        print('Mod Active')

    @commands.command(description='Set the muterole for the guild.')
    @commands.has_permissions(manage_messages=True)
    async def muterole(self, ctx, role : MXRoleConverter):
        data = await self.bot.prefixes.find(ctx.guild.id)

        if not data or "role_id" not in data:
            data = {"_id": ctx.guild.id, "role_id": role.id}

        data["role_id"] = role.id
        await self.bot.prefixes.upsert(data)

        await ctx.reply(f"The mute role has been changed to `{role.mention}`. If you couldn't use the mute commands before, you should be able to now.")

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
            description = f'This task was completed without any errors.',
            colour = discord.Colour.gold()
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_footer(text=f'Invoked by {ctx.author.name}')
        embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
        embed.add_field(name=f'Member', value=f'{member}', inline=True)
        embed.add_field(name=f'Reason', value=f'{reason}', inline=True)

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
            description = f'This task was completed without any errors.',
            colour = discord.Colour.gold()
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_footer(text=f'Invoked by {ctx.author.name}')
        embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
        embed.add_field(name=f'Member', value=f'{member}', inline=True)
        embed.add_field(name=f'Duration', value=f'{amount}{unit}', inline=True)

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
            description = f'This task was completed without any errors.',
            colour = discord.Colour.gold()
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_footer(text=f'Invoked by {ctx.author.name}')
        embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
        embed.add_field(name=f'Member', value=f'{member}', inline=True)
        embed.add_field(name=f'Reason', value=f'{reason}', inline=True)

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
            description = f'This task was completed without any errors.',
            colour = discord.Colour.gold()
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_footer(text=f'Invoked by {ctx.author.name}')
        embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
        embed.add_field(name=f'Member', value=f'{member}', inline=True)
        embed.add_field(name=f'Reason', value=f'{reason}', inline=True)

        await ctx.reply(embed=embed)

    @commands.command(description='Ban a member from the server.')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : commands.UserConverter, *, reason=None):
        await ctx.guild.ban(member, reason=reason)

        embed = discord.Embed(
            title = 'Banned Member',
            description = f'This task was completed without any errors.',
            colour = discord.Colour.gold()
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_footer(text=f'Invoked by {ctx.author.name}')
        embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
        embed.add_field(name=f'Member', value=f'{member}', inline=True)
        embed.add_field(name=f'Reason', value=f'{reason}', inline=True)

        await ctx.reply(embed=embed)

    @commands.command(description='Temporarily ban a member from the server.')
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, member : commands.UserConverter, duration : MXDurationConverter):

        multiplier = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        amount, unit = duration

        await ctx.guild.ban(member)
        embed = discord.Embed(
            title = 'Banned Member',
            description = f'This task was completed without any errors.',
            colour = discord.Colour.gold()
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_footer(text=f'Invoked by {ctx.author.name}')
        embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
        embed.add_field(name=f'Member', value=f'{member}', inline=True)
        embed.add_field(name=f'Duration', value=f'{amount}{unit}', inline=True)

        await ctx.reply(embed=embed)
        await asyncio.sleep(amount * multiplier[unit])
        await ctx.guild.unban(member)

    @commands.command(description='Unban a member from the server.')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member : commands.UserConverter, reason=None):
        await ctx.guild.unban(member, reason=reason)

        embed = discord.Embed(
            title = 'Unbanned Member',
            description = f'This task was completed without any errors.',
            colour = discord.Colour.gold()
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_footer(text=f'Invoked by {ctx.author.name}')
        embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
        embed.add_field(name=f'Member', value=f'{member}', inline=True)
        embed.add_field(name=f'Reason', value=f'{reason}', inline=True)

        await ctx.reply(embed=embed)

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
            colour = discord.Colour.light_grey()
        )

        embed.set_footer(text=f'Invoked by {ctx.author.name}, for {Role}')
        embed.set_author(name=f'{ctx.guild}', icon_url=f'{ctx.guild.icon_url}')

        for member in Role.members:
            total += 1
            try:
                await member.send(embed=embed)
                success += 1
            except:
                fail += 1

        embed = discord.Embed(
            title = 'Task Completed',
            colour = discord.Colour.light_grey()
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.add_field(name=f'Total', value=f'{total}', inline=True)
        embed.add_field(name=f'Success', value=f'{success}', inline=True)
        embed.add_field(name=f'Failed', value=f'{fail}', inline=True)

        await message.edit(embed=embed)

    @commands.command(description='Set the server prefix.')
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, *, prefix):
        data = await self.bot.prefixes.find(ctx.guild.id)

        if not data or "prefix" not in data:
            data = {"_id": ctx.guild.id, "prefix": prefix}

        data["prefix"] = prefix
        await self.bot.prefixes.upsert(data)

        await ctx.reply(f"This servers prefix has been changed to `{prefix}`, enjoy!")

    @commands.command(description='Lock a channel.')
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel : commands.TextChannelConverter = None):
        if channel is None:
            channel = ctx.channel

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(
                send_messages=False
            )
        }
        await channel.edit(overwrites=overwrites, reason=f'Locked channel {channel.name}.')

        await ctx.reply(f'Successfully locked {channel.mention}. Refer to the unlock command to unlock this channel.')

    @commands.command(description='Unlock a channel.')
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel : commands.TextChannelConverter = None):
        if channel is None:
            channel = ctx.channel

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(
                send_messages=True
            )
        }
        await channel.edit(overwrites=overwrites, reason=f'Locked channel {channel.name}.')

        await ctx.reply(f'Successfully unlocked {channel.mention}. Refer to the lock command to lock this channel.')

    @commands.command(description='Give a member a role./Take away a members role.')
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, member : commands.MemberConverter, *, role : MXRoleConverter):
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.reply(f'Removed `{role.name}` from `{member.name}`.')
        else:
            await member.add_roles(role)
            await ctx.reply(f'Gave `{role.name}` to `{member.name}`.')

    @commands.command(description='Set a logging channel. Logs will not be saved if a channel is not set.')
    @commands.has_permissions(manage_guild=True)
    async def logchannel(self, ctx, channel : commands.TextChannelConverter):
        data = await self.bot.log_channels.find(ctx.guild.id)

        if not data or "channel" not in data:
            data = {"_id": ctx.guild.id, "channel": channel.id}
            await self.bot.log_channels.upsert(data)

        else:
            data["channel"] = channel.id
            await self.bot.log_channels.upsert(data)

        await ctx.reply(f'Congrats! I am now able to log all events to {channel.mention}! If you wish to disable logging refer to the command in the help command.')

    @commands.command(description='Remove logging from the guild.')
    @commands.has_permissions(manage_guild=True)
    async def disablelogging(self, ctx):
        data = await self.bot.log_channels.find(ctx.guild.id)

        if not data or "channel" not in data:
            await ctx.reply(f'Logging is already disabled in this server.')

        else:
            await self.bot.log_channels.delete(data)
            await ctx.reply(f'Logging has been disabled.')

def setup(bot):
    bot.add_cog(Mod(bot))
