# CornBot
CornBot is a Discord bot that has various helpful functionalities with fun interactions.

CornBot can...
- flip a coin
- roll a dice
- create random number between intervals
- remind you or other users some message after cerain seconds
- congratulate user's birthday
- grants the user exp based on their activities in the server
- casts a poll to survey users' opinion
- create a lottery events where it randomly selects a participant

# Commands
## /corn:
Format: /corn <br/>
Basic command to see what cornbot can do!

## /coin
Format: /coin <br/>
Command to flip a coin and sends the results [HEAD/TAIL]

## /dice
Format: /dice <br/>
Command to roll a dice with 6 sides

## /roll
Format: /roll [MAX_NUM] <br/>
Command to generate a number between 1 to [MAX_NUM] (Inclusive)

## /remind
Format: /remind [TIME] [MESSAGE] <br/>
Command to send [MESSAGE] after [TIME] seconds with a user ping

## /remind_to
Format: /remind_to [TIME] [USER] [MESSAGE] <br/>
Command to send [MESSAGE] to [USER] with a user ping after [TIME] seconds

## /set_bday
Format: /set_bday [MONTH] [DAY] [USER] <br/> 
Command to register a birthday for [USER]. If time is 00:00 and there is a birthday registered in for a user, the bot sends the congratulation message.

## /remove_bday
Format: /remove_bday [USER] <br/>
Command to remove registered birthday for [USER]

## /create_vote
Format: /create_vote [TIME] [PROMPT] [OPTION1] [OPTION2] [OPTION3?] [OPTION4?] [OPTION5?]<br/>
Commands to cast a poll where user can respond by reacting to the message. It ends after[TIME]

## /check_my_level
Format: /check_my_level
Commands to let the user know how far they are in the progress towards to the next level <br/>

## /lottery
Format: /lottery [TIME] <br/>
Command to create a lottery event where it randomly selects a user who reacted to the message

## /start_backup
Format: /start_backup [NAME] <br/>
Command to create and activate backup and leaves the log for incoming messages

## /deactivate_backup
Format: /deactivate_backup [NAME] <br/>
Command to deactivate and stop the backup server from logging incoming message

## /download_backup
Format: /download_backup [NAME] <br/>
Command to create a txt.file with all of the logs stored in the backup database