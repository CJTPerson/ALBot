# This example requires the 'message_content' intent.

import os
import datetime
import re

from discord import client
from dotenv import load_dotenv

load_dotenv()

import discord

intents = discord.Intents.default()
intents.message_content = True

SERVER_ID = 1554286737931370566
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

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        """
        print("Fetching guild information...")
        server = await client.fetch_guild(server_id)
        print("Fetching guild channels...")
        channels = await server.fetch_channels()
        print("Aliasing channel names...")
        for channel in channels:
            if channel.name in aliases.values():
                channel_hash[channel.name] = channel
        print("Finished generating aliases:")
        print(channel_hash)
        """

    async def test(self, sender, title, description, max_players, datetime):
        server = await client.fetch_guild(SERVER_ID)
        post_schema = {
            # role id
            # text channel id
            # voice channel id
        }
        # creates a temporary role
        role = await server.create_role(
            name="Player (" + title + ")",
            colour=discord.Colour.blue(),
            hoist=False,
            reason="Created an AL session"
        )
        post_schema["role"] = role.id

        category = await server.create_category(
            name=title,
            position=1
        )
        post_schema["category"] = category.id

        cleaned = title
        cleaned = re.sub(r'[^a-zA-Z0-9]', '', cleaned)
        cleaned = "-".join([i.lower() for i in title.split(" ")])
        # creates a temporary text channel
        text = await server.create_text_channel(
            name=cleaned,
            category=category,
            position=1,
            topic="Text channel for the " + title + " session"
        )
        post_schema["text"] = text.id

        voice = await server.create_voice_channel(
            name=title + " Voice",
            category=category,
            position=1
        )
        post_schema["voice"] = voice.id

        await sender.add_roles(role)
        return post_schema

    async def on_message(self, message: discord.Message):
        print("Message:", message)
        if message.content.startswith("$test"):
            schema = await self.test(message.author, "Test Title", "This is a test", 6, datetime.datetime.now())
            print("Schema: ", schema)

    async def process_deliver(self):
        """

        print("Finished waiting")
        print(self.msg)
        msg_lines = self.msg.split("\n")
        deliverables, total = {}, []
        last_target = None
        for line in msg_lines:
            if total:
                name = self.detect_name(line)
                if name:
                    deliverables[last_target] = "\n".join(total)
                    last_target = name
                    total.clear()
            else:
                target = self.detect_name(line)
                if target:
                    last_target = target
            total.append(line)
        # for the last sent message
        deliverables[last_target] = "\n".join(total)
        pprint(deliverables)
        await self.send_messages(deliverables)
        :return:
        """
        # await asyncio.sleep(WAIT_DURATION)


    async def send_messages(self, to_what):
        """
        for alias, message in to_what.items():
            channel = aliases.get(alias)
            channel = channel_hash.get(channel)
            if not channel:
                continue
            await channel.send(message)
            self.message_count += 1
            if self.message_count > MAX_MSG_PER_SECOND:
                await asyncio.sleep(1)
                self.message_count = 0
        print("Done")
        """

client = ALBotClient(intents=intents)
client.run(os.environ['TOKEN'])
