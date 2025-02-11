import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Intents to track deleted messages
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Dictionary to store sniped messages
sniped_messages = {}

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message_delete(message):
    """ Store the last deleted message per channel """
    if message.author.bot:
        return  # Ignore bot messages
    sniped_messages[message.channel.id] = {
        "content": message.content,
        "author": message.author,
        "time": message.created_at
    }

@bot.command()
async def snipe(ctx):
    """ Recovers the last deleted message in the channel """
    if ctx.channel.id in sniped_messages:
        sniped = sniped_messages[ctx.channel.id]
        embed = discord.Embed(
            title="💬 Sniped Message",
            description=sniped["content"],
            color=discord.Color.blue(),
            timestamp=sniped["time"]
        )
        embed.set_footer(text=f"Deleted by: {sniped['author']}")

        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ No recently deleted messages found!")

# Run the bot
bot.run(TOKEN)
