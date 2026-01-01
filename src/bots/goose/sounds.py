import discord
import asyncio
import random
import os

from typing import Callable, Optional

from bots import utils

async def play_sound(client: discord.Client, message: discord.Message, sound, callback: Optional[Callable] = None) -> None:
    if not message.guild.voice_client:
        await message.guild.voice_channels[0].connect()

    message.guild.voice_client.play(discord.FFmpegOpusAudio(sound), after=callback)

    parrot = utils.get_emoji('fancy_parrot')

    if callback:
        parrot = utils.get_emoji('loro')
        sound = f'||{sound}||'

    channel = client.get_channel(1174179100227805245)
    await channel.send(f'{parrot} {sound} {parrot}')

cur_queue = os.listdir('assets/sounds')
random.shuffle(cur_queue)

async def play_all(client: discord.Client, message: discord.Message) -> None:
    global cur_queue

    if not cur_queue:
        cur_queue = os.listdir('assets/sounds')
        random.shuffle(cur_queue)
        return

    sound = cur_queue.pop()

    await play_sound(
        client,
        message,
        f'assets/sounds/{sound}',
        callback=lambda _: asyncio.run_coroutine_threadsafe(
            play_all(client, message),
            client.loop
        )
    )
