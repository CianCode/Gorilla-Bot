import discord

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import MissingPermissions


class Clear(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.checks.has_permissions(manage_messages=True)
    @commands.guild_only()
    @app_commands.command(name="clear", description="Efface un nombre de messages !")
    async def clear(self, interaction: discord.Interaction, amount: int = 1):
        if amount > 100:
            embed = discord.Embed(
                description='⚠️ Vous ne pouvez pas supprimer plus de 100 messages à la fois !',
                color=0xff7595
            )
            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )
            return    
        try:
            await interaction.response.defer(ephemeral=True, thinking=True)
            try:
                await interaction.message.delete()
            except:
                pass
            deleted = await interaction.channel.purge(limit=amount)
        except Exception as e:
            embed = discord.Embed(
                description=e,
                color=0xff7595
            )
            await interaction.followup.send(
                embed=embed
            )
            raise e

        if len(deleted) == 0:
            embed = discord.Embed(
                description=f'🧹 0 message a été supprimé',
                color=0xe38cf5
            )
        else:
            if len(deleted) == 1:
                embed = discord.Embed(
                    description=f'🧹 1 message a été supprimé',
                    color=0xe38cf5
                )
            else:
                embed = discord.Embed(
                    description=f'🧹 {len(deleted)} messages ont été supprimé',
                    color=0xe38cf5
                )

        try:
            await interaction.followup.send(
                embed=embed,
            )
        except:
            await interaction.followup.send(
                embed=embed,
            )

    # @clear.error
    # async def clear_error(self, interaction: discord.Interaction, error):
    #     if isinstance(error, app_commands.MissingPermissions):
    #         embed = discord.Embed(
    #             description='⚠️ Vous n\'avez pas la permission de supprimer des messages !',
    #             color=0xff7595
    #         )
    #         await interaction.response.send_message(
    #             embed=embed,
    #             ephemeral=True
    #         )
        

async def setup(bot):
    await bot.add_cog(Clear(bot))