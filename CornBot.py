#REMINDER: ANOTHER FILE Token.py IS NEEDED TO RUN THIS
import discord
from discord.ext import commands

import random
import asyncio
import Token
from datetime import datetime, time 

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='.', intents=intents)
@client.event
async def on_ready():
    """
    This function is called upon the bot successfully logs in

    Input: N/A
    Output: N/A
    """
    print("hi I am online")

@client.event
async def on_command_error(ctx, error):
    """
    This function is called upon the bot encounters error with commands

    Input: ctx, error
    Output: N/A
    """
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, I didn't understand that command.")
    else:
        print(f"Error: {error}")

@client.command()
async def corn(ctx):
    """
    This command is a basic command to see what cornbot can do

    Input: ctx
    Output: N/A
    """
    await ctx.send("Hi this is corn bot with some cool functionalities:\nHere is some commands to try:\n.coin \n.dice\n")
    await ctx.send("You can visit [this link](https://github.com/JacobCho-i/CornBot/blob/main/README.md) for a document with full commands!")

@client.command()
async def coin(ctx):
    """
    This command is a command to flip a coin and sends the results [HEAD/TAIL]

    Input: ctx
    Output: N/A
    """
    rand = random.randint(0,1)
    if (rand == 0):
        await ctx.send("coin is on the head!")
    else:
        await ctx.send("coin is on the tail!")

@client.command()
async def dice(ctx):
    """
    This command is a command to roll a dice with 6 sides

    Input: ctx
    Output: N/A
    """
    rand = random.randint(1, 6)
    await ctx.send(f'You rolled {rand}!')

@client.command()
async def roll(ctx, arg):
    """
    This command is a command to generate a number between 1 to [arg] (Inclusive)

    Input: ctx
    Output: N/A
    """
    rand = random.randint(1, int(arg))
    await ctx.send(f'You rolled {rand}!')

@roll.error
async def roll_error(ctx, error):
    """
    This function handles the error caused in .roll command

    Input: ctx, error
    Output: N/A
    """
    if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You have entered wrong parameters! Right format:')
        await ctx.send('.roll *MAX_NUMBER*')
    else:
        await ctx.send('Please enter a number!')

@client.command()
async def remind(ctx, time:int, *, msg: str):
    """
    This command is a command to send [msg] after [time] seconds with a user ping

    Input: ctx, time, msg
    Output: N/A
    """
    id = ctx.message.author.mention
    await asyncio.sleep(time)
    for i in range(3):
        await ctx.send(f"{id} {msg}!")

@remind.error
async def remind_error(ctx, error):
    """
    This function handles the error caused in .remind command

    Input: ctx, error
    Output: N/A
    """
    await ctx.send('You have entered wrong parameters! Right format:')
    await ctx.send('.remind *SECONDS* *MESSAGE*')

@client.command()
async def remind_to(ctx, time:int, member:discord.Member, *, msg: str):
    """
    This command is a command to send [msg] to [member] with a user ping after [time] seconds

    Input: ctx, time, member, msg
    Output: N/A
    """
    id = member.mention
    await asyncio.sleep(time)
    for i in range(3):
        await ctx.send(f"{id} {msg}!")

@remind_to.error
async def remind_to_error(ctx, error):
    """
    This function handles the error caused in .remind_to command

    Input: ctx, error
    Output: N/A
    """
    await ctx.send('You have entered wrong parameters! Right format:')
    await ctx.send('.remind_to *SECONDS* *USER* *MESSAGE*')

@client.command()
async def set_bday(ctx, month:int, day:int, user:discord.Member):
    """
    This command is a command to set a message planned in 00:00 (in current user's timezone)
    at [month]/[day] to congratulate [user]'s birthday with everyone ping

    Input: ctx, month, day, user
    Output: N/A
    """
    now = datetime.now()


@client.command()
async def congratulate_bday(ctx):
    await ctx.send(f"@everyone it is goyang's birthday! Happy Birthday!")

@client.command()
async def set_bday_utc(ctx, month:int, day:int, del_UTC:int, user:discord.Member):
    """
    This command is a command to set a message planned in 00:00 (in timezone UTC-[delUTC])
    at [month]/[day] to congratulate [user]'s birthday with everyone ping

    Input: ctx, month, day, del_UTC, user
    Output: N/A
    """
    now = datetime.utcnow()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

@set_bday.error
async def bday_error(ctx, error):
    """
    This function handles the error caused in .remind_to command

    Input: ctx, error
    Output: N/A
    """
    await ctx.send('You have entered wrong parameters! Right format:')
    await ctx.send('.set_bday *MONTH* *DAY* *USER*')

async def bday_check():
    await client.wait_until_ready() 
    while True:
        now = datetime.now().time()
        target_time = time(hour=1, minute=19, second=30)
        if now >= target_time:
            cmd = client.get_command('congratulate_bday')
            ctx = await client.get_context(message=None, cls=discord.ext.commands.Context)
            await cmd.invoke(ctx)
            target_time += datetime.timedelta(days=1)
        await asyncio.sleep(60) 

client.loop.create_task(bday_check())

client.run(Token.TOKEN)