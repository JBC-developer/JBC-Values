import discord
from discord.ext import commands
from discord import app_commands
import Token
import numpy as np
from difflib import *
import typing
from datetime import datetime
from datetime import date
import validators

import test
from keep_alive import keep_alive

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

msg = '''**Setting up VALUE BOT:**
1. Make a channel for the value bot
2. Please use the command /setup_value_bot
3. Select the channel that you just made. Keep in mind that the bot will not respond in any other channel
(You can change the channel by using /setup_value_bot command again)

**Setting up GRINDING BOT:**
1. Make a channel for the grinding bot
2. Make a role called "Grinding Ping"
3. Use the command /setup_grinding_bot
4. Select the channel you just made. Keep in mind that the bot will not respond in any other channel.
5. Select the role "Grinding Ping"

**Note:**
If the value bot does not work, make sure it has these permissions in the specified channel:
`View channel`, `Send messages`, `Read message history,` `Embed links`

If the grinding bot does not work, make sure it has these permissions in the specified channel:
`View channel`, `Send messages`, `Read message history,` `Embed links`, `Mention all roles`

Kindly turn on `Create invite` for our convenience, but the bot will work without it.

**Value Lists:**
[JBC Value List](<https://docs.google.com/spreadsheets/d/1mKz2YsgKevFvPI08XU7vCiaPBnUH9OvFzjBSO6TCvPg/edit#gid=1658217925>)

**Bot Owner:**
<@857892645543215116> `jailbreakduck | 857892645543215116`

**Bot Developer:** 
<@745583659389681675> `hydraulic4128 | 745583659389681675`

**Server Count:**
INSERT HERE

**Credits:**
[JBC](<https://discord.com/invite/jbc>)
[Auto Creavite](<https://auto.creavite.co/>)

**Other questions or concerns?**
Join our [Support & Development Server](<https://discord.gg/5wtYzKGn6u>)
Terms of Service can be accessed [here](<https://docs.google.com/document/d/1AbPgAUexIxxN6qIX5QOjK3TiWVF4_FR-62d1zoQOFIQ/edit>)'''

class MyView2(discord.ui.View):
    @discord.ui.select(
        cls=discord.ui.ChannelSelect,
        placeholder = "Choose a channel for the bot to work in",
        channel_types=[discord.ChannelType.text]
    )
    @commands.has_permissions(administrator = True)
    @app_commands.checks.has_permissions(administrator=True)
    async def select_callback(self, interaction, select):
        if not interaction.user.resolved_permissions.administrator:
            return
        channel_dict = dict(np.load('Channel_Dict_grind.npy', allow_pickle=True).item())
        channel = select.values[0]
        try:
            channel_dict[int(interaction.guild.id)] = ['','','']
            channel_dict[int(interaction.guild.id)][0] = int(channel.id)
        except Exception as e:
            print(e)

        np.save('Channel_Dict_grind.npy', channel_dict)
        try:
            await interaction.response.defer()
            await interaction.message.delete()
            embed=discord.Embed(title='The bot has been setup to work here',description = "Use /grind to generate Grinding pings!", color=0x11fa00)
            channel = bot.get_channel(int(channel.id))
            await channel.send(embed = embed)
            #await interaction.channel.send(f"The bot has been setup to work in {select.values[0]}")
            await interaction.channel.send("Please select the Grinding ping role - ", view=MyView3())
        except:
            embed=discord.Embed(title='**Important**',description = f"The bot has been setup to work in {select.values[0]}, but it cannot function right now\nPlease check the permissions of the bot in the {select.values[0]} channel\nMake sure it has these permissions:\n`Send Messages`, `Embed links` and `Attach files`\nThe bot will not work until it has these permissions", color=0xff0000)
            await interaction.channel.send(embed = embed)

class MyView1(discord.ui.View):
    @discord.ui.select(
        cls=discord.ui.ChannelSelect,
        placeholder = "Choose a channel for the bot to work in",
        channel_types=[discord.ChannelType.text]
    )
    @commands.has_permissions(administrator = True)
    @app_commands.checks.has_permissions(administrator=True)
    async def select_callback(self, interaction, select):
        channel_dict = dict(np.load('Channel_Dict.npy', allow_pickle=True).item())
        channel = select.values[0]
        channel_dict[int(interaction.guild.id)] = int(channel.id)

        np.save('Channel_Dict.npy', channel_dict)
        try:
            await interaction.response.defer()
            embed=discord.Embed(title='The bot has been setup to work here',description = "Type the name of the item you want to know the value of", color=0x11fa00)
            channel = bot.get_channel(int(channel.id))
            await channel.send(embed = embed)
            await interaction.channel.send(f"The bot has been setup to work in {select.values[0]}")
        except:
            embed=discord.Embed(title='**Important**',description = f"The bot has been setup to work in {select.values[0]}, but it cannot function right now\nPlease check the permissions of the bot in the {select.values[0]} channel\nMake sure it has these permissions:\n`Send Messages`, `Read message history`, `Embed links` and `Attach files`\nThe bot will not work until it has these permissions", color=0xff0000)
            await interaction.channel.send(embed = embed)

