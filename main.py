# Imports
from sqlite3.dbapi2 import Error
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from MaxEmbeds import EmbedBuilder
import sqlite3
from sqlite_func import *


#Load .env
load_dotenv()

#define prefix
prefix = "?"

#define intents
intents = discord.Intents.all()
#define bot object
bot = commands.Bot(command_prefix=prefix)

#cog reload disable in production
bot.load_extension('cog_reloader')



#Info tell if bot is logged in
@bot.listen()
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

#test shit
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
    
    await bot.process_commands(message)

#setup DB
conn = create_connection("r4tech.db")
if conn is not None:
    # create projects table
    sql_create_ticket = """ CREATE TABLE IF NOT EXISTS ticket (
	id integer PRIMARY KEY,
	member_id integer NOT NULL,
	channel_id integer NOT NULL); """

    sql_create_apply = """ CREATE TABLE IF NOT EXISTS apply (
	id integer PRIMARY KEY,
	message_id integer NOT NULL); """
    create_table(conn, sql_create_ticket)
    create_table(conn,sql_create_apply)
else:
    print("Error! cannot create the database connection.")
bot.conn = conn

#load cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded Cog : {filename}")
        except Exception as e:
            print(f'Failed to load Cog : {filename}')
            raise e

#start the bot
bot.run(os.environ.get('token'))

