from discord.commands import slash_command
from discord.ext import commands

class ErrorLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_error(self, event):
        print(event)
        error_log_channel = self.bot.get_channel(946062815700062291)
        
        

def setup(bot):
    bot.add_cog(ErrorLog(bot))