class MyView3(discord.ui.View):
    @discord.ui.select(
        cls=discord.ui.RoleSelect,
        placeholder = "Choose the Grinding ping role",
    )

    async def select_callback(self, interaction, select):
        if not interaction.user.resolved_permissions.administrator:
            return
        channel_dict = dict(np.load('Channel_Dict_grind.npy', allow_pickle=True).item())
        channel = select.values[0]
        try:
            channel_dict[int(interaction.guild.id)][1] = int(channel.id)
        except Exception as e:
            print(e)
        
        np.save('Channel_Dict_grind.npy', channel_dict)
        await interaction.response.defer()
        await interaction.message.delete()
        #await interaction.channel.send(f"The bot has been setup to work with the role <@&{select.values[0].id}>")
        await interaction.channel.send("Please select the cooldown for /grind (in minutes) - ", view=MyView4())

class MyView4(discord.ui.View):
    @discord.ui.select(
        placeholder = "Choose the cooldown for Grinding ping (in minutes)",
        options=[discord.SelectOption(label="30", description="30 minutes cooldown"),
                 discord.SelectOption(label="45", description="45 minutes cooldown"),
                 discord.SelectOption(label="60", description="60 minutes cooldown"),
                 discord.SelectOption(label="90", description="90 minutes cooldown"),
                 discord.SelectOption(label="120", description="120 minutes cooldown"),
                 discord.SelectOption(label="150", description="150 minutes cooldown"),
                 discord.SelectOption(label="180", description="180 minutes cooldown"),
                 discord.SelectOption(label="240", description="240 minutes cooldown"),
                 discord.SelectOption(label="600", description="600 minutes cooldown")]
    )

    async def select_callback(self, interaction, select):
        if not interaction.user.resolved_permissions.administrator:
            return
        channel_dict = dict(np.load('Channel_Dict_grind.npy', allow_pickle=True).item())
        channel = select.values[0]
        try:
            channel_dict[int(interaction.guild.id)][2] = int(channel)
        except Exception as e:
            print(e)
        
        np.save('Channel_Dict_grind.npy', channel_dict)
        await interaction.response.defer()
        await interaction.message.delete()
        embed = discord.Embed(title="**Success!**", description=f"The bot has been setup to work in {bot.get_channel(channel_dict[int(interaction.guild.id)][0])}, with grinding ping <@&{channel_dict[int(interaction.guild.id)][1]}> and cooldown {channel_dict[int(interaction.guild.id)][2]} minutes", color=0x00ff00)
        await interaction.channel.send(embed=embed)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/help"))

    print("Im jbc bot")
    channel_dict = dict(np.load('Channel_Dict.npy', allow_pickle=True).item())

    i = 0
    for guild in bot.guilds:
        i = i + 1
    msg = f'''It seems that you have added our bot to your server but it has not been set up yet. Here is how to do it!
    
**Setting up:**
1. Please use the command /setup_value_bot
2. Select the channel that you want the bot to work in. Keep in mind that it will not respond in any other channel
3. Enjoy!
(You can change the channel by using /setup_value_bot command again)

**Note:**
If the bot does not work, make sure it has these permissions in the specified channel -
`View channel`, `Send messages`,`Read message history`, `Embed links`

Kindly turn on `Create invite` for our convenience, but the bot will work without it.
'''
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



@bot.tree.command(name="setup_value_bot", description = "Choose a channel for the value bot to reply in")
@commands.has_permissions(administrator = True)
@app_commands.checks.has_permissions(administrator=True)
async def setup_value_bot(interaction : discord.Interaction):
    await interaction.response.send_message('Thanks for using our value bot! Please select a channel for it to work in - ', view = MyView1(), ephemeral=True)



