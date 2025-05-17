import discord
import os # default module
from dotenv import load_dotenv
import asyncio

load_dotenv() # load all the variables from the env file
bot = discord.Bot()

@bot.event
async def on_ready():
  await bot.sync_commands()
  print(f"{bot.user} is ready and online!")
    
@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx: discord.ApplicationContext):
  await ctx.respond("Hey!")
    
@bot.slash_command(name="slow", description="Simulate a slow response")
async def slow(ctx: discord.ApplicationContext):
  await ctx.defer()  # tells Discord you're processing
  await asyncio.sleep(5)
  await ctx.respond("Thanks for waiting!")
  await ctx.send("This is a follow-up message.")
  
@bot.user_command(name="Account Creation Date")  # create a user command for the supplied guilds
async def account_creation_date(ctx: discord.ApplicationContext, member: discord.Member):  # user commands return the member
  await ctx.respond(f"{member.name}'s account was created on {member.created_at}")

@bot.message_command(name="Get Message ID")  # creates a global message command. use guild_ids=[] to create guild-specific commands.
async def get_message_id(ctx: discord.ApplicationContext, message: discord.Message):  # message commands return the message
  await ctx.respond(f"Message ID: `{message.id}`")

bot.run(os.getenv('BOT_TOKEN')) # run the bot with the token