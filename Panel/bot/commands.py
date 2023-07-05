import sys
import datetime
import random
import discord
import asyncio
import json
import requests
from datetime import timedelta
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
    embed.add_field(name="Wish to add to the bot?", value="Go on the [GitHub](https://github.com/AngleBoost/Self-Hosting-Bot) and make a pull request on commands.py or cogs.")
    await interaction.response.send_message(embed=embed)

@client.tree.command(name='timeout', description='Times out a member.')
@app_commands.checks.has_permissions(kick_members=True)
async def timeout(interaction: discord.Interaction, member: discord.User, *, reason: str, minutes: int):
    await member.timeout(timedelta(minutes=minutes), reason=reason)
    mod = interaction.user
    print(f"{mod} timed out {member}.")
    embed = discord.Embed(title='Timeout Successful', description=f'{member.mention} has been timed out for {minutes} minute(s).', color=0xFD7720)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client.tree.command(name='unban', description='Unbans a user.')
@app_commands.checks.has_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, userid: discord.User):
    guild = interaction.guild
    mod = interaction.user
    await guild.unban(user=userid)
    print(f"{mod} unbanned {userid}.")
    embed = discord.Embed(title='Unban Successful', description=f'{userid.mention} has been unbanned.', color=0xFD7720)
    await interaction.response.send_message(embed=embed)


@client.tree.command(name='softban', description='Bans and immediately unbans a user.')
@app_commands.checks.has_permissions(ban_members=True)
async def softban(interaction: discord.Interaction, userid: discord.User, *, reason: str):
    guild = interaction.guild
    mod = interaction.user
    await userid.ban(reason=reason)
    await guild.unban(user=userid)
    print(f"{mod} softbanned {userid}.")
    embed = discord.Embed(title='Softban Successful', description=f'{userid.mention} has been softbanned for {reason}.', color=0xFD7720)
    await interaction.response.send_message(embed=embed)


@client.tree.command(name='ban', description='Bans a user.')
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.User, *, reason: str):
    mod = interaction.user
    await member.ban(reason=f'{reason} - by {mod}')
    print(f"{mod} banned {member}.")
    embed = discord.Embed(title='Ban Successful', description=f'{member.mention} has been banned by {mod.mention} for {reason}.', color=0xFD7720)
    await interaction.response.send_message(embed=embed)


@client.tree.command(name='kick', description='Kicks a user.')
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.User, *, reason: str):
    mod = interaction.user
    await member.kick(reason=reason)
    embed = discord.Embed(title='Kick Successful', description=f'{member.mention} has been kicked by {mod.mention} for {reason}.', color=0xFD7720)
    print(f"{mod} kicked {member}.")
    await interaction.response.send_message(embed=embed)


@client.tree.command(name='clear', description='Clears messages.')
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    mod = interaction.user
    embed = discord.Embed(title='Clear Successful', description=f'{amount} message(s) have been cleared.', color=0xFD7720)
    await interaction.response.send_message(embed=embed, ephemeral=True)
    await interaction.channel.purge(limit=amount)
    print(f"{mod} cleared {amount} messages.")
    


@client.tree.command(name='nuke', description='Nukes a selected channel')
@app_commands.checks.has_permissions(manage_channels=True)
async def nuke(interaction: discord.Interaction, channel: discord.TextChannel):
    mod = interaction.user
    await interaction.response.defer()

    confirm_msg = await interaction.followup.send(content=f"Are you sure you want to nuke {channel.mention}?", ephemeral=True)
    await confirm_msg.add_reaction('✅')
    await confirm_msg.add_reaction('❌')

    def check(reaction, user):
        return user == interaction.user and str(reaction.emoji) in ['✅', '❌']

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await confirm_msg.edit(content='', embed=discord.Embed(title='Confirmation canceled.',color=discord.Color.red()))
        return
    if str(reaction.emoji) == '❌':
        await confirm_msg.edit(content='', embed=discord.Embed(title='Confirmation canceled.',color=discord.Color.red()))
        return

    await confirm_msg.edit(embed=discord.Embed(
        title='Nuking...',
        description=f'{channel.mention} is being nuked in 5 seconds!',
        color=discord.Color.red()
    ))

    message = await channel.send("THIS CHANNEL IS BEING NUKED IN 5")
    print(f"{mod} nuked {channel.name} messages.")
    for i in range(4, -1, -1):
        await asyncio.sleep(1)
        await message.edit(content=f'THIS CHANNEL IS BEING NUKED IN {i}')

    new_channel = await channel.clone(reason="Has been nuked!")
    await channel.delete()

    await new_channel.send("Nuked the channel successfully! :boom:")


