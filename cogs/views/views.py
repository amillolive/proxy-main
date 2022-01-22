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
import json
import requests

class InviteView(discord.ui.View):
    def __init__(self):
        super().__init__()

        load_dotenv(dotenv_path="./.env")
        invite_link = os.getenv('INVITE_LINK')

        self.add_item(discord.ui.Button(label="Invite Me!", url=invite_link))

class SpotifyView(discord.ui.View):
    def __init__(self, ctx, member, timeout = 180.0):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.member = member
        try:
            self.add_item(discord.ui.Button(label="Spotify Link!", url=member.activities[1].track_url))
        except:
            self.add_item(discord.ui.Button(label="Spotify Link!", url=member.activity.track_url))

    @discord.ui.button(label='More Info!', style=discord.ButtonStyle.primary)
    async def SpotifyButton(self, button: discord.ui.Button, interaction: discord.Interaction):
        button.style = discord.ButtonStyle.secondary
        button.disabled = True
        await interaction.message.edit(view=self)
        try:
            embed = discord.Embed(
                colour = self.member.activities[1].colour,
                title = 'Activity Information',
                description = "This task was completed without any errors."
            )
            embed.timestamp = discord.utils.utcnow()
            embed.set_footer(text=f'Invoked by {self.ctx.author.name}')
            embed.set_author(name=f'{self.member}', icon_url=f'{self.member.display_avatar.url}')
            embed.set_thumbnail(url=f'{self.ctx.bot.user.display_avatar.url}')
            embed.set_image(url=f'{self.member.activities[1].album_cover_url}')
            embed.add_field(name='Activity', value='Spotify', inline=False)

            artist_count = 0

            for artist in self.member.activities[1].artists:
                artist_count += 1
                embed.add_field(name='Artist' + '-' + f'{artist_count}', value=f'{artist}', inline=False)

            embed.add_field(name='Song', value=f'{self.member.activities[1].title}', inline=False)
            embed.add_field(name='Album', value=f'{self.member.activities[1].album}', inline=False)

            button.style = discord.ButtonStyle.success
            await interaction.message.edit(view=self)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        except:
            embed = discord.Embed(
                colour = self.member.activity.colour,
                title = 'Activity Information',
                description = "This task was completed without any errors."
            )
            embed.timestamp = discord.utils.utcnow()
            embed.set_footer(text=f'Invoked by {self.ctx.author.name}')
            embed.set_author(name=f'{self.member}', icon_url=f'{self.member.display_avatar.url}')
            embed.set_thumbnail(url=f'{self.ctx.bot.user.display_avatar.url}')
            embed.set_image(url=f'{self.member.activity.album_cover_url}')
            embed.add_field(name='Activity', value='Spotify', inline=False)

            artist_count = 0

            for artist in self.member.activity.artists:
                artist_count += 1
                embed.add_field(name='Artist' + '-' + f'{artist_count}', value=f'{artist}', inline=False)

            embed.add_field(name='Song', value=f'{self.member.activity.title}', inline=False)
            embed.add_field(name='Album', value=f'{self.member.activity.album}', inline=False)

            button.style = discord.ButtonStyle.success
            await interaction.message.edit(view=self)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

class GitHubView(discord.ui.View):
    def __init__(self):
        super().__init__()

        join_link = 'https://github.com/signup'
        repo_link = 'https://github.com/mxze16/proxy-main/issues'

        self.add_item(discord.ui.Button(label="Create Account", url=join_link))
        self.add_item(discord.ui.Button(label="Report Bug", url=repo_link))
