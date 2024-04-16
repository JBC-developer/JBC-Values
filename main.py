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

msg = '''**Setting up:**
1. Please use the command /setup
2. Select the channel that you want the bot to work in. Keep in mind that it will not respond in any other channel
3. Enjoy!
(You can change the channel by using /setup command again)

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
    @commands.has_permissions(administrator = True)
    @app_commands.checks.has_permissions(administrator=True)
    async def select_callback(self, interaction, select): # the function called when the user is done selecting options
        #if !(interaction.user.guild_permissions.administrator):
            #return
        channel_dict = dict(np.load('Channel_Dict.npy', allow_pickle=True).item())
        channel = select.values[0]
        channel_dict[int(interaction.guild.id)] = int(channel.id)

        np.save('Channel_Dict.npy', channel_dict)
        try:
            embed=discord.Embed(title='The bot has been setup to work here',description = "Type the name of the item you want to know the value of", color=0x11fa00)
            channel = bot.get_channel(int(channel.id))
            await channel.send(embed = embed)
            await interaction.channel.send(f"The bot has been setup to work in {select.values[0]}")
        except:
            embed=discord.Embed(title='**Important**',description = f"The bot has been setup to work in {select.values[0]}, but it cannot function right now\nPlease check the permissions of the bot in the {select.values[0]} channel\nMake sure it has these permissions:\n`Send Messages`, `Embed links` and `Attach files`\nThe bot will not work until it has these permissions", color=0xff0000)
            await interaction.channel.send(embed = embed)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/help"))

    print("Im jbc bot")
    channel_dict = dict(np.load('Channel_Dict.npy', allow_pickle=True).item())

    i = 0
    for guild in bot.guilds:
        i = i + 1
    msg = f'''**Setting up:**
1. Please use the command /setup
2. Select the channel that you want the bot to work in. Keep in mind that it will not respond in any other channel
3. Enjoy!
(You can change the channel by using /setup command again)