@setup_value_bot.error
async def setup_value_bot_error(interaction :  discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("You have no permissions to run this command", ephemeral=True)

@bot.tree.command(name="setup_grinding_bot", description = "Choose a channel for the grinding bot to work in")
@commands.has_permissions(administrator = True)
@app_commands.checks.has_permissions(administrator=True)
async def setup_grinding_bot(interaction : discord.Interaction):
    await interaction.response.send_message('Thanks for using our grinding bot! Please select a channel for it to work in - ', view = MyView2())


@setup_grinding_bot.error
async def setup_value_bot_error(interaction :  discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("You have no permissions to run this command", ephemeral=True)

@bot.tree.command(name="reset_grinding_cooldown", description = "Reset cooldown for the server")
@commands.has_permissions(administrator = True)
@app_commands.checks.has_permissions(administrator=True)
async def reset_grinding_cooldown(interaction : discord.Interaction):
    cooldown = np.load('cooldown.npy', allow_pickle=True).item()
    id = int(interaction.guild.id)
    del cooldown[id]
    np.save('cooldown.npy', cooldown)
    await interaction.response.send_message('Cooldown reset', ephemeral=True)

@reset_grinding_cooldown.error
async def reset_grinding_cooldown_error(interaction :  discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("You have no permissions to run this command", ephemeral=True)
    

@bot.tree.command(name="grind", description="Generate a ping for players to grind with you!")
@app_commands.describe(amount_of_people = "The amount of people to grind with", server_type = "Private or public", server_link = "Link to the grinding server")
async def grind(interaction : discord.Interaction, amount_of_people : typing.Literal['1','2',
    '3','4',
    '5','6',
    '7','8',
    '9','10',
    '11','12',
    '13','14',
    '15','16',
    '17','18',
    '19','20',
    '21','22',
    '23','24',
    '25'], server_type : typing.Literal['Public','Private'], server_link : typing.Optional[str] = ''):
    banned = np.load("Banned.npy", allow_pickle=True).item()
    if interaction.user.id in list(banned.keys()):
        if banned[interaction.user.id]:
            return
    channel_dict = dict(np.load('Channel_Dict_grind.npy', allow_pickle=True).item())
    if interaction.guild.id not in list(channel_dict.keys()):
        await interaction.response.send_message('The grinding bot has not been setup yet. Please ask a server admin to set it up', ephemeral=True)
        return

    if channel_dict[interaction.guild.id][0] != interaction.channel_id:
        return
    
    if server_link == '' and server_type == "Private":
        await interaction.response.send_message('You have to specify a link if playing on a private server.', ephemeral=True)
        return
    if server_link != '' and server_type == "Public":
        await interaction.response.send_message('You cannot specify a link if playing on a public server.', ephemeral=True)
        return
    
    current_time = datetime.now().strftime("%H:%M:%S")
    current_time = datetime.now().strptime(current_time, "%H:%M:%S")
    current_date = date.today()

    id = int(interaction.guild.id)

    cooldown = np.load("cooldown.npy", allow_pickle=True).item()
    if id in list(cooldown.keys()):
        prev_time = cooldown[id][0]
        prev_date = cooldown[id][1]

        difference_time = current_time - prev_time
        difference_date = (current_date - prev_date).days

        difference_time = difference_time.total_seconds()/60
        

        if ((int(difference_time) < int(channel_dict[interaction.guild.id][2]) and int(difference_date) == 0)):
            if (int(difference_date) > 0):
                pass
            else:
                await interaction.response.send_message(f"The server is on cooldown for {int(channel_dict[interaction.guild.id][2] - difference_time)} minutes", ephemeral=True)
                return
    if (validators.url(server_link) and "https://www.roblox.com/" in server_link) or (server_link == ''):
        cooldown[id] = ['','']
        cooldown[id][0] = current_time
        cooldown[id][1] = current_date
        np.save("cooldown.npy", cooldown)

        #server_link = "https://www.roblox.com/games/606849621/Jailbreak-Saturday?privateServerLinkCode=35811044437989989744211517148641"

        
        m = f'''**Host:** <@{interaction.user.id}>
**Amount of people:** {amount_of_people}
**Server Type:** {server_type}'''
        embed = discord.Embed(title="**Grinding session**", description=m)
        embed.set_image(url = "https://cdn.discordapp.com/attachments/1185575193989632051/1230055721593208886/standard_8.gif?ex=6631eda9&is=661f78a9&hm=71b0fe539f0a61b6ef645a6a92f131ec98f3bb511441b106d425be447af70ac7&")
        button = discord.ui.Button(label="Get link", style=discord.ButtonStyle.green)

        user_list = []
        async def button_callback(interaction1 : discord.Interaction):
            user_id = interaction1.user.id
            user = bot.get_user(int(user_id))
            if user not in user_list:
                embed1 = discord.Embed(title="**Grinding session**", description=f"[Join here](<{server_link}>)")
                await interaction1.response.send_message(embed=embed1, ephemeral=True)
                user_list.append(user)
            else:
                embed1 = discord.Embed(title="**Grinding session**", description=f"[Join here](<{server_link}>)")
                await interaction1.response.send_message(embed=embed1, ephemeral=True)
            #await interaction1.response.defer()
            if len(user_list) >= int(amount_of_people):
                button.disabled = True
                view = discord.ui.View()
                view.add_item(button)
                await interaction.edit_original_response(embed=embed, view=view)
        
        button.callback = button_callback

        view = discord.ui.View()
        view.add_item(button)

        if server_type == "Private":
            await interaction.response.send_message(embed=embed, view=view)
        else:
            await interaction.response.send_message(embed=embed)
        role = channel_dict[interaction.guild.id][1]
        try:
            await interaction.channel.send(f"<@&{role}>")
        except:
            await interaction.channel.send('The bot could not ping due to missing permissions.')
    else:
        await interaction.response.send_message("There is a problem with the link. Make sure it works and starts with 'https://'", ephemeral=True)




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
        await interaction.channel.send(file = discord.File('Channel_Dict_grind.npy'))
        await interaction.response.send_message(file = discord.File('Channel_Dict.npy'))
    except:
        pass


@bot.tree.command(name="list_servers")
async def list_servers(interaction : discord.Interaction):
    dev_id = ["745583659389681675", "857892645543215116"]
    if (str(interaction.user.id) not in dev_id):
        await interaction.response.send_message("This command is only for the Bot owner and Bot developer.", ephemeral = True)
        return
    await interaction.response.send_message("Creating links...")
    for guild in bot.guilds:
        try:
            link = await guild.text_channels[0].create_invite(reason=f"Requested by Bot owner/developer")
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
    await interaction.response.send_message("Announcing...", ephemeral = True)
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
    await interaction.edit_original_response(content="The message has been announced")


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
    msg = f'''**Commands:**
/help - Get help and information about the bot
/setup_value_bot - Setup the value bot
/setup_grinding_bot - Setup the grinding bot
/grind - Generate a ping for players to grind with you!

**Setting up VALUE BOT:**
1. Make a channel for the value bot
2. Please use the command /setup_value_bot
3. Select the channel that you just made. Keep in mind that the bot will not respond in any other channel
(You can change the channel by using /setup_value_bot command again)

**Setting up GRINDING BOT:**
1. Make a channel for the grinding bot
2. Make a role called "Grinding Ping"
3. Use the command /setup_grinding_bot
4. Select the channel you just made. Keep in mind that the bot will not respond in any other channel.
5. Select the role "Grinding Ping"

**Note:**
If the value bot does not work, make sure it has these permissions in the specified channel:
`View channel`, `Send messages`, `Read message history,` `Embed links`

If the grinding bot does not work, make sure it has these permissions in the specified channel:
`View channel`, `Send messages`, `Read message history,` `Embed links`, `Mention all roles`

Kindly turn on `Create invite` for our convenience, but the bot will work without it.

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
        if user_message.lower() == "jav":
            user_message = "javelin"
        if user_message.lower() == "arach":
            user_message = "arachnid"
        if user_message.lower() == "cel":
            user_message = "celsior"
        if user_message.lower() == "carb":
            user_message = "carbonara"
        if user_message.lower() == "carbon":
            user_message = "carbonara"
        if user_message.lower() == "p1" or user_message.lower() == "p 1":
            user_message = "power 1"
        if user_message.lower() == "air":
            user_message = "airtail"
        if user_message.lower() == "volt":
            user_message = "volt bike"
        
        for color in ['red','blue','green','purple', 'diamond', 'orange', 'pink', 'yellow']:
            if color in user_message.lower():
                for num in [2,3,4,5]:
                    if str(num) in user_message.lower():
                        user_message = "Hyper " + user_message.lower()
        
        if user_message.lower() == "hyper red 50":
            user_message = "red 50"
        if user_message.lower() == "hyper blue 50":
            user_message = "blue 50"

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
    msg = f'''**Setting up VALUE BOT:**
1. Make a channel for the value bot
2. Please use the command /setup_value_bot
3. Select the channel that you just made. Keep in mind that the bot will not respond in any other channel
(You can change the channel by using /setup_value_bot command again)

**Setting up GRINDING BOT:**
1. Make a channel for the grinding bot
2. Make a role called "Grinding Ping"
3. Use the command /setup_grinding_bot
4. Select the channel you just made. Keep in mind that the bot will not respond in any other channel.
5. Select the role "Grinding Ping"

**Note:**
If the value bot does not work, make sure it has these permissions in the specified channel:
`View channel`, `Send messages`, `Read message history,` `Embed links`

If the grinding bot does not work, make sure it has these permissions in the specified channel:
`View channel`, `Send messages`, `Read message history,` `Embed links`, `Mention all roles`

Kindly turn on `Create invite` for our convenience, but the bot will work without it.

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
