#REMINDER: ANOTHER FILE Token.py IS NEEDED TO RUN THIS
import discord
from discord import app_commands
from discord.ext import tasks

import asyncio
import math
import random

from datetime import datetime, time 
from Token import TOKEN, guild_id


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

exp = {}
cooldown = {}

@client.event
async def on_message(msg):
    if msg.author.bot:
        return
    if msg.author.id in cooldown:
        if cooldown[msg.author.id] == 1:
            return
    if msg.author.id in exp:
        exp[msg.author.id] = exp[msg.author.id] + 1
    else:
        exp[msg.author.id] = 1
    cooldown[msg.author.id] = 1
    lvl = check_levelup(exp[msg.author.id])
    if lvl < 0:
        guild = client.get_guild(guild_id)
        channel = discord.utils.get(guild.channels, name = 'general')
        general = guild.get_channel(channel.id)
        try:
            role = discord.utils.get(guild.roles, name='level 1-10')
            if lvl > 10 and lvl <= 20:
                role = discord.utils.get(guild.roles, name='level 11-20')
            if lvl > 20 and lvl <= 30:
                role = discord.utils.get(guild.roles, name='level 21-30')
            if role is not None:
                await msg.author.add_roles(role)
            else:
                if lvl > 0 and lvl <= 10:
                    new_role = await guild.create_role(name='level 1-10')
                    await msg.author.add_roles(new_role)
                if lvl > 10 and lvl <= 20:
                    new_role = await guild.create_role(name='level 11-20')
                    await msg.author.add_roles(new_role)
                if lvl > 20 and lvl <= 30:
                    new_role = await guild.create_role(name='level 21-30')
                    await msg.author.add_roles(new_role)
                
            await general.send(f'{msg.author.mention} has leveled up to {-1 * lvl}!')
        except Exception as e:
            general.send('Please give me a permission to create/assign roles in server setting/role!')

    await asyncio.sleep(30)
    print(f'{msg.author.mention}s cooldown reset!')
    cooldown[msg.author.id] = 0

def check_levelup(exp):
    level = 0
    while exp > 0:
        formula = int(3 * math.pow(level, 1.4))
        if formula == 0:
            formula = 3
        exp -= formula
        if exp > 0: 
            level += 1
        elif exp == 0:
            level += 1
            level *= -1
            break
    return level


@tree.command(name="check_my_level", description="shows what level you are in this server", guild=discord.Object(id = id))
async def check_my_level(interaction: discord.Interaction):
    if interaction.user.id in exp:
        experience = exp[interaction.user.id]
        level = 0
        while experience > 0:
            formula = int(3 * math.pow(level, 1.4))
            if formula == 0:
                formula = 3
            if formula > experience:
                break
            experience -= formula
            if experience >= 0: 
                level += 1
            
        await interaction.response.send_message(f"your level is {level} and {(experience / formula) * 100 : .2f}% towards the next level", ephemeral=True)
    else:
        await interaction.response.send_message(f"your level is level 0.", ephemeral=True)
    

@tasks.loop(seconds=10)
async def check_bday():
    """
    This task runs in loop to send congratulation msg if time is 00:00 
    and today is birthday of any users registered in the 'general' channel

    Input: N/A
    Output: N/A
    """
    time = datetime.now()
    guild = client.get_guild(guild_id)
    try:
        for id in birthdays:
            user = await client.fetch_user(id)
            member = guild.get_member(user.id)
            if guild:
                if member:
                    bday = birthdays[id]
                    if (time.month == bday.month and time.day == bday.day):
                        if (time.hour == 1 and time.minute == 1 and time.second < 10):
                            channel = discord.utils.get(guild.channels, name = 'general')
                            general = guild.get_channel(channel.id)
                            await general.send(f'happy birthday to {member.mention}!')
            else:
                print('guild does not exist')
    except Exception as e:
        print(e)

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