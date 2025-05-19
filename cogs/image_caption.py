import discord
from discord.ext import commands
import asyncio
from services.image_caption import generate_caption

class ImageCaption(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.attachments:
            return

        # Step 1: Send all placeholder messages immediately
        placeholder_tasks = []
        for attachment in message.attachments:
            task = message.channel.send(f"Processing image `{attachment.filename}`...")
            placeholder_tasks.append(task)

        placeholder_messages = await asyncio.gather(*placeholder_tasks)

        # Step 2: Process each image concurrently and edit the placeholder message
        async def process_image(author, attachment, placeholder_msg):
            caption = f"Description for image sent by `{author}`:{generate_caption(attachment.url, attachment.content_type)}"
            await placeholder_msg.edit(content=caption)
            

        processing_tasks = [
            process_image(message.author.display_name, attachment, placeholder)
            for attachment, placeholder in zip(message.attachments, placeholder_messages)
        ]

        await asyncio.gather(*processing_tasks)
    
def setup(bot):
    bot.add_cog(ImageCaption(bot))