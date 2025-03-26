import discord
from discord.ext import commands
import asyncio
import database
from config import BOT_TOKEN

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        database.init_db()
        await self.load_extension('cogs.checks')
        await self.load_extension('cogs.management')
        await self.load_extension('cogs.userinfo')
        await self.tree.sync()

    async def on_ready(self):
        print(f"Бот {self.user} запущен и готов к работе!")

bot = Bot()
bot.run(BOT_TOKEN)
