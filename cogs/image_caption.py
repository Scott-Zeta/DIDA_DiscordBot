import discord
from discord.ext import commands
import asyncio
from services.image_caption import generate_caption
from utils.logger import Logger
from utils.rate_limiter import rate_limit

log = Logger("cogs.image_caption")

# Constants
MAX_FILE_SIZE_MB = 20
SUPPORTED_FORMATS = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']

class ImageCaption(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    @rate_limit(cooldown_seconds=30, max_uses=3, feature_name="Image Caption")
    async def on_message(self, message):
        if message.author.bot or not message.attachments:
            return

        # Filter only supported image attachments
        valid_attachments = [
            attachment for attachment in message.attachments
            if attachment.content_type in SUPPORTED_FORMATS 
            and attachment.size <= MAX_FILE_SIZE_MB * 1024 * 1024
        ]
        
        if not valid_attachments:
            return
            
        log.info(f"Processing {len(valid_attachments)} images from {message.author.display_name}")
        
        # Step 1: Send all placeholder messages immediately
        placeholder_tasks = []
        for attachment in valid_attachments:
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
            for attachment, placeholder in zip(valid_attachments, placeholder_messages)
        ]

        await asyncio.gather(*processing_tasks)
    
def setup(bot):
    bot.add_cog(ImageCaption(bot))