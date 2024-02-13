import discord
import os

from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Info(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="info", description="Donne les info sur le bot")
    @app_commands.checks.has_permissions(administrator=True)
    async def info(self, interaction: discord.Interaction):

        if round(self.bot.latency * 1000) > 200:
            icon = "<:lowconnection:1199405832073380032> "
        elif round(self.bot.latency * 1000) > 150:
            icon = "<:idleconnection:1199405830710231070> "
        elif round(self.bot.latency * 1000) < 150:
            icon = "<:goodconnection:1199405827900055583> "
        

        Embed = discord.Embed(title=" Gorilla <a:think:1206606264679796826>", color=0x9cffd4)
        Embed.add_field(name="Langage", value="Python", inline=True)
        Embed.add_field(name="Version", value=os.getenv("VERSION"), inline=True)
        Embed.add_field(name="Latence", value=f"{icon} {round(self.bot.latency * 1000)} MS", inline=True)
        Embed.add_field(name="Créateur", value="ciancoding", inline=False)

        await interaction.response.send_message(embed=Embed, ephemeral=False)



async def setup(bot):
    await bot.add_cog(Info(bot))