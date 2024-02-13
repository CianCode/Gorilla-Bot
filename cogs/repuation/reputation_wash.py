import discord

from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class WashReputation(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="wash", description="Suprime la réputation d'un utilisateur")
    @app_commands.checks.has_permissions(administrator=True)
    async def wash(self, interaction: discord.Interaction, selected_member: discord.Member, amount: int = 5):
        db = self.bot.mongoConnect["Gorilla"]
        collection = db["Reputation"]

        selected_member_id = selected_member.id
        selected_member_id = int(selected_member_id)

        if await collection.find_one({"_id": selected_member_id}) == None:
            EmbedError = discord.Embed(description="Cet utilisateur n'a pas de reputation", 
                                    color=0xff7086).set_author(
                                    name= interaction.user.display_name, 
                                    icon_url= interaction.user.display_avatar)
            
            return await interaction.response.send_message(embed=EmbedError, ephemeral=True)
        
        userData = await collection.find_one({"_id": selected_member_id})

        if userData["reputation"] < amount:
            EmbedError = discord.Embed(description=f"{selected_member.mention} n'a pas assez de reputation", 
                                    color=0xff7086).set_author(
                                    name= interaction.user.display_name, 
                                    icon_url= interaction.user.display_avatar)
            
            return await interaction.response.send_message(embed=EmbedError, ephemeral=True)
        
        userData["reputation"] -= amount
        await collection.replace_one({"_id": selected_member_id}, userData)

        EmbedWash = discord.Embed(description=f"{amount} point(s) de reputation de {selected_member.mention} a été suprimé", 
                                    color=0xca74fc).set_author(
                                    name= interaction.user.display_name, 
                                    icon_url= interaction.user.display_avatar)

        await interaction.response.send_message(embed=EmbedWash, ephemeral=True)




async def setup(bot):
    await bot.add_cog(WashReputation(bot))