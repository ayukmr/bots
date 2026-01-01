import discord
import random
from emoji import EMOJI_DATA

def text_emoji(text: str) -> list[str | discord.Emoji]:
    text = text.lower()

    all_subs = {
        '0': ['0️⃣'],
        '1': ['1️⃣', '🥇'],
        '2': ['2️⃣', '🥈'],
        '3': ['3️⃣', '🥉'],
        '4': ['4️⃣'],
        '5': ['5️⃣'],
        '6': ['6️⃣'],
        '7': ['7️⃣'],
        '8': ['8️⃣'],
        '9': ['9️⃣'],

        '10':  ['🔟'],
        '100': ['💯'],

        '#':   ['#️⃣'],
        '*':   ['*️⃣', '✳️', '❇️'],
        '∞':   ['♾️'],
        '(':   [get_emoji('left_bird')],
        ')':   [get_emoji('right_bird')],
        '!':   ['❕', '❗'],
        '?':   ['❔', '❓'],
        '!!':  ['‼️'],
        '!?':  ['⁉️'],
        ' = ': ['🟰'],

        'ng':   ['🆖'],
        'ok':   ['🆗'],
        'up':   ['🆙'],
        'abc':  ['🔤'],
        'new':  ['🆕'],
        'cool': ['🆒'],
        'free': ['🆓'],

        'tm':  ['™️'],
        'atm': ['🏧'],
        'wc':  ['🚾'],
        'ab':  ['🆎'],
        'cl':  ['🆑'],
        'sos': ['🆘'],
        'id':  ['🆔'],
        'vs':  ['🆚'],
        'zzz': ['💤'],

        'a': ['🇦', '🅰️'],
        'b': ['🇧', '🅱️'],
        'c': ['🇨', '↪️'],
        'd': ['🇩'],
        'e': ['🇪', get_emoji('moji'), get_emoji('spheeer'), '📧'],
        'f': ['🇫'],
        'g': ['🇬'],
        'h': ['🇭', '♓'],
        'i': ['🇮', 'ℹ'],
        'j': ['🇯'],
        'k': ['🇰'],
        'l': ['🇱', get_emoji('el'), '🫷'],
        'm': ['🇲', '〽️', '♏', '♍'],
        'n': ['🇳', '♑', get_emoji('n64')],
        'o': ['🇴', '🅾️', '⭕'],
        'p': ['🇵', '🅿️'],
        'q': ['🇶'],
        'r': ['🇷', get_emoji('randwich')],
        's': ['🇸', get_emoji('cool')],
        't': ['🇹', get_emoji('tee'), '✝️'],
        'u': ['🇺'],
        'v': ['🇻', '♈'],
        'w': ['🇼'],
        'x': ['🇽', '❌'],
        'y': ['🇾'],
        'z': ['🇿'],

        ' ': ['🛤️', '🛣️', '🗾', '🎑', '🏞️', '🌅', '🌄', '🌠', '🎇', '🎆', '🌇', '🌆', '🏙️', '🌃', '🌌', '🌉']
    }

    random.shuffle(all_subs[' '])

    emojis = []

    # FIXME fix me
    for pred, subs in sorted(all_subs.items(), key=lambda item: -len(item[0])):
        if len(pred) > 1:
            for sub in subs:
                text = text.replace(pred, sub, 1)

    for char in text:
        if char in all_subs and all_subs[char] and all_subs[char][0] not in emojis:
            emojis.append(all_subs[char].pop(0))
        elif char in EMOJI_DATA:
            emojis.append(char)

    return emojis

async def react_text(message: discord.Message, text: str) -> None:
    reactions = list(dict.fromkeys(text_emoji(text)))

    if len(reactions) > 20:
        for reaction in reactions[:19]:
            await message.add_reaction(reaction)

        await react_emoji(message, 'whatever')
    else:
        for reaction in reactions:
            await message.add_reaction(reaction)

async def react_emoji(message: discord.Message, emoji: str) -> None:
    await message.add_reaction(get_emoji(emoji))

EMOJI = []

def load_emoji(client: discord.Client):
    global EMOJI
    EMOJI = client.emojis

def all_emojis() -> list[discord.Emoji]:
    return EMOJI

def get_emojis(emoji: str) -> list[discord.Emoji]:
    return [e for e in EMOJI if e.name == emoji]

def get_emoji(emoji: str) -> discord.Emoji:
    return get_emojis(emoji)[0]
