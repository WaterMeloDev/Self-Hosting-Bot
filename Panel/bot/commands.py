import sys
import customtkinter
import discord
import asyncio
import shutil
from discord import app_commands
from discord.ext import commands, tasks
from itertools import cycle
from tkinter import messagebox

# Retrieve the bot token from command-line arguments
bot_token = sys.argv[1]

interaction = discord.Interaction
intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix="s!", intents=intents)

bot_status = cycle([
    "Beta",
    "Self Hosting Bot"
])

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Streaming(name=next(bot_status), url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'))

client.remove_command('help')


@client.event
async def on_ready():
    try: 
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands!")
    except:
        print('already synced')

    change_status.start()
    print(f"Sucessfully logged in as {client.user}")

@client.tree.command(name="help", description="Displaying help commands.")
async def help_command(interaction):
    embed = discord.Embed(title="Self-Hosting Help", description="Displaying help commands.", color=discord.Color.blue())
    embed.add_field(name="Warning!", value="This bot program requires basic knowledge of Python and Discord.py.")
    embed.add_field(name="Wish to add to the bot?", value="Go on the [GitHub](https://github.com) and make a pull request on commands.py or cogs.")
    await interaction.response.send_message(embed=embed)

async def main():
    async with client:
        try:
            await client.start(bot_token)
        except discord.LoginFailure:
            messagebox.showerror("Error", "Failed to log in. Please check the bot token.")

asyncio.run(main())
