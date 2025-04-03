import discord
from discord.ext import commands
from discord import Embed
import os
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set intents
intents = discord.Intents.default()
intents.message_content = True

# Initialize bot
bot = commands.Bot(command_prefix=',', intents=intents)
bot.remove_command('help')  # Remove built-in help command

# Storage for AFK statuses, XP, and levels
afk_status = {}
user_xp = {}
user_levels = {}

# Kiss GIFs (FULL LIST)
kiss_gifs = [
    "https://media.giphy.com/media/3o6ZthkAMShWZvK7NC/giphy.gif",
    "https://media.giphy.com/media/6uFetT0Kw9Isg/giphy.gif",
    "https://media.giphy.com/media/l3vQWNHXOZzdMnIL6/giphy.gif",
    "https://media.giphy.com/media/J2WQhnfK2WuUE/giphy.gif",
    "https://media.giphy.com/media/frHK797nhEUow/giphy.gif",
    "https://media.giphy.com/media/HN4Om0tu8y7gk/giphy.gif",
    "https://media.giphy.com/media/YDB4EF3U6i6IM/giphy.gif",
    "https://media.giphy.com/media/l0HlPkb1ktE2PZFbG/giphy.gif",
    "https://media.giphy.com/media/l41lWAxLh1gwCzPmo/giphy.gif",
    "https://media.giphy.com/media/5x3rdgeXsujptmMRQC/giphy.gif"
]

# Hug GIFs (FULL LIST)
hug_gifs = [
    "https://media.giphy.com/media/SZyKSKOoEU1L73UzKB/giphy.gif",
    "https://media.giphy.com/media/f6y4qvdxwEDx6/giphy.gif",
    "https://media.giphy.com/media/VGACXbkf0AeGs/giphy.gif",
    "https://media.giphy.com/media/MViBn3PuOL6H4CIm2X/giphy.gif",
    "https://media.giphy.com/media/kooPUWvhaGe7C/giphy.gif",
    "https://media.giphy.com/media/3EJsCqoEiq6n6/giphy.gif",
    "https://media.giphy.com/media/Ilkurs1e3hP0c/giphy.gif",
    "https://media.giphy.com/media/xT9KVqbcSR3SzgQOC4/giphy.gif",
    "https://media.giphy.com/media/oajWAg9pnVzj56lOCp/giphy.gif"
]

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=",help"))
    print(f'Logged in as {bot.user}')


# AFK Command
@bot.command(help="sets your status to afk with an optional reason")
async def afk(ctx, *, reason="no reason provided"):
    afk_status[ctx.author.id] = reason
    embed = Embed(
        title="afk status",
        description=f"{ctx.author.mention} is now afk.\nreason: {reason}",
        color=0x000000
    )
    embed.set_footer(text="♡")
    await ctx.send(embed=embed)

# Remove AFK when user sends a message
@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore bot messages

    if message.author.id in afk_status:
        del afk_status[message.author.id]
        embed = Embed(
            title="afk status removed",
            description=f"{message.author.mention} is no longer afk!",
            color=0x000000
        )
        embed.set_footer(text="♡")
        await message.channel.send(embed=embed)

    # Leveling system with very small XP gain
    user_id = message.author.id
    if user_id not in user_xp:
        user_xp[user_id] = 0
        user_levels[user_id] = 1

    user_xp[user_id] += random.randint(1, 3)  # Tiny XP gain
    xp_needed = 200 * user_levels[user_id]  # XP needed increases per level

    if user_xp[user_id] >= xp_needed:
        user_levels[user_id] += 1
        user_xp[user_id] = 0
        level_up_embed = Embed(
            title=" Level up! <:milk_up:1356383429150904531> ",
            description=f"{message.author.mention} is now level {user_levels[user_id]}!",
            color=0x000000
        )
        level_up_embed.set_footer(text="♡")
        await message.channel.send(embed=level_up_embed)

    await bot.process_commands(message)

# Hug Command
@bot.command(help="hug another user with a cute gif")
async def hug(ctx, member: discord.Member):
    gif_url = random.choice(hug_gifs)
    embed = Embed(
        title="hug!",
        description=f"{ctx.author.mention} hugs {member.mention}! ^^",
        color=0x000000
    )
    embed.set_image(url=gif_url)
    embed.set_footer(text="♡")
    await ctx.send(embed=embed)

# Kiss Command
@bot.command(help="kiss another user with a cute gif")
async def kiss(ctx, member: discord.Member):
    gif_url = random.choice(kiss_gifs)
    embed = Embed(
        title="kiss!",
        description=f"{ctx.author.mention} kissed {member.mention}! <3",
        color=0x000000
    )
    embed.set_image(url=gif_url)
    embed.set_footer(text="♡")
    await ctx.send(embed=embed)

# Level Command
@bot.command(help="shows your current level and XP")
async def level(ctx):
    user_id = ctx.author.id
    level = user_levels.get(user_id, 1)
    xp = user_xp.get(user_id, 0)
    embed = Embed(
        title="your level stats",
        description=f"{ctx.author.mention} is level {level} with {xp} XP!",
        color=0x000000
    )
    embed.set_footer(text="♡")
    await ctx.send(embed=embed)

# Leaderboard Command
@bot.command(help="shows the XP leaderboard")
async def leaderboard(ctx):
    sorted_users = sorted(user_levels.items(), key=lambda x: x[1], reverse=True)
    leaderboard_text = ""

    for index, (user_id, lvl) in enumerate(sorted_users[:20], start=1):
        member = ctx.guild.get_member(user_id)
        xp = user_xp.get(user_id, 0)

        if member:
            leaderboard_text += f"#{index} {member.mention}: level {lvl}, {xp} XP\n"
        else:
            try:
                user = await bot.fetch_user(user_id)
                leaderboard_text += f"#{index} {user.mention}: level {lvl}, {xp} XP\n"
            except discord.NotFound:
                leaderboard_text += f"#{index} User ID {user_id}: level {lvl}, {xp} XP\n"

    embed = Embed(
        title="XP leaderboard",
        description=leaderboard_text if leaderboard_text else "No users ranked yet.",
        color=0x000000
    )
    embed.set_footer(text="♡")
    await ctx.send(embed=embed)

# Help Command
@bot.command(help="shows this help message")
async def help(ctx):
    embed = Embed(title="bot commands", description="use `,` as the prefix.", color=0x000000)
    embed.add_field(name="user commands", value="`,hug`, `,kiss`, `,afk`, `,level`, `,leaderboard`", inline=False)
    embed.set_footer(text="♡")
    await ctx.send(embed=embed)

bot.run(TOKEN)
