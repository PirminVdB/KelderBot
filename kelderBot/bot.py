# bot.py
import os
import random
import json

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Steam game price
# https://api.steampowered.com/ISteamApps/GetAppList/v2/
# https://store.steampowered.com/api/appdetails?appids=57690

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
JSON = os.getenv('JSON_FILENAME')
GAMES = os.getenv('JSON_GAMESNODENAME')

bot = commands.Bot(command_prefix='!')
with open(JSON) as gamesfile:
    data = json.load(gamesfile)

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@roll.error
async def roll_error(ctx, error):
    #https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#ext-commands-api-errors
    await ctx.send('kloters')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please select 2 numbers')

@bot.command(name='slap', help='slap someone in da face')
async def slap(ctx, members: commands.Greedy[discord.Member], *, reason='no reason'):
    slapped = " and ".join(x.name for x in members)
    await ctx.send('{} just got slapped for {}'.format(slapped, reason))

@bot.command(name='addgame', help='add a game to the list')
async def addgame(ctx, name):
    data[GAMES].append(name)
    with open(JSON, "w") as gamesfile:
        json.dump(data, gamesfile)
    await ctx.send('{} was added to the games'.format(name))

@bot.command(name='pickgame', help='picks a random game')
async def pickgame(ctx):
    await ctx.send(random.choice(data[GAMES]))

@bot.command(name='gameslist', help='list the available games')
async def gameslist(ctx):
    await ctx.send(data[GAMES])

bot.run(TOKEN)
