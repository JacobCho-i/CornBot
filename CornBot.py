#REMINDER: ANOTHER FILE Token.py IS NEEDED TO RUN THIS
import discord
from discord import app_commands
from discord.ext import tasks

import asyncio
import mysql.connector;
import math
import random

from datetime import datetime, time
from Token import TOKEN, guild_id, host, password, name

db = None
cur = None
backup_db = {}

class aclient(discord.Client):
    def __init__(self):
        intent = discord.Intents.all()
        #intent.members = True
        super().__init__(intents=intent)
        self.synced = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id = guild_id))
            self.synced = True
        check_bday.start()
        try:
            db = get_db(database='user_db')
            cur = db.cursor()
        except Exception as e:
            if e.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                db = get_db()
                cur = db.cursor()
                cur.execute("CREATE DATABASE user_db")
                db.commit()
                db.close()
                db = get_db(database='user_db')
                cur = db.cursor()
            else:
                print(e)
        db = db.close()
        setup_db()
        print("successfully logged in!")

def setup_db():
    #TODO: optimize code here
    db = get_db(database = 'user_db')
    query = '''
            SELECT *
            FROM user_db
            '''
    cur = db.cursor()
    try:
        cur.execute(query)
        print(f'cur = {cur}')
    except mysql.connector.Error as e:
        print(e)
        if e.errno == mysql.connector.errorcode.ER_NO_SUCH_TABLE:
            query = '''
                    CREATE TABLE user_db (
                        username VARCHAR(50),
                        userid int PRIMARY KEY,
                        exp int
                    )
                    '''
            cur.execute(query)
            db.commit()
            print('table no exist, so we created one')
    finally:
        print('db closed')
        db.close()
    query = '''
            SELECT *
            FROM backup_servers
            '''
    db = get_db(database = 'user_db')
    cur = db.cursor()
    try:
        cur.execute(query)
        for servers in cur:
            backup_db[f'backup_{servers[0]}'] = servers[1]
    except mysql.connector.Error as e:
        print(e)
        if e.errno == mysql.connector.errorcode.ER_NO_SUCH_TABLE:
            query = '''
                    CREATE TABLE backup_servers (
                        name VARCHAR(50),
                        guild_id BIGINT
                    )
                    '''
            cur.execute(query)
            db.commit()
    finally:
        print('db closed')
        db.close()
    
def get_db(database:str=""):
    """
    This helper function retruns db

    Input: db_name
    outpt: db
    """
    db = None
    if (str == ""):
        db = db = mysql.connector.connect(
                                host = host,
                                user = name,
                                passwd = password)
        return db
    db = mysql.connector.connect(
                                host = host,
                                user = name,
                                passwd = password,
                                database = database)
    return db


client = aclient()
tree = app_commands.CommandTree(client)
id = guild_id

exp = {}
cooldown = {}

@client.event
async def on_message(msg):
    """
    This event observes the user messages and grants the user
    experience which can level up the user. It works depends on 
    time frame upon each message to prevent spam for exp

    Input: msg
    Output: N/A
    """
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

@client.event
async def on_message(msg):
    """
    This event observes incoming messages and if there
    is active backup_server, then leaves the log of 
    each message if it matches with the guild_id provided
    (Purposely made a separate function to distinguish each functions)

    Input: msg
    Output: N/A
    """
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    content = msg.content
    if content:
        print(f'author: {msg.author}, content: {content}, time: {now}, id: {msg.author.id}')
    elif msg.attachments:
        content = msg.attachments[0].url
        print(f'author: {msg.author}, content: {msg.attachments[0].url}, time: {now}, id: {msg.author.id}')
    #elif msg.embeds:
    #    print(msg.embeds)
    for database in backup_db:
        if msg.guild.id != backup_db[database]:
            continue
        db = get_db(database=database)
        cursor = db.cursor()
        query = f"INSERT INTO Message (user, msg, timeStr, msgid, userid) VALUES ('{msg.author}', '{msg.content}', '{now}', '{msg.id}', {msg.author.id})"
        cursor.execute(query)
        db.commit()
        db.close()


def check_levelup(exp):
    """
    This is a helper function used for check_my_level()
    to calculate the current level and progress until 
    the next level.

    Input: exp
    Output: level
    """
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

