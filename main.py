import discord
import os
import motor.motor_asyncio
import time

from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv, find_dotenv
from utils import color_code

load_dotenv(find_dotenv())

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.mongoConnect = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('DB_CONNECTION'))

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"Hello world!"))

    print(f'✍️ {color_code.white} |  ----------------------')
    print(f'✅ {color_code.green}|  {bot.user} est prêt!{color_code.white}')
    print(f'🏓 {color_code.yellow}|  Latence -> {round(bot.latency * 1000)} MS{color_code.green}{color_code.white}')
    print(f'✍️ {color_code.white} |  ----------------------') 

    
    await bot.tree.sync() 

async def load():
        print(f'🔨 {color_code.white}|  ----------------------') 

        folders = os.listdir('./cogs')

        for folder in folders:
             if folder != "__pycache__":
                  files = os.listdir(f'./cogs/{folder}')

                  for file in files:
                          if file.endswith('.py'):
                             try:
                                    await bot.load_extension(f'cogs.{folder}.{file[:-3]}')
                                    print(f'🔮 {color_code.purple}|  Fichier {file[:-3]} a été charger{color_code.white}')
                             except Exception as e:
                                    print(f'❌ {color_code.red}|  {e}{color_code.white}')

        
        print(f'🔨 {color_code.white}|  ----------------------')
          


@bot.event
async def on_connect():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"Initialisation..."))

@bot.event
async def setup_hook():
    await load()

@bot.tree.error
async def on_app_command_error(ctx, error):
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = discord.Embed(title="⚠️ Commande en rechargement",
                                  description=f"Cette commande est en rechargement.\nVeuillez réessayer <t:{int(time.time() + error.retry_after)}:R>.",
                                  color=0xffdd63)
            await ctx.response.send_message(embed=embed)
        elif isinstance(error, app_commands.MissingPermissions):
            missing_perms = ', '.join(error.missing_permissions)
            embed = discord.Embed(title="⚠️ Permission(s) manquante(s)",
                                  description=f"Permission(s) manquante(s): `{missing_perms}`.\nVous avez besoin de cette (ou ces) permission(s).",
                                  color=0xffdd63)
            await ctx.response.send_message(embed=embed)
        elif isinstance(error, app_commands.MissingRole):
            missing_role = error.missing_role
            embed = discord.Embed(title="⚠️ Rôle requis manquant",
                                  description=f"Rôle manquant: <@&{missing_role}>.\nVous avez besoin de ce rôle.",
                                  color=0xffdd63)
            await ctx.response.send_message(embed=embed)
        else:
            await ctx.response.send_message(
                embed=discord.Embed(
                    title="Erreur inconnue au bataillon",
                    description=f"> {error}",
                    color=0xffdd63
                ))
            raise error


if __name__ == "__main__":
    bot.run(os.getenv('TOKEN'))





