import discord
from discord.ext import commands

class Applications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author == self.bot.user:
            return

        #add reactions to vote on applications
        if message.channel.id == 887779003040153630:
            await message.add_reaction("\U00002705")
            await message.add_reaction("\U0000274e")

def setup(bot):
    bot.add_cog(Applications(bot))