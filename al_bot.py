# This example requires the 'message_content' intent.

import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

class ALBotClient(discord.Client):
    """
    1. A person starts a ticket with Ticket Bot (this bot already exists) and fills out the info about their AL game so that it creates a message with a standardized format for the AL Bot to read
    2. AL Bot then posts a signup message in the <#1559251308857397309> channel with the info provided
    3. AL Bot creates a temporary role with title of the game
    4. AL Bot creates a temporary text channel with the title of the game that only the people with the role have access to
    5. AL Bot creates a temporary text channel with the title of the game that only the people with the role have access to
    6. AL Bot gives the DM (the person who made the ticket) the temp session role
    7. AL Bot runs a command through Reaction Role Bot (this already exists) to add a reaction role to its sign up message with the temp session role
    8. After a number of users equal to the max player count plus 1 (to account for the DM) have the temp role, AL Bot edits the message to say at the bottom “GAME FULL!”
    9. After a number of users equal to the max player count plus 1 (to account for the DM) have the temp role, AL Bot uses Reaction Role Bot to delete the reaction role
    10. After a number of user equal to the max player count plus 1 (to account for the DM) have the temp role, AL Bot removes the reactions from the message
    11. On the start time of the game, AL Bot pings the temp role in the temp channel with the message “Game starting now!”
    12. After 24 hours have passed since the Game Start, AL Bot deletes the text channel
    13. After 24 hours have passed since the Game Start, AL Bot deletes the voice channel
    14. After 24 hours have passed since the Game Start, AL Bot deletes the role
    15. After 24 hours have passed since the Game Start, AL Bot deletes the sign up message
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.msg = ""
        self.message_count = 0
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()


    async def on_ready(self):
        print(f'Logged on as {self.user}!')   

    #@client.event
    async def on_message(message):
        pass

    async def process_deliver(self):
        pass

    async def send_messages(self, to_what):
        pass

    async def on_message(self, message):
        print(f'Message from {message.author.id}: {message.content}')

client=ALBotClient(intents=intents)

@client.tree.command(name='create-session',description='Creates a session for AL')
@app_commands.describe(session_name='The name of the session', max_players='The maximum number of players for a session', start_time='The date and time when the session will start')
async def createSession(interaction: discord.Interaction, session_name: str, max_players: int, start_time: app_commands.Timestamp):
    await interaction.response.send_message(f'Test {session_name} {max_players} {start_time}')



client.run(os.environ['TOKEN'])