**Value Lists:**
[JBC Value List](<https://docs.google.com/spreadsheets/d/1mKz2YsgKevFvPI08XU7vCiaPBnUH9OvFzjBSO6TCvPg/edit#gid=1658217925>)

**Bot Owner:**
<@857892645543215116> `jailbreakduck | 857892645543215116`

**Bot Developer:** 
<@745583659389681675> `hydraulic4128 | 745583659389681675`

**Server Count:**
{i}

**Credits:**
[JBC](<https://discord.com/invite/jbc>)
[Auto Creavite](<https://auto.creavite.co/>)

**Other questions or concerns?**
Join our [Support & Development Server](<https://discord.gg/5wtYzKGn6u>)
Terms of Service can be accessed [here](<https://docs.google.com/document/d/1AbPgAUexIxxN6qIX5QOjK3TiWVF4_FR-62d1zoQOFIQ/edit>)'''
    embed=discord.Embed(title="**Hi there!**", description=msg)

    owners = []
    
    for guild in bot.guilds:
        if(int(guild.id)) not in list(channel_dict.keys()):
            try:
                owner = bot.get_user(int(guild.owner.id))
                if owner not in owners:
                    await owner.send(embed = embed)
                    owners.append(owner)
            except:
                owner = bot.fetch_user(int(guild.owner.id))
                if owner not in owners:
                    await owner.send(embed = embed)
                    owners.append(owner)
    
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



@bot.tree.command(name="setup", description = "Choose a channel for the bot to reply in")
@commands.has_permissions(administrator = True)
@app_commands.checks.has_permissions(administrator=True)
async def setup(interaction : discord.Interaction):
    await interaction.response.send_message('Thanks for using our bot! Please select a channel for it to work in - ', view = MyView(), ephemeral=True)



@setup.error
async def setup_error(interaction :  discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("You have no permissions to run this command", ephemeral=True)

@bot.tree.command(name="ban", description = "Ban a user")
@app_commands.describe(user_id = "The ID of the user to ban")
async def ban(interaction : discord.Interaction, user_id : str):
    dev_id = ["745583659389681675", "857892645543215116"]
    if (str(interaction.user.id) not in dev_id):
        await interaction.response.send_message("This command is only for the Bot owner and Bot developer.\nIf you want to report a user, please do so in our [Discord Server](<https://discord.gg/5wtYzKGn6u>)", ephemeral = True)
        return
    if (user_id in dev_id):
        await interaction.response.send_message("You can't ban this person, he's too awesome", ephemeral =True)
        return
    banned = np.load("Banned.npy", allow_pickle=True).item()
    banned[int(user_id)] = True
    np.save("Banned.npy", banned)
    await interaction.response.send_message("The mentioned user has been banned", ephemeral = True)

@bot.tree.command(name="unban", description = "Unban a user")
@app_commands.describe(user_id = "The ID of the user to unban")
async def unban(interaction : discord.Interaction, user_id : str):
    dev_id = ["745583659389681675", "857892645543215116"]
    if (str(interaction.user.id) not in dev_id):
        await interaction.response.send_message("This command is only for the Bot owner and Bot developer.\nIf you want to appeal, please do so in our [Discord Server](<https://discord.gg/5wtYzKGn6u>)", ephemeral = True)
        return
    if (user_id in dev_id):
        await interaction.response.send_message("You can't ban this person, he's too awesome to be banned in the first place.", ephemeral =True)
        return
    banned = np.load("Banned.npy", allow_pickle=True).item()
    banned[int(user_id)] = False
    np.save("Banned.npy", banned)
    await interaction.response.send_message("The mentioned user has been unbanned", ephemeral = True)

@bot.tree.command(name="list_ban", description = "List all banned users")
async def list_ban(interaction : discord.Interaction):
    dev_id = ["745583659389681675", "857892645543215116"]
    if (str(interaction.user.id) not in dev_id):
        await interaction.response.send_message("This command is only for the Bot owner and Bot developer.", ephemeral = True)
        return
    banned = np.load("Banned.npy", allow_pickle=True).item()
    for id in list(banned.keys()):
        if banned[id]:
            await interaction.channel.send(id)
            
@bot.tree.command(name="list_channels")
async def list_channels(interaction : discord.Interaction):
    dev_id = ["745583659389681675", "857892645543215116"]
    if (str(interaction.user.id) not in dev_id):
        await interaction.response.send_message("This command is only for the Bot owner and Bot developer.", ephemeral = True)
        return
    channel_dict = np.load("Channel_Dict.npy", allow_pickle=True).item()
    k = list(channel_dict.keys())
    v = list(channel_dict.values())
    try:
        await interaction.response.send_message(file = discord.File('Channel_Dict.npy'))
    except:
        pass
    for ky in k:
        await interaction.channel.send(f"{ky} : {channel_dict[ky]}")


@bot.tree.command(name="list_servers")
async def list_servers(interaction : discord.Interaction):
    dev_id = ["745583659389681675", "857892645543215116"]
    if (str(interaction.user.id) not in dev_id):
        await interaction.response.send_message("This command is only for the Bot owner and Bot developer.", ephemeral = True)
        return
    await interaction.response.send_message("Creating links...")
    for guild in bot.guilds:
        try:
            link = guild.text_channels[0].create_invite(reason=f"Requested by Bot owner/developer")
            await interaction.channel.send(link)
        except:
            pass
        

@bot.tree.command(name="announce", description = "Announce something to every server")
@app_commands.describe(announcement = "The message to announce")
async def announce(interaction : discord.Interaction, announcement : str):
    dev_id = ["745583659389681675", "857892645543215116"]
    if (str(interaction.user.id) not in dev_id):
        await interaction.response.send_message("This command is only for the Bot owner and Bot developer.", ephemeral = True)
        return
    embed=discord.Embed(title="**Announcement!**", description=announcement)
    channel_dict = dict(np.load('Channel_Dict.npy', allow_pickle=True).item())

    owners = []
    
    for guild in bot.guilds:
        if int(guild.id) in list(channel_dict.keys()):
            try:
                channel = guild.get_channel(int(channel_dict[int(guild.id)]))
                await channel.send(embed = embed)
            except:
                channel = guild.fetch_channel(int(channel_dict[int(guild.id)]))
                await channel.send(embed = embed)
        try:
            owner = bot.get_user(int(guild.owner.id))
            if owner not in owners:
                await owner.send(embed=embed)
                owners.append(owner)
        except:
            owner = bot.fetch_user(int(guild.owner.id))
            if owner not in owners:
                await owner.send(embed=embed)
                owners.append(owner)
    await interaction.response.send_message("The message has been announced", ephemeral = True)


@bot.tree.command(name="valueupdate", description = "Update values from the value list")
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



@bot.tree.command(name="help", description = "Get help and information about the bot")
async def help(interaction: discord.Interaction):
    banned = np.load("Banned.npy", allow_pickle=True).item()
    if interaction.user.id in list(banned.keys()):
        if banned[interaction.user.id]:
            return
    i = 0
    for guild in bot.guilds:
        i = i + 1
    msg = f'''**Setting up:**
1. Please use the command /setup
2. Select the channel that you want the bot to work in. Keep in mind that it will not respond in any other channel
3. Enjoy!
(You can change the channel by using /setup command again)

**Value Lists:**
[JBC Value List](<https://docs.google.com/spreadsheets/d/1mKz2YsgKevFvPI08XU7vCiaPBnUH9OvFzjBSO6TCvPg/edit#gid=1658217925>)

**Bot Owner:**
<@857892645543215116> `jailbreakduck | 857892645543215116`

**Bot Developer:** 
<@745583659389681675> `hydraulic4128 | 745583659389681675`

**Server Count:**
{i}

**Credits:**
[JBC](<https://discord.com/invite/jbc>)
[Auto Creavite](<https://auto.creavite.co/>)

**Other questions or concerns?**
Join our [Support & Development Server](<https://discord.gg/5wtYzKGn6u>)
Terms of Service can be accessed [here](<https://docs.google.com/document/d/1AbPgAUexIxxN6qIX5QOjK3TiWVF4_FR-62d1zoQOFIQ/edit>)'''
    embed=discord.Embed(title="**Hi there!**", description=msg)
    await interaction.response.send_message(embed = embed)



@bot.event
async def on_message(message):
    channel_dict = dict(np.load('Channel_Dict.npy', allow_pickle=True).item())
    banned = np.load("Banned.npy", allow_pickle=True).item()
    if message.author.id in list(banned.keys()):
        if banned[message.author.id]:
            return
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

@bot.event
async def on_guild_join(guild):
    i = 0
    for guild in bot.guilds:
        i = i + 1
    msg = f'''**Setting up:**
1. Please use the command /setup
2. Select the channel that you want the bot to work in. Keep in mind that it will not respond in any other channel
3. Enjoy!
(You can change the channel by using /setup command again)

**Value Lists:**
[JBC Value List](<https://docs.google.com/spreadsheets/d/1mKz2YsgKevFvPI08XU7vCiaPBnUH9OvFzjBSO6TCvPg/edit#gid=1658217925>)

**Bot Owner:**
<@857892645543215116> `jailbreakduck | 857892645543215116`

**Bot Developer:** 
<@745583659389681675> `hydraulic4128 | 745583659389681675`

**Server Count:**
{i}

**Credits:**
[JBC](<https://discord.com/invite/jbc>)
[Auto Creavite](<https://auto.creavite.co/>)

**Other questions or concerns?**
Join our [Support & Development Server](<https://discord.gg/5wtYzKGn6u>)
Terms of Service can be accessed [here](<https://docs.google.com/document/d/1AbPgAUexIxxN6qIX5QOjK3TiWVF4_FR-62d1zoQOFIQ/edit>)'''
    embed=discord.Embed(title="**Hi there!**", description=msg)
    try:
        owner = bot.get_user(int(guild.owner.id))
        await owner.send(embed=embed)
    except:
        owner = bot.fetch_user(int(guild.owner.id))
        await owner.send(embed = embed)

bot.run(Token.TOKEN)
