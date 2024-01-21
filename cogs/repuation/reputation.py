import discord
import asyncio

from discord import app_commands
from discord.ext import commands
        

class MemberSelect(discord.ui.Select):
    def __init__(self, bot, options):
        super().__init__(placeholder='Sélectionnez un membre', options=options)
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        db = self.bot.mongoConnect["Gorilla"]
        collection = db["Reputation"]

        selected_member_id = interaction.data['values'][0]
        selected_member_id = int(selected_member_id)
        membersName = interaction.guild.get_member(selected_member_id)

        if await collection.find_one({"_id": selected_member_id}) == None:
            newData = {"_id": selected_member_id, "reputation": 0}
            await collection.insert_one(newData)

        userData = await collection.find_one({"_id": selected_member_id})

        reputRecieved = 5

        userData["reputation"] += reputRecieved
        await collection.replace_one({"_id": selected_member_id}, userData)

        Embed = discord.Embed(description=f"{membersName.mention} a été sélectionné comme la personne à avoir aider le plus dans se thread \n Il a reçu {reputRecieved} point de reputation !", color=0xff78a7)
        await interaction.response.send_message(embed=Embed, ephemeral=False)

        forum = interaction.channel.parent
        all_tags = forum.available_tags
        tag = discord.utils.get(all_tags, name="Résolu")

        await interaction.channel.edit(locked=True, applied_tags=[tag])


        

class Reputation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    
    @app_commands.command(name="resolu", description="Indiquer que le thread est résolu.")
    async def resolue(self, interaction: discord.Interaction):

        if isinstance(interaction.channel, discord.Thread) and (interaction.channel.owner_id == interaction.user.id or interaction.user.guild_permissions.administrator):
            members = await interaction.channel.fetch_members()
            participants = set()
            for member in members:
                membersId = interaction.guild.get_member(member.id)
                participants.add(membersId)

            options = [
                discord.SelectOption(label=participant.display_name, value=str(participant.id), emoji="👲")
                for participant in participants
                if participant.id != interaction.channel.owner_id and not participant.bot
            ]

            select = MemberSelect(self.bot, options)
            view = discord.ui.View()
            view.add_item(select)

            EmbedSelect = discord.Embed(description="Sélectionnez un membre à remercier pour vous avoir aider !", 
                                    color=0x94ffed).set_author(
                                    name= interaction.user.display_name, 
                                    icon_url= interaction.user.display_avatar)

            await interaction.response.send_message(embed=EmbedSelect, view=view, ephemeral=True)
        else:
            if isinstance(interaction.channel, discord.Thread):
                embedError = discord.Embed(description="Vous devez être propriétaire du Thread", color=0xff7595)
            else:
                embedError = discord.Embed(description="Cette commande ne peut être utilisée que dans un thread.", color=0xff7595)
                    
            await interaction.response.send_message(embed=embedError, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Reputation(bot))