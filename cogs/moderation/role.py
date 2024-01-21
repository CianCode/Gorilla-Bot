import discord

from discord import app_commands
from discord.ext import commands


class Role(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="role", description="Selection de role")
    @commands.has_permissions(manage_messages=True)
    async def role(self, interaction: discord.Interaction):
        pass

        

async def setup(bot):
    await bot.add_cog(Role(bot))