@client.tree.command(name="server", description="Displays server infomation.")
@app_commands.checks.has_permissions(kick_members=True)
async def server(interaction: discord.Interaction):
    if interaction.guild.icon.url == None:
        embed = discord.Embed(title=f"{interaction.guild.name} Info",description="Information of this Server", color=0xFD7720)
        embed.add_field(name='🆔Server ID', value=f"{interaction.guild.id}", inline=False)
        embed.add_field(name='📆Created on',value=interaction.guild.created_at.strftime("%b %d %Y"),inline=False)
        embed.add_field(name='👑Owner',value=f"{interaction.guild.owner.mention}",inline=False)
        embed.add_field(name='👥Members',value=f'{interaction.guild.member_count} Members',inline=False)
        embed.add_field(name='💬Channels',value=f'{len(interaction.guild.text_channels)} Text | {len(interaction.guild.voice_channels)} Voice',inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=False)
    else:
        embed = discord.Embed(title=f"{interaction.guild.name} Info",description="Information of this Server", color=0xFD7720)
        embed.add_field(name='🆔Server ID', value=f"{interaction.guild.id}", inline=False)
        embed.add_field(name='📆Created on',value=interaction.guild.created_at.strftime("%b %d %Y"),inline=False)
        embed.add_field(name='👑Owner',value=f"{interaction.guild.owner.mention}",inline=False)
        embed.add_field(name='👥Members',value=f'{interaction.guild.member_count} Members',inline=False)
        embed.add_field(name='💬Channels',value=f'{len(interaction.guild.text_channels)} Text | {len(interaction.guild.voice_channels)} Voice',inline=False)
        embed.set_thumbnail(url=interaction.guild.icon.url)
        await interaction.response.send_message(embed=embed, ephemeral=False)

@client.tree.command(name='remind-me', description="Set a reminder")
async def remindme(interaction: discord.Interaction, time_str: str, *, reminder_message: str):
    await interaction.response.defer()
    # Parse the time string
    try:
        time_amount, time_unit = time_str[:-1], time_str[-1]
        time_amount = int(time_amount)
        if time_unit == 's':
            delta = datetime.timedelta(seconds=time_amount)
        elif time_unit == 'm':
            delta = datetime.timedelta(minutes=time_amount)
        elif time_unit == 'h':
            delta = datetime.timedelta(hours=time_amount)
        elif time_unit == 'd':
            delta = datetime.timedelta(days=time_amount)
        else:
            await interaction.followup.send('Invalid time unit! Please use s, m, h, or d. Example: /remindme 1h Go for a walk.')
            return
    except ValueError:
        await interaction.followup.send('Invalid time format! Please use a number followed by s, m, h, or d. Example: /remindme 1h Go for a walk.')
        return

    # Set the reminder
    await interaction.followup.send('Your reminder has been set. I will send you a DM when it is time so please have your DMs open to me.')
    await asyncio.sleep(delta.total_seconds())
    await interaction.user.send(f'Reminder: {reminder_message}')

@client.tree.command(name='8ball', description='Let the 8 Ball Predict!')
async def _8ball(interaction: discord.Interaction, *, question: str):
        responses = [
            'As I see it, yes.',
            'Yes.',
            'Positive',
            'From my point of view, yes',
            'Convinced.',
            'Most Likley.',
            'Chances High',
            'No.',
            'Negative.',
            'Not Convinced.',
            'Perhaps.',
            'Not Sure',
            'Maybe',
            'I cannot predict now.',
            'Im to lazy to predict.',
            'I am tired. *proceeds with sleeping*'
            ]
        response = random.choice(responses)
        embed=discord.Embed(title="The Magic 8 Ball has Spoken!", color=0xFD7720)
        embed.add_field(name='Question: ', value=question, inline=True)
        embed.add_field(name='Answer: ', value=response, inline=False)
        await interaction.response.send_message(embed=embed)


