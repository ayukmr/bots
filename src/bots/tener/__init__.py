import os
import random
import discord

from bots import utils as butils
from bots.tener import utils

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready() -> None:
    print(f'logged in as {client.user}')

@client.event
async def on_message(message: discord.Message) -> None:
    if message.author == client.user:
        return

    if message.content.startswith('~roose'):
        for _ in range(100):
            await message.channel.send('~race @Drumming2008')

    if message.content == 'not very tener':
        async for hist in message.channel.history(limit=100):
            if hist.author == client.user:
                await message.delete()

                emoji = random.choice(['disgruntled', 'no', 'unimpressed'])

                if random.randint(0, 9) >= 5:
                    emoji = 'sad'

                await hist.reply(
                    f'that was not very tener {butils.get_emoji(emoji)}'
                )

                await butils.react_text(hist, 'fake')
                await butils.react_emoji(hist, 'fake')

                return

    if message.content == 'very tener':
        async for hist in message.channel.history(limit=100):
            if hist.author == client.user:
                await message.delete()

                await hist.reply(
                    f"that was very tener {butils.get_emoji('good')}"
                )

                await butils.react_text(hist, 'real')
                await butils.react_emoji(hist, 'emoji_35')

                return

    if message.content == '!honk':
        await message.delete()

        if not message.guild.voice_client:
            await message.guild.voice_channels[0].connect()

        message.guild.voice_client.play(discord.FFmpegOpusAudio('assets/sounds/honk.opus'))

    if (
        any(map(
            lambda start: message.content.startswith(f'{start} when '),
            ['me', 'tener', 'renet']
        )) or
        any(map(
            lambda end: message.content.endswith(f' when {end}'),
            ['tener', 'renet', 'tener?', 'renet?']
        )) or
        message.content.startswith('yo cuando ') or
        any(map(
            lambda end: message.content.endswith(f' cuando {end}'),
            ['tener', 'to have', 'renet', 'evah ot']
        ))
    ):
        if not message.attachments and not (message.reference and message.reference.resolved.attachments):
            return

        await utils.enhance(message)

def run() -> None:
    token = os.environ['TENER_TOKEN']
    client.run(token)
