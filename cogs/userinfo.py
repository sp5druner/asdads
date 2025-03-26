import discord
from discord.ext import commands
from discord import app_commands
from database import get_allowed_users
from config import ADMIN_ID

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_admin(interaction: discord.Interaction):
        return interaction.user.id == ADMIN_ID

    @app_commands.command(name="userinfo")
    @app_commands.check(is_admin)
    async def userinfo(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Разрешенные пользователи", color=0xFF0000)
        for user_id in get_allowed_users():
            user = self.bot.get_user(user_id) or await self.bot.fetch_user(user_id)
            embed.add_field(name=user.name if user else "Неизвестный", value=f"ID: {user_id}", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @userinfo.error
    async def admin_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Только администратор может использовать эту команду.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(UserInfo(bot))
