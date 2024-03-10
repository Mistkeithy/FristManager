import disnake
from disnake.ext import commands
import os
from config import Config
from logger import Logger
from localization import Localization

# Global aid objects
conf = Config()
l10n = Localization(conf.get("localization_code"))
log = Logger.getInstance(verbose=conf.get("log_verb_level"), debug=conf.get("log_debug"), file_path=conf.get("log_path"))
log.write(l10n.get("loaded_extension", extension = os.path.basename(__file__)), status=5, level=4)

class ClearCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='очистка', description='Удалить указанное количество сообщений из текущего канала')
    @commands.has_permissions(manage_messages = True, manage_channels = True)    
    async def clear_messages(
        self,
        ctx,
        count: int = commands.Param(description='Количество сообщений для удаления')
    ):
        log.write(l10n.get("removing_messages", count=count), status=5, level=5)
        if count <= 0:
            await ctx.send(l10n.get("incorrect_value", value=count), ephemeral=True)
            return
        try:
            await ctx.channel.purge(limit=count)
            await ctx.send(l10n.get("removed_messages", count=count), ephemeral=True)
        except disnake.errors.Forbidden:
            log.write(l10n.get("no_permission"), status=5, level=5)
            await ctx.send(l10n.get("no_permission"), ephemeral=True)

def setup(bot):
    bot.add_cog(ClearCog(bot))
