# This example requires the 'message_content' intent.

import os
from dotenv import load_dotenv

load_dotenv()

import discord

intents = discord.Intents.default()
intents.message_content = True

class ALBotClient(discord.Client):
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

    @client.event
    async def on_message(message):
        pass

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

    async def on_message(self, message):
        print(f'Message from {message.author.id}: {message.content}')
        """
        if message.author.id != bot_id:
            return
        if self.msg == "":
            self.msg += message.content + "\n"
            await self.process_deliver()
            self.msg = ""
        else:
            self.msg += message.content + "\n"
        """

@commands.command()
async def mute(self, ctx, member: discord.Member):
    guild = ctx.guild
    role = await guild.create_role(name='muted', hoist=True)

    all_roles = await guild.fetch_roles()
    num_roles = len(all_roles)
    print(f'The server has {num_roles} roles.')
    await role.edit(reason=None, position=num_roles - 2)
    print('Created new role!')
    await member.add_roles(role)
    await ctx.send(f'{member} has been muted.')

client.run(os.environ['TOKEN'])
