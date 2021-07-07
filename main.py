import discord
import json
from discord.ext import commands
import os
from keep_alive import keep_alive
from dotenv import load_dotenv

#bot init and prefixes
def get_prefix(client, ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(ctx.guild.id)]


intents = discord.Intents.all()
client = commands.Bot(command_prefix=get_prefix, intents=intents)
client.remove_command('help')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game('ncchelp'))
    print('Bot is ready')


@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefix = json.load(f)

    prefix[str(guild.id)] = 'ncc'

    with open('prefixes.json', 'w') as f:
        json.dump(prefix, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefix = json.load(f)

    prefix.pop(str(guild.id))

#commands and stuff
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! Latency: **{round(client.latency * 1000)}**ms')

@client.command()
async def help(ctx):
    embed = discord.Embed(title="Help", color=0x00ffb7)
    embed.set_thumbnail(
        url=
        "https://cdn.discordapp.com/attachments/861967320541167616/862283229755342848/220px-Ncadetclogo.png"
    )
    embed.set_footer(text=f"Requested by: {ctx.message.author.name}",
                     icon_url=f"{ctx.message.author.avatar_url}")
    embed.add_field(name="ping:",
                    value="Returns the latency of the bot.",
                    inline=False)
    await ctx.send(embed=embed)

#random connec stuff
keep_alive()
load_dotenv()
client.run(os.getenv('DISCORD_TOKEN'))