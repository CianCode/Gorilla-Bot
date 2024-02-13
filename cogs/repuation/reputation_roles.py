import discord

class ReputationRoles():
    reputation_roles = {
        10: discord.utils.get(guild.roles, name='Debutant'),
        15: discord.utils.get(guild.roles, name='Intermédiaire'),
        20: discord.utils.get(guild.roles, name='Pro'),
    }