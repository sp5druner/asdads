import discord
from discord.ext import commands
from discord import app_commands
from api import fetch_server_data
from utils import format_score, parse_score
from config import ANNOUNCEMENT_URL, NIGHTLY_ANNOUNCEMENT_URL
from database import get_allowed_users

class Checks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def allowed(interaction: discord.Interaction):
        allowed_users = get_allowed_users()
        return interaction.user.id in allowed_users

    async def send_server_info(self, interaction, url, server_limit):
        data = await fetch_server_data(url)
        if not data:
            await interaction.response.send_message("Не удалось получить данные.", ephemeral=True)
            return

        servers = data.get('servers', [])
        total_players = sum(int(s.get("client_count", 0)) for s in servers[:server_limit])

        servers_sorted = sorted(
            servers[:server_limit],
            key=lambda s: parse_score(s.get("top_player_score", 0)),
            reverse=True
        )

        desc = f"```\n[Total players: {total_players}]\n"
        desc += "--------------------------------------\n"
        desc += "{:<18} {:<9} {:<8} {}\n".format("Server", "Count", "Score", "Nickname")
        desc += "--------------------------------------\n"
        for srv in servers_sorted:
            label = srv.get('label', 'Unknown')
            if label == "russia-0":
                label += " 🇷🇺"
            desc += "{:<18} {:<9} {:<8} {}\n".format(
                label,
                srv.get("client_count", "0"),
                format_score(int(srv.get("top_player_score", 0))),
                srv.get("top_player_name", "")
            )
        desc += "```"

        embed = discord.Embed(title="LastikSquad>ALL", description=desc, color=0xFF0000)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="check")
    @app_commands.check(allowed)
    async def check(self, interaction: discord.Interaction):
        await self.send_server_info(interaction, ANNOUNCEMENT_URL, 17)

    @app_commands.command(name="cn")
    @app_commands.check(allowed)
    async def cn(self, interaction: discord.Interaction):
        await self.send_server_info(interaction, NIGHTLY_ANNOUNCEMENT_URL, 2)

    @check.error
    @cn.error
    async def on_check_failure(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("У вас нет доступа к этой команде.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Checks(bot))
