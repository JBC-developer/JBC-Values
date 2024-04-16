import discord
from discord.ext import commands
from discord import app_commands
import Token
import numpy as np
from difflib import *

from keep_alive import keep_alive
import test

keep_alive()
bot = commands.Bot(command_prefix="?", intents= discord.Intents.all())

value = np.load('ValueList.npy', allow_pickle=True).item()
k = list(value.keys())
v = list(value.values())
values : dict[str, list[str]]
values = {}
values = {k: v for k, v in zip(k,v)}
names = list(values.keys())


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

msg = '''## Hi There!

**Setting up:**
1. Please use the command /setup
2. Select the channel that you want the bot to work in. Keep in mind that it will not respond in any other channel
3. Enjoy!

**Value Lists:**
[JBC Value List](<https://docs.google.com/spreadsheets/d/1mKz2YsgKevFvPI08XU7vCiaPBnUH9OvFzjBSO6TCvPg/edit#gid=1658217925>)

**Bot Owner:**
<@857892645543215116> `jailbreakduck | 857892645543215116`

**Bot Developer:** 
<@745583659389681675> `hydraulic4128 | 745583659389681675`

**Credits:**
[JBC](<https://discord.com/invite/jbc>)
[Auto Creavite](<https://auto.creavite.co/>)

**Other questions or concerns?**
Join our [Support & Development Server](<https://discord.gg/5wtYzKGn6u>)
Terms of Service can be accessed [here](<https://docs.google.com/document/d/1AbPgAUexIxxN6qIX5QOjK3TiWVF4_FR-62d1zoQOFIQ/edit>)'''

class MyView(discord.ui.View):
    @discord.ui.select(
        cls=discord.ui.ChannelSelect,
        placeholder = "Choose a channel for the bot to work in",
        channel_types=[discord.ChannelType.text]
    )
    async def select_callback(self, interaction, select): # the function called when the user is done selecting options
        channel_dict = dict(np.load('Channel_Dict.npy', allow_pickle=True).item())
        channel = select.values[0]
        channel_dict[int(interaction.guild.id)] = int(channel.id)

        np.save('Channel_Dict.npy', channel_dict)
        try:
            embed=discord.Embed(title='The bot has been setup to work here',description = "Type the name of the item you want to know the value of", color=0x11fa00)
            channel = bot.get_channel(int(channel.id))
            await channel.send(embed = embed)
            await interaction.response.send_message(f"The bot has been setup to work in {select.values[0]}")
        except:
            embed=discord.Embed(title='**Important**',description = f"The bot has been setup to work in {select.values[0]}, but it cannot function right now\nPlease check the permissions of the bot in the {select.values[0]} channel\nMake sure it has these permissions:\n`Send Messages`, `Embed links` and `Attach files`\nThe bot will not work until it has these permissions", color=0xff0000)
            await interaction.response.send_message(embed = embed)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/help"))

    print("Im jbc bot")
    channel_dict = dict(np.load('Channel_Dict.npy', allow_pickle=True).item())

    values = np.load('ValueList.npy', allow_pickle=True).item()

    k = list(values.keys())
    v = list(values.values())
    img = []
    for va in v:
        img.append(va[0])
    images = {}
    images = {k: img for k, img in zip(k,img)}

    test.main(images)

    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)



@bot.tree.command(name="setup")
@commands.has_permissions(administrator = True)
@app_commands.checks.has_permissions(administrator=True)
async def setup(interaction : discord.Interaction):
    await interaction.response.send_message('Thanks for using our bot! Please select a channel for it to work in - ', view = MyView())



@setup.error
async def setup_error(interaction :  discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("You have no permissions to run this command", ephemeral=True)


@bot.tree.command(name="valueupdate")
@commands.has_permissions(administrator = True)
@app_commands.checks.has_permissions(administrator=True)
async def valueupdate(interaction : discord.Interaction):
    await interaction.response.send_message('Updating Values...')
    try:
        values = np.load('ValueList.npy', allow_pickle=True).item()

        k = list(values.keys())
        v = list(values.values())
        img = []
        for va in v:
            img.append(va[0])
        images = {}
        images = {k: img for k, img in zip(k,img)}

        test.main(images)



        names = list(values.keys())
        
        return await interaction.channel.send('Values updated')
    except Exception as e:
        print(e)
        return await interaction.channel.send("I wasn't able to update the values")
    


@valueupdate.error
async def valueupdate_error(interaction :  discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("You have no permissions to run this command", ephemeral=True)
    #await interaction.response.send_message("No perms", ephemeral=True)



@bot.tree.command(name="help")
async def help(interaction: discord.Interaction):
    embed=discord.Embed(title="JBC Value Bot", description="This bot has been created for JBC by Hydraulic (`745583659389681675`)")
    embed.add_field(name="Commands :-", value="Only for administrators - \n\n/valueupdate - Updates values from the Value List\n/setup - Setup the bot\n\nFor getting a value, just type the name of the item in the value commands channel", inline=False)
    await interaction.response.send_message(msg)



@bot.event
async def on_message(message):
    channel_dict = dict(np.load('Channel_Dict.npy', allow_pickle=True).item())
    if(message.guild.id not in list(channel_dict.keys())):
        return
    if(message.channel.id != channel_dict[message.guild.id]):
        return

    value = np.load('ValueList.npy', allow_pickle=True).item()
    k = list(value.keys())
    v = list(value.values())
    values : dict[str, list[str]]
    values = {}
    values = {k: v for k, v in zip(k,v)}
    names = list(values.keys())

    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)

    if message.author == bot.user:
        return
    if True:#message.channel.name == 'general':

        if user_message.lower() == "beam":
            user_message = "beam hybrid"
        if user_message.lower() == "ice":
            user_message = "ice breaker"
        if user_message.lower() == "torp":
            user_message = "torpedo"
        if user_message.lower() == "crew":
            user_message = "crew capsule"
        if user_message.lower() == "banana":
            user_message = "banana car"
        if user_message.lower() == "rtx":
            user_message = "RTx"

        itemlow = get_close_matches(user_message,names,1,0.4)[0]
        item = itemlow.capitalize()
        update_date = str(values[itemlow][4])
        embed=discord.Embed(title=item, color=0x00ff1e)
        embed.set_thumbnail(url = (values[itemlow][0]))
        embed.add_field(name="Clean Value", value = f"`{values[itemlow][1]}`", inline=False)
        embed.add_field(name="Duped Value", value = f"`{values[itemlow][2]}`", inline=False)
        embed.add_field(name="Demand", value = f"`{values[itemlow][3]}`", inline=False)
        embed.add_field(name="Last Updated", value = f"`{update_date}`", inline=False)
        #embed.set_footer(text= f"Powered by JBC | discord.gg/jbc")
        await message.channel.send(embed=embed, reference = message)



bot.run(Token.TOKEN)
