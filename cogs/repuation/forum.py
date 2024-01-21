import discord

from discord import app_commands
from discord.ext import commands


progress = discord.ForumTag(name="En cours", emoji="🔨", moderated=False)
impossible = discord.ForumTag(name="Sans suite", emoji="🍂", moderated=False)
resolve = discord.ForumTag(name="Résolu", emoji="✅", moderated=False)


class Forum(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="forum", description="Créer un forum")
    @app_commands.checks.has_permissions(administrator=True)
    async def forum(self, interaction: discord.Interaction):

        if interaction.channel.category:

            await interaction.guild.create_forum(
                name= f"Entraide", 
                topic= f"Un problème ? Posez vos questions ici !", 
                category= interaction.channel.category, 
                position= 0, nsfw=False, slowmode_delay=0, 
                reason="Forum Creation", 
                default_auto_archive_duration= 10080, 
                default_thread_slowmode_delay= 0, 
                default_sort_order= discord.ForumOrderType.latest_activity, 
                default_reaction_emoji= "🔨",
                default_layout= discord.ForumLayoutType.list_view, 
                available_tags=[progress, impossible, resolve]
            )

            embedSucces = discord.Embed(description="Vous venez de créer un forum !", 
                                       color=0xf5da8c).set_author(
                                       name= interaction.user.display_name, 
                                       icon_url= interaction.user.display_avatar)
            
            await interaction.response.send_message(embed=embedSucces, ephemeral=True)
        else:
            embedError = discord.Embed(description="Le canal d'interaction n'appartient à aucune catégorie.", color=0xff7595)
            
            await interaction.response.send_message(embed=embedError, ephemeral=True)
        

async def setup(bot):
    await bot.add_cog(Forum(bot))