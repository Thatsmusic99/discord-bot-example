import os

import discord
import dotenv
from discord.ext import commands
import datetime
from pytz import timezone

dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix="$^")


@bot.event
async def on_ready():
    print("Hello, world!")


@bot.command()
async def time(context, timezone_raw):
    print("a")
    time_format = "%H:%M:%S (%d-%m-%Y)"
    mention = context.author.mention
    tz = timezone(timezone_raw)
    time_in_tz = datetime.datetime.now(tz)
    await context.send(f"Hello, {mention}! It's {time_in_tz.strftime(time_format)} "
                       f"in {timezone_raw}.")


bot.run(os.environ["BOT_TOKEN"])
