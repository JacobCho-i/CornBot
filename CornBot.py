#REMINDER: ANOTHER FILE Token.py IS NEEDED TO RUN THIS
import discord
from discord.ext import commands

import random
import asyncio
import Token

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='.', intents=intents)
@client.event
async def on_ready():
    print("hi I am online")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, I didn't understand that command.")
    else:
        print(f"Error: {error}")

@client.command()
async def corn(ctx):
    await ctx.send("Hi this is corn bot with some goated functionality:")
    await ctx.send("Here is some commands to try:\n -.coin \n -.dice\n -.roll")

@client.command()
async def coin(ctx):
    rand = random.randint(0,1)
    if (rand == 0):
        await ctx.send("coin is on the head!")
    else:
        await ctx.send("coin is on the tail!")

@client.command()
async def dice(ctx):
    rand = random.randint(1, 6)
    await ctx.send(f'You rolled {rand}!')

@client.command()
async def roll(ctx, arg):
    rand = random.randint(1, int(arg))
    await ctx.send(f'You rolled {rand}!')

@roll.error
async def roll_error(ctx, error):
    if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You have entered wrong parameters! Right format:')
        await ctx.send('.roll *MAX_NUMBER*')
    else:
        await ctx.send('Please enter a number!')

@client.command()
async def remind(ctx, time:int, *, msg: str):
    id = ctx.message.author.mention
    await asyncio.sleep(time)
    for i in range(3):
        await ctx.send(f"{id} {msg}!")

@remind.error
async def remind_error(ctx, error):
    #if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You have entered wrong parameters! Right format:')
        await ctx.send('.remind *SECONDS* *MESSAGE*')

@client.command()
async def remind_to(ctx, time:int, member:discord.Member, *, msg: str):
    id = member.mention
    await asyncio.sleep(time)
    for i in range(3):
        await ctx.send(f"{id} {msg}!")

@remind_to.error
async def remind_to_error(ctx, error):
    #if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You have entered wrong parameters! Right format:')
        await ctx.send('.remind_to *SECONDS* *USER* *MESSAGE*')

client.run(Token.TOKEN)