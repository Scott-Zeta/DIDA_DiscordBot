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

class MyButtonView(discord.ui.View):
  @discord.ui.button(label="Button 1", style=discord.ButtonStyle.primary)
  async def button1(self, button, interaction):
    await interaction.response.send_message("Button 1 clicked!")
    self.disable_all_items()
    await interaction.message.edit(view=self)

  @discord.ui.button(label="Button 2", style=discord.ButtonStyle.success)
  async def button2(self, button, interaction):
    await interaction.response.send_message("Button 2 clicked!")
    self.disable_all_items()
    await interaction.message.edit(view=self)

@bot.slash_command() # Create a slash command
async def button(ctx: discord.ApplicationContext):
  await ctx.respond("This is a button!", view=MyButtonView()) # Send a message with our View class that contains the button

class MySelectView(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose a Flavor!", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="Vanilla",
                description="Pick this if you like vanilla!"
            ),
            discord.SelectOption(
                label="Chocolate",
                description="Pick this if you like chocolate!"
            ),
            discord.SelectOption(
                label="Strawberry",
                description="Pick this if you like strawberry!"
            )
        ]
    )
    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")

@bot.command()
async def flavor(ctx):
    await ctx.respond("Choose a flavor!", view=MySelectView())
    
class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Short Input"))
        self.add_item(discord.ui.InputText(label="Long Input", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Results")
        embed.add_field(name="Short Input", value=self.children[0].value)
        embed.add_field(name="Long Input", value=self.children[1].value)
        await interaction.response.send_message(embeds=[embed])
        
@bot.slash_command()
async def modal_slash(ctx: discord.ApplicationContext):
    """Shows an example of a modal dialog being invoked from a slash command."""
    modal = MyModal(title="Modal via Slash Command")
    await ctx.send_modal(modal)
bot.run(os.getenv('BOT_TOKEN')) # run the bot with the token