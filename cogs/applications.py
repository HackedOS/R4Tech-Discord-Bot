from typing import Pattern
import discord
from discord.message import Message
from discord.ext import commands
from discord.ext.commands.core import command, has_role
from sqlite_func import *
from MaxEmbeds import EmbedBuilder
from discord.utils import get
class Applications(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.conn = bot.conn
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self,message: discord.Message):
        if message.author == self.bot.user:
            return

        #add reactions to vote on applications
        if message.channel.id == 887779003040153630:
            await message.add_reaction("\U00002705")
            await message.add_reaction("\U0000274e")
    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload: discord.RawReactionActionEvent):
        if payload.member.bot == False:
            if len(query_apply(self.conn)) != 0:
                if payload.message_id == query_apply(self.conn)[0][1] and payload.emoji.name == "\U0001f4ec":
                    await self.bot.get_guild(payload.guild_id).get_channel(payload.channel_id).get_partial_message(payload.message_id).remove_reaction("\U0001f4ec",payload.member)
                    if len(query_tickit_uid(self.conn,payload.user_id)) == 0:
                        member = payload.member
                        admin_role = get(self.bot.get_guild(payload.guild_id).roles, name="Member")
                        overwrites = {
                            self.bot.get_guild(payload.guild_id).default_role: discord.PermissionOverwrite(read_messages=False),
                            member: discord.PermissionOverwrite(read_messages=True),
                            admin_role: discord.PermissionOverwrite(read_messages=True)
                        }
                        channel = await self.bot.get_guild(payload.guild_id).create_text_channel("application-" + payload.member.name,category=self.bot.get_channel(887778958714748928))
                        ticket = (payload.user_id, channel.id)
                        create_ticket(self.conn,ticket)
                        embed = EmbedBuilder(
                        title="Apply to R4Tech",
                        description="Pls fill in the google form and await a response.\nhttps://forms.gle/LUnH4YYXf2JzUb7PA",
                        color=discord.Color.blue(),
                        footer=["Made by HackOS#9518", "https://cdn.discordapp.com/avatars/735367315734134887/c7c350169af19bef2876dcc52024efec.webp"],
                        thumbnail="https://cdn.discordapp.com/avatars/903900200521834577/97a802d6467c952af0f378ac8f3bc4b8.webp?size=64"
                        ).build()
                        await channel.send(embed=embed)

    @commands.command(name="close-ticket")
    @commands.has_any_role("Mod","Admin")
    async def close_ticket(self, message: discord.Message):
        if len(query_tickit_id(self.conn,message.channel.id)) != 0: 
            await message.channel.delete()
            delete_ticket(self.conn,message.channel.id)
        else:
            embed = EmbedBuilder(
            color=discord.Color.red(),
            description="This channel is not a ticket"
            ).build()
            await message.channel.send(embed=embed)

    @commands.command(name="open-apply")
    @commands.has_role("Admin")
    async def open_apply(self,message: discord.Message):
        if len(query_apply(self.conn)) == 0:
            embed = EmbedBuilder(
                title="Apply to R⁴Tech",
                description="To apply react with \U0001f4ec",
                color=discord.Color.blue(),
                footer=["Made by HackOS#9518", "https://cdn.discordapp.com/avatars/735367315734134887/c7c350169af19bef2876dcc52024efec.webp"],
                thumbnail="https://cdn.discordapp.com/avatars/903900200521834577/97a802d6467c952af0f378ac8f3bc4b8.webp?size=48"
                ).build()
            a = await message.guild.get_channel(895844610293792768).send(embed=embed)
            await a.add_reaction("\U0001f4ec")
            create_apply(self.conn,a.id)
        else:
            embed = EmbedBuilder(
                description="Applications are already open",
                color=discord.Color.red(),
                ).build()
            a = await message.channel.send(embed=embed)

    @commands.command(name="close-apply")
    @commands.has_role("Admin")
    async def close_apply(self,message: discord.Message):
        a = await message.channel.fetch_message(query_apply(self.conn)[0][1])
        await a.delete()
        delete_apply(self.conn)

def setup(bot):
    bot.add_cog(Applications(bot))