# This example requires the 'message_content' intent.

import os
import re

from discord import client
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

    async def create_session(self, sender, title, description, max_players, start_time):
        server = sender.guild

        post_schema = {
            # role id
            # text channel id
            # voice channel id
        }

        # Creates a temporary role
        role = await self.create_session_role(server=server, title=title)
        post_schema["role"] = role.id

        # Creates a temporary category
        category = await self.create_session_category(server=server, role=role, title=title)
        post_schema["category"] = category.id

        # Creates a temporary text channel
        text_channel = await self.create_session_text_channel(server=server, category=category, title=title)
        post_schema["text"] = text_channel.id

        # Creates a temporary voice channel
        voice_channel = await self.create_session_voice_channel(server=server, category=category, title=title)
        post_schema["voice"] = voice_channel.id

        await sender.add_roles(role)

        await self.send_session_signup_message(dm=sender, title=title, description=description, max_players=max_players, start_time=start_time, role=role, text_channel=text_channel, voice_channel=voice_channel)

        return post_schema

    async def on_message(self, message: discord.Message):
        print("Message:", message.content)
        if message.content.startswith("$test"):
            schema = await self.create_session(message.author, "Test Title", "This is a test", 6, datetime.now())
            print("Schema: ", schema)
        print(f'Logged on as {self.user}!')

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reactor = await self.fetch_user(payload.user_id)
        server = await self.fetch_guild(payload.guild_id)
        role = await server.fetch_role((await self.extract_var(message=message, var_name="Role"))[3:-1])
        member = await server.fetch_member(payload.user_id)
        dm = await self.fetch_user((await self.extract_var(message=message, var_name="DM"))[2:-1])

        if message.author == self.user and reactor != self.user and message.content.endswith("\nPlease react to this message with ✅ to sign up.") and payload.emoji.name=="✅":
            if reactor == dm:
                await message.remove_reaction(emoji="✅",member=reactor)
                await reactor.send(f"You are the DM, you cannot play your own game.")
            else:
                substring_1 = message.content[message.content.index("\nCurrent Players (")+18:]
                current_player_count = int(substring_1[:substring_1.index("/")])
                max_players = int(await self.extract_var(message=message, var_name="Max Players"))
                title = await self.extract_var(message=message, var_name="Title")

                if current_player_count < max_players:
                    for i in range(current_player_count+1):
                        substring_2 = substring_1[substring_1.index("\n")+1:]
                    new_message = message.content[:-len(substring_1)]+str(current_player_count+1)+substring_1[substring_1.index("/"):-len(substring_2)] + f"- {reactor.mention}\n"+substring_2

                    await message.edit(content=new_message)
                    await reactor.send(f"Joined {title}.")
                    await member.add_roles(role)
                else:
                    await message.remove_reaction(emoji="✅",member=reactor)
                    await reactor.send(f"{title} is full!")

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reactor = await self.fetch_user(payload.user_id)
        server = await self.fetch_guild(payload.guild_id)
        role = await server.fetch_role((await self.extract_var(message=message, var_name="Role"))[3:-1])
        member = await server.fetch_member(payload.user_id)
        dm = await self.fetch_user((await self.extract_var(message=message, var_name="DM"))[2:-1])

        if message.author == self.user and reactor != self.user and reactor != dm and message.content.endswith("\nPlease react to this message with ✅ to sign up.") and payload.emoji.name=="✅":
            substring_1 = message.content[message.content.index("\nCurrent Players (")+18:]
            current_player_count = int(substring_1[:substring_1.index("/")])
            title = await self.extract_var(message=message, var_name="Title")

            if substring_1.find(reactor.mention)!=-1:
                substring_2 = substring_1[substring_1.find(reactor.mention)-2:]
                substring_3 = substring_2[substring_2.index("\n")+1:]
                new_message = message.content[:-len(substring_1)]+str(current_player_count-1)+substring_1[substring_1.index("/"):-len(substring_2)] + substring_3

                await message.edit(content=new_message)
                await reactor.send(f"Left {title}.")
                await member.remove_roles(role)


    async def process_deliver(self):
        pass

    async def send_messages(self, to_what):
        pass

    # Cleans a title for discord's particular format
    async def clean_title(self, title):
        cleaned_title = title
        cleaned_title = re.sub(r'[^a-zA-Z0-9]', '', cleaned_title)
        cleaned_title = "-".join([i.lower() for i in title.split(" ")])

        return cleaned_title

    # Creates a session role
    async def create_session_role(self, server, title):
        seed = hash(title)
        role = await server.create_role(
            name="Player (" + title + ")",
            colour=discord.Colour.random(seed=seed),
            hoist=False,
            reason="Created an AL session"
        )

        return role
    
    # Creates a session category
    async def create_session_category(self, server, role, title):
        category = await server.create_category(
            name=title,
            position=1
        )

        await category.set_permissions(server.default_role, view_channel=False)
        await category.set_permissions(role, view_channel=True)
        await category.set_permissions(self.user, view_channel=True)
        
        return category

    # Creates a session text channel
    async def create_session_text_channel(self, server, category, title):
        text_channel = await server.create_text_channel(
            name = await self.clean_title(title=title),
            category=category,
            position=1,
            topic="Text channel for the " + title + " session"
        )

        return text_channel

    # Creates a session voice channel
    async def create_session_voice_channel(self, server, category, title):
        voice_channel = await server.create_voice_channel(
            name=title + " Voice",
            category=category,
            position=1
        )

        return voice_channel

    async def extract_var(self, message, var_name):
        substring = message.content[message.content.index(var_name+": ")+len(var_name)+2:]
        substring = substring[:substring.index("\n")]
        return substring
    
    # Sends a message for when a session begins
    async def send_session_signup_message(self, dm, title, description, max_players, start_time, role, text_channel, voice_channel):
        game_channel = discord.utils.get(dm.guild.channels, name="al-games")
        message = await game_channel.send(f"DM: {dm.mention}\nTitle: {title}\nDescription: {description}\nMax Players: {max_players} \nStart Time: <t:{int(start_time.timestamp())}:F>\n\nRole: {role.mention}\nText Channel: {text_channel.mention}\nVoice Channel: {voice_channel.mention}\n\nCurrent Players (0/{max_players}):\n\nPlease react to this message with ✅ to sign up.")
        await message.add_reaction("✅")

client = ALBotClient(intents=intents)

@client.tree.command(name='create-session',description='Creates a session for AL')
@app_commands.describe(title='The title of the session', description='The description of the session', max_players='The maximum number of players for a session', start_time='The date and time when the session will start')
async def create_session(interaction: discord.Interaction, title: str, description: str, max_players: int, start_time: app_commands.Timestamp):
    await client.create_session(sender=interaction.user, title=title, description=description, max_players=max_players, start_time=start_time)
    await interaction.response.send_message(f"Session created successfully!", ephemeral=True)

client.run(os.environ['TOKEN'])