@client.tree.command(name='funnyrate', description='Rate how funny you are')
async def funnyrate(interaction: discord.Interaction):
        embed=discord.Embed(title=f"You are {random.randrange(101)}% funny!", color=0xFD7720)
        await interaction.response.send_message(embed=embed)


@client.tree.command(name='ship', description='unrelated to boats btw')
async def ship(interaction: discord.Interaction, member1: discord.User, member2: discord.User):
        """Ship two members together"""
        ship_percent = random.randint(1, 100)
        name1 = member1.name[:len(member1.name)//2]
        name2 = member2.name[len(member2.name)//2:]
        nameship = name1 + name2

        embed = discord.Embed(
            title=f"{member1.name} x {member2.name} = {nameship}",
            description=f"**Compatibility: {ship_percent}%**",
            color=0xFD7720
        )
    
        if ship_percent <= 35:
            embed.add_field(name="Result", value="😅 There doesn't seem to be such great chemistry going on, but who knows...?")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1067596766356185131/1068988991145259018/brokenheart_ship.gif")
        elif ship_percent > 35 and ship_percent <= 65:
            embed.add_field(name="Result", value="🫤 This combination has potential, how about a romantic dinner?")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1067596766356185131/1068989461083455548/thinking_ship.gif")
        elif ship_percent > 65:
            embed.add_field(name="Result", value="😍 Perfect combination! When will the wedding be?")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1067596766356185131/1068986257826402304/ship.gif")

        await interaction.response.send_message(embed=embed)


@client.tree.command(name='joke', description='Ask The Bot For A Funny')
async def joke(interaction: discord.Interaction):
        url = "https://v2.jokeapi.dev/joke/Programming,Miscellaneous,Dark,Pun,Spooky?blacklistFlags=nsfw,racist,sexist,explicit"
        try:
            res = requests.get(url)
            data = json.loads(res.text)
            if "setup" in data:
                joke = f"{data['setup']}...{data['delivery']}"
            else:
                joke = data["joke"]
            embed = discord.Embed(title="Joke", description=joke, color=0xFD7720)
            await interaction.response.send_message(embed=embed)
        except requests.exceptions.RequestException as e:
            await print(f"Error: {e}")


@client.tree.command(name='roll', description='Roll a dice')
async def roll(interaction: discord.Interaction):
        """Roll a dice"""
        roll = random.randint(1, 6)
        embed = discord.Embed(title=f"Rolling a dice...", description=f"You rolled a {roll}!", color=0xFD7720)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1067596766356185131/1068993152784023705/roll-the-dice.gif")
        await interaction.response.send_message(embed=embed) 

@client.tree.command(name='rps', description='Rock, Paper, Scissors')
async def rps(interaction: discord.Interaction, choice: str):
        choices = ["rock", "paper", "scissors"]
        computer_choice = random.choice(choices)
        result = ""
        if choice.lower() not in choices:
            result = "Invalid choice. Please choose rock, paper or scissors."
        elif choice.lower() == computer_choice:
            result = "It's a tie! You both chose " + choice + "."
        elif (choice.lower() == "rock" and computer_choice == "scissors") or (choice.lower() == "paper" and computer_choice == "rock") or (choice.lower() == "scissors" and computer_choice == "paper"):
            result = "You win! " + choice + " beats " + computer_choice + "."
        else:
            result = "You lose! " + computer_choice + " beats " + choice + "."
        embed = discord.Embed(title="Rock, Paper, Scissors", description=result, color=0xFD7720)
        embed.set_footer(text="Powered by RPSAPI")
        await interaction.response.send_message(embed=embed)

@client.tree.command(name='catfact', description='Tells you a random cat fact')
async def catfact(interaction: discord.Interaction):
    url = "https://cat-fact.herokuapp.com/facts/random"
    fact = json.loads(requests.get(url).text)["text"]
    embed = discord.Embed(title="Fun Cat Fact", description=fact, color=0xFD7720)
    embed.set_footer(text="Powered by CatFactsAPI")
    await interaction.response.send_message(embed=embed)

async def main():
    async with client:
        try:
            await client.start(bot_token)
        except discord.LoginFailure:
            messagebox.showerror("Error", "Failed to log in. Please check the bot token.")

asyncio.run(main())
