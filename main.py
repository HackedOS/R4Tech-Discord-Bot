from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from MaxEmbeds import EmbedBuilder
load_dotenv()

prefix = "?"


bot = commands.Bot(command_prefix=prefix)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded Cog : {filename}")
        except Exception as e:
            print(f'Failed to load Cog : {filename}')
            raise e

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith("$test"):
        embed = EmbedBuilder(
            title="Project Board",
            description="",
            color=discord.Color.blue(),
            fields=[["Field 1", "Test field", True], ["Field 2", "Test field", True]],
            footer=["Test footer", message.author.avatar_url],
            author=[message.author.name, message.author.avatar_url],
            thumbnail=message.author.avatar_url
            ).build()
        await message.channel.send(embed=embed)
        
    if message.channel.id == 887779003040153630:
        await message.add_reaction("\U00002705")
        await message.add_reaction("\U0000274e")

bot.run(os.environ.get('token'))

