import discord

from discord import app_commands
from discord.ext import commands


class ReputationWallet(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="reputation", description="Affiche le nombre de points de reputation que vous avez !")
    async def reputation(self, interaction: discord.Interaction):
        db = self.bot.mongoConnect["Gorilla"]
        collection = db["Reputation"]

        if await collection.find_one({"_id": interaction.user.id}) == None:
            newData = {"_id": interaction.user.id, "reputation": 0}
            await collection.insert_one(newData)

        userData = await collection.find_one({"_id": interaction.user.id})

        EmbedWallet = discord.Embed(description="Vous avez actuellement " + str(userData["reputation"]) + " points de reputation !", 
                                    color=0xff99df).set_author(
                                    name= interaction.user.display_name, 
                                    icon_url= interaction.user.display_avatar)
        
        await interaction.response.send_message(embed=EmbedWallet, ephemeral=False)

async def setup(bot):
    await bot.add_cog(ReputationWallet(bot))