@tree.command(name="test", guild=discord.Object(id = id))
async def test(intereaction:discord.Interaction, db_name:str):
    """
    dummy command to test some features
    """
    db = get_db(database = f'backup_{db_name}')
    cur = db.cursor()
    query = '''
            SELECT * FROM Message
            '''
    cur.execute(query)
    for msg in cur:
        print(msg)
    db.close()

@tree.command(name="deactivate_backup", guild=discord.Object(id = id))
async def deactivate_backup(interaction:discord.Interaction, db_name:str):
    #TODO: Test this command
    """
    This command deactivates and stop the backup server from
    logging incoming messages

    Input: interaction, db_name
    Output: N/A
    """
    if db_name not in backup_db:
        await interaction.response.send_message('that db does not exist')
        return
    db = get_db(database = 'user_db')
    cur = db.cursor()
    query = f'''
            DELETE FROM backup_servers
            WHERE name = {db_name} AND guild_id = {guild_id}
            '''
    cur.execute(query)
    db.commit()
    db.close()

@tree.command(name="download_backup", guild=discord.Object(id = id))
async def download_backup(interaction:discord.Interaction, db_name: str):
    """
    This command sends a message with txt file attachment that has
    user message logs since the back up was activated

    Input: interaction, db_name
    Output: N/A
    """
    if db_name not in backup_db:
        await interaction.response.send_message('that db does not exist')
        return
    db = get_db(database = f'backup_{db_name}')
    cur = db.cursor()
    query = '''
            SELECT * FROM Message
            '''
    cur.execute(query)
    random_id = random.randint(0,10000000)
    filename = f'server_backup_{db_name}_{random_id}.txt'  # Add file extension
    with open(filename, 'w') as f:
        for msg in cur:
            f.write(f'{msg}\n')
    
    await interaction.response.send_message(
        content='Here is the backup file:',
        file=discord.File(filename)
    )

    f.close()
    db.close()

@tree.command(name="start_backup", 
              description="from now, observe all incoming message and store it on the database until stopped", 
              guild=discord.Object(id = id))
async def start_backup(interaction: discord.Interaction, db_name: str):
    """
    This command activates the backup_server that store all the 
    incoming messages once activated.

    Input: interaction, db_name
    output: N/A
    """
    try:
        db = get_db(database = f'backup_{db_name}')
        cur = db.cursor()
        await interaction.response.send_message('this backup already exists!')
    except Exception as e:
        print(e)
        if e.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print('hi')
            db = get_db()
            cur = db.cursor()
            cur.execute(f"CREATE DATABASE backup_{db_name}")
            print('Created backup database!')
            db.commit()
            db.close()
            asyncio.sleep(2)
            db = get_db(database=f'backup_{db_name}')
            cur = db.cursor()
            cur.execute("""
                            CREATE TABLE Message(
                                user VARCHAR(50),
                                msg VARCHAR(4000),
                                timeStr VARCHAR(30),
                                msgid BIGINT PRIMARY KEY,
                                userid BIGINT)
                        """)
            db.commit()
            db.close()
            db = get_db(database='user_db')
            cur = db.cursor()
            cur.execute(f"""
                            INSERT INTO backup_servers (name, guild_id) VALUES ('{db_name}', '{interaction.guild.id}')
                        """)
            db.commit()
            backup_db[f'backup_{db_name}'] = guild_id
            db.close()
            await interaction.response.send_message('successfully created backup db')
        else:
            await interaction.response.send_message(f'error occured! {e}')
    finally:
        db.close()
        


