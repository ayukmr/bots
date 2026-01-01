import discord
import collections

async def user_reactions(message: discord.Message) -> None:
    total = 0
    user_count = collections.defaultdict(int)

    async with message.channel.typing():
        async for msg in message.channel.history(limit=1000):
            for reaction in msg.reactions:
                async for user in reaction.users():
                    total += 1
                    user_count[user.name] += 1

    response = f'## Total: {total}'

    response += '\n## Users'
    for user, count in sorted(user_count.items(), key=lambda user_count: -user_count[1]):
        response += f'\n{user}: {count} ({(count / total) * 100}%)'

    await message.channel.send(response)

async def all_reactions(message: discord.Message) -> None:
    total = collections.defaultdict(int)
    unique = collections.defaultdict(int)

    async with message.channel.typing():
        async for msg in message.channel.history(limit=5000):
            for reaction in msg.reactions:
                unique[reaction.emoji] += 1
                total[reaction.emoji] += reaction.count

    response = f'# Last 5000 messages'

    response += f'\n## Unique'
    for emoji, count in sorted(unique.items(), key=lambda emoj_count: -emoj_count[1]):
        response += f'\n{emoji}: {count}'

    response += '\n## Total'
    for emoji, count in sorted(total.items(), key=lambda emoj_count: -emoj_count[1]):
        response += f'\n{emoji}: {count}'

    await message.channel.send(response)
