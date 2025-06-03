import discord
from utils.logger import Logger
from config import BOT_TOKEN

log = Logger()
bot = discord.Bot(intents=discord.Intents.all())

# Cogs List
cogs_list = ["cogs.health_check",
             "cogs.image_caption"]

@bot.event
async def on_ready():
    log.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    for cog in cogs_list:
        try:
            bot.load_extension(cog)
            log.info(f"Loaded cog: {cog}")
        except Exception as e:
            log.error(f"Failed to load cog {cog}: {e}")
    await bot.sync_commands()
    log.info("Bot is ready and commands are synced.")

@bot.event
async def on_application_command_error(ctx, error):
    log.error(f"Command error: {error}")
    await ctx.respond("An error occurred while executing the command.")

log.info("Starting bot...")
bot.run(BOT_TOKEN)
               
