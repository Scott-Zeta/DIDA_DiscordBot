import discord
from discord.ext import commands
import asyncio

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
        async def process_image(attachment, placeholder_msg):
            await asyncio.sleep(3)  # Replace with actual async API call
            caption = f"Image caption for `{attachment.filename}`: This is a sample caption."
            await placeholder_msg.edit(content=caption)
            

        processing_tasks = [
            process_image(attachment, placeholder)
            for attachment, placeholder in zip(message.attachments, placeholder_messages)
        ]

        await asyncio.gather(*processing_tasks)
    
def setup(bot):
    bot.add_cog(ImageCaption(bot))