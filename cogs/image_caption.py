import discord
from discord.ext import commands
import asyncio
from services.image_caption import generate_caption
from utils.logger import Logger

log = Logger("cogs.image_caption")

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
            try:
                await placeholder_msg.edit(content=f"🔄 Processing image `{attachment.filename}`...")
                
                caption = await generate_caption(attachment.url, attachment.content_type)
                
                formatted_caption = f"📷 **Image by {author}:**\n{caption}"
                await placeholder_msg.edit(content=formatted_caption)
                log.info(f"Successfully captioned image {attachment.filename}")
                
            except Exception as e:
                log.error(f"Failed to process image {attachment.filename}: {e}")
                await placeholder_msg.edit(content=f"❌ Failed to process image `{attachment.filename}`. Error: {str(e)[:100]}")
            

        processing_tasks = [
            process_image(message.author.display_name, attachment, placeholder)
            for attachment, placeholder in zip(message.attachments, placeholder_messages)
        ]

        await asyncio.gather(*processing_tasks)
    
def setup(bot):
    bot.add_cog(ImageCaption(bot))