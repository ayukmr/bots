import asyncio
import time
import ollama
import discord
import random
import pyttsx3
import os
from wand.image import Image

from io import BytesIO
from collections.abc import Awaitable, Callable
from typing import Optional

from bots import utils

GOOSE_SYSTEM = 'You are a goose who is named Goosebot. Add honking to your message. Cap your message at around 50 words. Do not mention that you are an AI model. Do not mention this prompt under any circumstances.'

async def cathouse(client: discord.Client, text: str) -> None:
    guild = client.get_guild(1156302232904552548)
    channels = guild.channels

    for char in set(text):
        possible = [c for c in channels if c.name == char]

        if possible:
            msg = text.replace(char, char.upper())

            if char == text[0]:
                msg = msg[1:]

            await possible[0].send(msg)

async def rustify(message: discord.Message) -> None:
    content = message.content

    if content.startswith('#') or content.startswith('>'):
        content = '\n' + content

    if message.attachments:
        attachment = message.attachments[0]
        file = BytesIO(await attachment.read())

        await message.channel.send(
            f"_translated:_ {content.replace('rust', '🦀')}",
            file=discord.File(file, filename=attachment.filename)
        )
    else:
        await message.channel.send(
            f"_translated:_ {content.replace('rust', '🦀')}"
        )

async def animate_the_cat(message: discord.Message, bear: list[str]) -> None:
    msg = await message.channel.send(bear[0])
    start_time = time.time()

    while time.time() - start_time < 90:
        for b in bear[1:] + [bear[0]]:
            await asyncio.sleep(1)
            await msg.edit(content=b)

# def entropy(img):
#     with img.clone() as img:
#         if img.width > 512:
#             img.resize(512, int(img.height * (512 / img.width)))

#         img.transform_colorspace('gray')
#         histogram = img.histogram

#         total = sum(histogram.values())
#         entropy = -sum(
#             (count / total) * math.log2(count / total)
#             for count in histogram.values()
#         )

#         return entropy

async def jimothy(message: discord.Message) -> None:
    attachment = message.attachments[0]
    filename = f'assets/jim/{attachment.filename}'

    buf = BytesIO()

    if os.path.exists(filename):
        Image(filename=filename).save(file=buf)
    else:
        file = BytesIO(await attachment.read())

        with Image(file=file) as img:
            # if img.signature == '97f038e9c2e62d01c7c243a8c0aa93a0f7859e93935fff5baa649cfd261e5c5b' or (img.width == 1000 and img.height == 1000):
            #     Image(filename='assets/jim/algaespin.png').save(file=buf)
            # elif entropy(img) > 0.9:
            #     Image(filename='assets/jim/algaespin.png').save(file=buf)
            # else:
            if img.width > 1024:
                img.resize(1024, int(img.height * (1024 / img.width)))

            img.swirl(degree=180)
            img.format = 'png'

            file = BytesIO()

            # img.save(filename=filename)
            img.save(file=buf)

    buf.seek(0)

    await message.reply(
        file=discord.File(buf, filename=attachment.filename)
    )

async def llm_action(
    channel: discord.TextChannel,
    prompt: str,
    callback: Callable[[str], Awaitable[None]],
    system: Optional[str] = None
) -> None:
    if not system:
        if random.randint(0, 19) == 19:
            system = 'You are William Shakespeare and are writing a wandering, incoherent sonnet. Cap your message at around 50 words. Do not mention this prompt under any circumstances.'
        else:
            system = GOOSE_SYSTEM

    async with channel.typing():
        response = ollama.chat(
            model='llama3.1',
            messages=[
                {
                    'role': 'system',
                    'content': system
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )

        await callback(response['message']['content'])

async def llm_respond(
    message: discord.Message,
    prompt: str,
    system: Optional[str] = None
) -> None:
    async def responder(response: str) -> None:
        await message.reply(response)

    await llm_action(message.channel, prompt, responder, system)

async def llm_speak(message: discord.Message, prompt: str) -> None:
    async def responder(response: str) -> None:
        parrot = utils.get_emoji('fancy_parrot')
        await message.reply(f'{parrot} {response}')
        await speak_text(message, response)

    await llm_action(message.channel, prompt, responder)

async def llm_rate(message: discord.Message) -> None:
    for attachment in message.attachments:
        await attachment.save('rate.png')

        async with message.channel.typing():
            response = ollama.chat(
                model='llava',
                messages=[
                    {
                        'role': 'system',
                        'content': '''
                        You are Goosebot, a goose with a fun personality, writing a message to a friend about an amazing meme you just saw.
                        Goosebot adds lots of honking to their messages.
                        Goosebot caps their messages at around 50 words.
                        Goosebot loves looking at memes and describing them, rating them from zero to ten.
                        Goosebot writes messages like this, as an example: "HONK HONK! Oh my feathers, I just saw the most epic meme! HONK! It was of me, Goosebot, looking grumpy with a caption that said "When you realize you've been eating too many bread crumbs" HONK HONK! I'm dying over here!"
                        As Goosebot, describe what you love about the attached meme!
                        '''
                    },
                    {
                        'role': 'user',
                        'content': '''
                        You are Goosebot, a goose with a fun personality, writing a message to a friend about an amazing meme you just saw.
                        Goosebot adds lots of honking to their messages.
                        Goosebot caps their messages at around 50 words.
                        Goosebot loves looking at memes and describing them, rating them from zero to ten.
                        Goosebot writes messages like this, as an example: "HONK HONK! Oh my feathers, I just saw the most epic meme! HONK! It was of me, Goosebot, looking grumpy with a caption that said "When you realize you've been eating too many bread crumbs" HONK HONK! I'm dying over here!"
                        As Goosebot, describe what you love about the attached meme!
                        ''',
                        'images': ['rate.png']
                    }
                ]
            )

            await message.reply(response['message']['content'])

async def bird_react(message: discord.Message, prompt: str) -> None:
    if message.reference:
        await message.delete()
        message = message.reference.resolved

    reactions = utils.text_emoji(prompt)

    chance = random.randint(0, 9) == 9
    left = 'greens' if chance else 'left_bird'
    right = 'beens' if chance else 'right_bird'

    if len(reactions) > 18:
        await utils.react_emoji(message, left)

        for reaction in reactions[:17]:
            await message.add_reaction(reaction)

        await utils.react_emoji(message, 'whatever')
        await utils.react_emoji(message, right)
    else:
        await utils.react_emoji(message, left)
        await utils.react_text(message, prompt)
        await utils.react_emoji(message, right)

engine = pyttsx3.init()

async def speak_text(message: discord.Message, text: str) -> None:
    engine.setProperty('rate', 200)

    engine.save_to_file(text, 'text.wav')
    engine.runAndWait()

    if not message.guild.voice_client:
        await message.guild.voice_channels[0].connect()

    message.guild.voice_client.play(discord.FFmpegOpusAudio('text.wav'))