@tree.command(name="create_vote", description="create a poll", guild=discord.Object(id = id))
async def create_vote(interaction: discord.Interaction, time:int, 
                      prompt: str, option1:str, option2:str, option3:str="",
                      option4:str="", option5:str=""):
    """
    This commands create a poll where user can respond 
    to it by reacting to the message
    
    Input: interaction, time, prompmt, ption1, option2, option3(optional), option4(optional), option5(optional)
    Output: N/A
    """
    guild = client.get_guild(guild_id)
    channel = discord.utils.get(guild.channels, name = 'general')
    general = guild.get_channel(channel.id)
    msg_str = f'{interaction.user.mention} has casteed a poll! Respond to this poll by adding a reaction. This poll lasts for {time} seconds\nPrompt: {prompt} \n'
    msg_str += f"1️⃣: {option1}\n"
    msg_str += f"2️⃣: {option2}\n"
    if option3 != "":
        msg_str += f"3️⃣: {option3}\n"
    if option4 != "":
        msg_str += f"4️⃣: {option4}\n"
    if option5 != "":
        msg_str += f"5️⃣: {option5}\n"
    msg = await general.send(msg_str)
    
    await msg.add_reaction('1️⃣')
    await msg.add_reaction('2️⃣')
    if option3 != "":
        await msg.add_reaction('3️⃣')
    if option4 != "":
        await msg.add_reaction('4️⃣')
    if option5 != "":
        await msg.add_reaction('5️⃣')
    await interaction.response.send_message('poll successfully created!')
    await asyncio.sleep(time)
    msg = await channel.fetch_message(msg.id)
    max = 0
    react = {}
    for reaction in msg.reactions:
        if (reaction.count > max):
            max = reaction.count
            react = {reaction}
        elif reaction.count == max:
            react.add(reaction)
    msg_str = "The vote is ended, the result is "
    msg_str += reaction.emoji
    msg_str += " "
    await general.send(msg_str)

@tree.command(name="lottery", description="randomly selects one user who reacted to the message", guild=discord.Object(id = id))
async def lottery(interaction: discord.Interaction, time: int):
    """
    This commands creates a lottery event and randomly
    selects one user who reacted to the message after given time
    
    Input: interaction, time
    Output: N/A
    """
    guild = client.get_guild(guild_id)
    channel = discord.utils.get(guild.channels, name = 'general')
    general = guild.get_channel(channel.id)
    msg = await general.send(f'{interaction.user.mention} has started a lottery event! React ✅ to this message to participate')
    await msg.add_reaction('✅')
    await interaction.response.send_message('event successfully created!')
    await asyncio.sleep(time)
    msg = await channel.fetch_message(msg.id)
    react_users = []
    
    for reaction in msg.reactions:
        if reaction.emoji == '✅':
            async for user in reaction.users():
                react_users.append(user)
    
    num = random.randint(0, len(react_users) - 1)
    await general.send(f'Congratualtion!, {react_users[num].mention} has won the lottery event!')

@tree.command(name="check_my_level", description="shows what level you are in this server", guild=discord.Object(id = id))
async def check_my_level(interaction: discord.Interaction):
    """
    This commands lets the user know how far they are in 
    their progress towards the next level

    Input: Interaction
    Output: N/A
    """
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

    Input: interaction
    Output: N/A
    """
    await interaction.response.send_message("Hi this is corn bot with some cool functionalities:\nHere is some commands to try:\n.coin \n.dice\nYou can visit (https://github.com/JacobCho-i/CornBot/blob/main/README.md) for a document with full commands!\n")
    await interaction.response.send_message("")

@tree.command(name="coin", description="flip a coin and sends the results", guild=discord.Object(id = id))
async def coin(interaction: discord.Interaction):
    """
    This command is a command to flip a coin and sends the results [HEAD/TAIL]

    Input: interaction
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

    Input: interaction
    Output: N/A
    """
    rand = random.randint(1, 6)
    await interaction.response.send_message(f'You rolled {rand}!')

@tree.command(name="roll", description="generate a number between 1 to [arg] (Inclusive)", guild=discord.Object(id = id))
async def roll(interaction: discord.Interaction, arg:int):
    """
    This command is a command to generate a number between 1 to [arg] (Inclusive)

    Input: interaction
    Output: N/A
    """
    rand = random.randint(1, arg)
    await interaction.response.send_message(f'You rolled {rand}!')

@tree.command(name="remind", description="send [msg] after [time] seconds with a user ping", guild=discord.Object(id = id))
async def remind(interaction: discord.Interaction, time:int, *, msg: str):
    """
    This command is a command to send [msg] after [time] seconds with a user ping

    Input: interaction, time, msg
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

    Input: interaction, time, member, msg
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

    Input: interaction, month, day, user
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

    Input: interaction, month, day, user
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

    Input: interaction, error
    Output: N/A
    """
    await ctx.send('You have entered wrong parameters! Right format:')
    await ctx.send('.set_bday *MONTH* *DAY* *USER*')

client.run(TOKEN)