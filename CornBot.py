#REMINDER: ANOTHER FILE Token.py IS NEEDED TO RUN THIS
import discord
from discord import app_commands
from discord.ext import tasks

import random
import asyncio
from Token import TOKEN, guild_id
from datetime import datetime, time 

class aclient(discord.Client):
    def __init__(self):
        intent = discord.Intents.default()
        intent.members = True
        super().__init__(intents=intent)
        
        self.synced = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id = guild_id))
            self.synced = True
        check_bday.start()
        print("successfully logged in!")

client = aclient()
tree = app_commands.CommandTree(client)
id = guild_id

@tasks.loop(seconds=10)
async def check_bday():
    time = datetime.now()
    guild = client.get_guild(guild_id)
    for id in birthdays:
        user = await client.fetch_user(id)
        member = guild.get_member(user.id)
        if guild:
            if member:
                bday = birthdays[id]
                if (time.month == bday.month and time.day == bday.day):
                    if (time.hour == 2 and time.minute == 35):
                        channel = guild.get_channel(928447198746804265)
                        await channel.send(f'happy birthday @{member}')
            else:
                print('owo')
        else:
            print('guild does not exist')
@tree.command(name="corn", description="prints out what this bot does", guild=discord.Object(id = id))
async def corn(interaction: discord.Interaction):
    """
    This command is a basic command to see what cornbot can do

    Input: ctx
    Output: N/A
    """
    await interaction.response.send_message("Hi this is corn bot with some cool functionalities:\nHere is some commands to try:\n.coin \n.dice\nYou can visit (https://github.com/JacobCho-i/CornBot/blob/main/README.md) for a document with full commands!\n")
    await interaction.response.send_message("")

@tree.command(name="coin", description="flip a coin and sends the results", guild=discord.Object(id = id))
async def coin(interaction: discord.Interaction):
    """
    This command is a command to flip a coin and sends the results [HEAD/TAIL]

    Input: ctx
    Output: N/A
    """
    rand = random.randint(0,1)
    if (rand == 0):
        await interaction.response.send_message("coin is on the head!")
    else:
        await interaction.response.send_message("coin is on the tail!")

@tree.command(name="dice", description="roll a dice with 6 sides", guild=discord.Object(id = id))
async def dice(interaction: discord.Interaction):
    """
    This command is a command to roll a dice with 6 sides

    Input: ctx
    Output: N/A
    """
    rand = random.randint(1, 6)
    await interaction.response.send_message(f'You rolled {rand}!')

@tree.command(name="roll", description="generate a number between 1 to [arg] (Inclusive)", guild=discord.Object(id = id))
async def roll(interaction: discord.Interaction, arg:int):
    """
    This command is a command to generate a number between 1 to [arg] (Inclusive)

    Input: ctx
    Output: N/A
    """
    rand = random.randint(1, arg)
    await interaction.response.send_message(f'You rolled {rand}!')

@tree.command(name="remind", description="send [msg] after [time] seconds with a user ping", guild=discord.Object(id = id))
async def remind(interaction: discord.Interaction, time:int, *, msg: str):
    """
    This command is a command to send [msg] after [time] seconds with a user ping

    Input: ctx, time, msg
    Output: N/A
    """
    
    id = interaction.user.mention
    await asyncio.sleep(time)
    for i in range(3):
        await interaction.response.send_message(f"{id} {msg}!")

@tree.command(name="remind_to", description="send [msg] to [member] with a user ping after [time] seconds", guild=discord.Object(id = id))
async def remind_to(interaction: discord.Interaction, time:int, member:discord.Member, *, msg: str):
    """
    This command is a command to send [msg] to [member] with a user ping after [time] seconds

    Input: ctx, time, member, msg
    Output: N/A
    """
    id = member.mention
    await asyncio.sleep(time)
    for i in range(3):
        await interaction.response.send_message(f"{id} {msg}!")

birthdays = {}

@tree.command(name="set_bday", description="register a user's birthday", guild=discord.Object(id = id))
async def set_bday(interaction: discord.Interaction, month:int, day:int, user:discord.Member):
    """
    This command is a command to register a user's birthday

    Input: ctx, month, day, user
    Output: N/A
    """
    date_str = f'{month}/{day}'
    bday = datetime.strptime(date_str, '%m/%d').date()
    birthdays[user.id] = bday
    await interaction.response.send_message(f"Successfully set {user.mention}'s birthday!")

@tree.command(name="remove_bday", description="remove registered user's birthday", guild=discord.Object(id = id))
async def remove_bday(interaction: discord.Interaction, user:discord.Member):
    """
    This command is a command to remove registered user's birthday

    Input: ctx, month, day, user
    Output: N/A
    """
    if user.id in birthdays:
        del birthdays[user.id]
        await interaction.response.send_message(f"Successfully removed {user.mention}'s birthday!")
    else:
        await interaction.response.send_message("This user's birthday is not registered!")
        return 

@tree.command(name="check", description="check bday functionality", guild=discord.Object(id = id))
async def check(interaction: discord.Interaction, user:discord.Member):
    """
    This is prototype function to check bday functionality

    Input: ctx, user
    Output: N/A
    """
    for date in birthdays:
        print(date)
        print(birthdays[date])
    now = datetime.now()
    if user.id in birthdays:
        bday = birthdays[user.id]
        if (bday.month == now.month and bday.day == now.day):
            await interaction.response.send_message(f"happy birthday to {user.mention}!")
        else:
            await interaction.response.send_message("no birthday today")
    else:
        await interaction.response.send_message("This user's birthday is not registered!")

@check.error
async def check_error(ctx, error):
    print(error)

@set_bday.error
async def bday_error(ctx, error):
    """
    This function handles the error caused in .remind_to command

    Input: ctx, error
    Output: N/A
    """
    await ctx.send('You have entered wrong parameters! Right format:')
    await ctx.send('.set_bday *MONTH* *DAY* *USER*')

client.run(TOKEN)