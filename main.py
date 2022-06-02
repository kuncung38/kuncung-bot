from asyncio import QueueEmpty

import os

from DiscordUserId import *

import nextcord
from nextcord import VoiceState
from nextcord import Interaction
from nextcord.ext import commands

import wavelink
from wavelink.ext import spotify

import datetime

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix= '!', intents=intents)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def reload (ctx: commands.Context):
    if ctx.author.id == kuncung_id or ctx.author.id == owen_id:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                client.reload_extension(f'cogs.{filename[:-3]}')
        print('Cogs Reloaded')
        return await ctx.reply('Refreshed!')
    else:
        return await ctx.reply('Siapa lu reload reload???')


client.run(os.environ["DISCORD_TOKEN"])