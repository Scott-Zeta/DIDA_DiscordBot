import discord
from discord.ext import commands

class HealthCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="ping", description="Check the bot's health.")
    async def ping(self, ctx):
        """Check the bot's health."""
        await ctx.respond(f'Pong! The bot is alive and running!')

def setup(bot):
    bot.add_cog(HealthCheck(bot))