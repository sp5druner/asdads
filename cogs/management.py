import discord
from discord.ext import commands
from discord import app_commands
from database import add_allowed_user, remove_allowed_user
from config import ADMIN_ID

class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_admin(interaction: discord.Interaction):
        return interaction.user.id == ADMIN_ID

    manage_group = app_commands.Group(name="manage", description="Manage allowed users")

    @manage_group.command(name="add")
    @app_commands.check(is_admin)
    async def add(self, interaction: discord.Interaction, user: discord.Member):
        add_allowed_user(user.id)
        await interaction.response.send_message(f"{user.mention} добавлен.", ephemeral=True)

    @manage_group.command(name="remove")
    @app_commands.check(is_admin)
    async def remove(self, interaction: discord.Interaction, user: discord.Member):
        remove_allowed_user(user.id)
        await interaction.response.send_message(f"{user.mention} удален.", ephemeral=True)

    @add.error
    @remove.error
    async def admin_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("У вас нет прав администратора.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Management(bot))
