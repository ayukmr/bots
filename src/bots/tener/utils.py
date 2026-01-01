import discord

from io import BytesIO
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

async def enhance(message: discord.Message) -> None:
    origin = message
    content = message.content

    if message.reference:
        message = message.reference.resolved

    attachment = message.attachments[0]
    file = BytesIO(await attachment.read())

    if (
        any(map(
            lambda start: message.content.startswith(start),
            ['renet', 'evah ot']
        )) or
        any(map(
            lambda end: message.content.endswith(end),
            ['renet', 'evah ot']
        ))
    ):
        orig = Image.open(file)

        image = ImageOps.invert(orig.convert('RGB'))

        enhancer = ImageEnhance.Contrast(image)
        image    = enhancer.enhance(2)

        enhancer = ImageEnhance.Color(image)
        image    = enhancer.enhance(2)

        image = image.filter(ImageFilter.SHARPEN)

        file = BytesIO()
        image.save(file, format=orig.format)

        file.seek(0)

    await message.channel.send(
        content,
        file=discord.File(file, filename=attachment.filename)
    )

    await origin.delete()
