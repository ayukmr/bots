import os
import discord
import asyncio
from mcstatus import JavaServer

from bots import utils as butils
from bots.goose import responders

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
last = 0

async def minecraft() -> None:
    global last

    channel = client.get_channel(1405419544239144971)
    channel2 = client.get_channel(1456153714187440393)

    spanish = ['cero', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve', 'diez']

    while True:
        players = JavaServer('shnebir.com').status().players.online

        await channel.edit(topic=f'{players} player{'' if players == 1 else 's'} honking')
        await channel2.edit(name=f'{spanish[players]}-whenemos')

        if players >= 2 and players != last:
            await channel2.send(f'<@&1456154992963489885> ¡¡¡{spanish[players]} players están en linea!!!')
        last = players

        await asyncio.sleep(300)

@client.event
async def on_ready() -> None:
    print(f'logged in as {client.user}')

    butils.load_emoji(client)
    asyncio.create_task(minecraft())

    activity = discord.CustomActivity(
        name=f'Honking in {len(client.guilds)} servers. | !help'
    )
    await client.change_presence(activity=activity)

@client.event
async def on_message(message: discord.Message) -> None:
    if message.author == client.user:
        return

    await responders.command(client, message)
    await responders.text(client, message)

def run() -> None:
    token = os.environ['GOOSE_TOKEN']
    client.run(token)
