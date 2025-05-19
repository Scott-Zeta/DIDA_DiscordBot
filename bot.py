import discord
from config import BOT_TOKEN

bot = discord.Bot()

# Cogs List
cogs_list = ["cogs.health_check"]

@bot.event
async def on_ready():
    print(f"Loading Cogs...")
    bot.load_extensions(*cogs_list)
    await bot.sync_commands()
    print(f"{bot.user} is ready and online!")

bot.run(BOT_TOKEN)
               
