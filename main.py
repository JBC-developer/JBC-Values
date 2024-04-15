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

class MyView(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        select_type=discord.ComponentType.channel_select,
        placeholder = "Choose a channel for the bot to work in",
        channel_types=[discord.ChannelType.text]
    )
    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        select.disabled = True
        channel_dict = dict(np.load('Channel_Dict.npy', allow_pickle=True).item())
    
        channel = select.values[0]
        channel_dict[interaction.guild.id] = channel.id

        np.save('Channel_Dict.npy', channel_dict)
        await interaction.channel.send(f"The bot has been setup to work in {select.values[0].mention}")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/help"))

    print("Im jbc bot")
    channel_dict = dict(np.load('Channel_Dict.npy', allow_pickle=True).item())

    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)

    for guild in bot.guilds:
        if guild.id not in list(channel_dict.keys()):
            channel = guild.text_channels[0]
            await channel.send('The bot has not been set up. Please use /setup and select the channel for it to work in')
    
    values = np.load('ValueList.npy', allow_pickle=True).item()

    k = list(values.keys())
    v = list(values.values())
    img = []
    for va in v:
        img.append(va[0])
    images = {}
    images = {k: img for k, img in zip(k,img)}

    test.main(images)



@bot.tree.command(name="setup")
@commands.has_permissions(administrator = True)
@app_commands.checks.has_permissions(administrator=True)
async def setup(interaction : discord.Interaction):
    await interaction.response.send_message('Thanks for using our bot! Please select a channel for it to work in - ', view = MyView())
    
    '''try:
        channel = bot.get_channel(int(channel_id)).name
        channel_dict[interaction.guild.id] = channel_id

        np.save('Channel_Dict.npy', channel_dict)
        await interaction.response.send_message(f'The bot has been set to work in the channel {channel}')
    except Exception as e:
        await interaction.response.send_message(f'There is no channel with that channel ID')
        print(e)'''



@setup.error
async def setup_error(interaction :  discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("You have no permissions to run this command", ephemeral=True)


'''
@bot.tree.command(name="valuechange")
@commands.has_permissions(administrator = True)
@app_commands.describe(item = "The item you want to change", value = "New value", dupe_value = "Duped value", demand = "New demand")
@app_commands.checks.has_permissions(administrator=True)
async def valuechange(interaction : discord.Interaction, item : str, value : str, dupe_value : str, demand : str):

    item = get_close_matches(item,names,1,0.4)[0]
    channel = interaction.channel

    await interaction.response.send_message(f'Do you want to change the value of {item}?')
    
    def check(message : discord.Message):
        return True
    
    try:
        msg = await bot.wait_for('message', check= check, timeout= 10)
    except asyncio.TimeoutError:
        return await channel.send("You took too long")

    else:
        m = get_close_matches(msg.content, ['yes','no'], 1, 0.6)[0]
        if m == 'yes':
            update_date = str(date.today())
            update_date = datetime.strptime(update_date, '%Y-%m-%d').strftime('%d/%m/%Y')
            values[item] = [values[item][0], value, dupe_value, demand, update_date]

            names = list(values.keys())

            np.save('ValueList.npy',values)
            return await channel.send(f'Changed the value of {item} to {value}, duped value to {dupe_value} and demand to {demand}')

        else:
            return await channel.send("Try to be more accurate. If you want to add an item, use /valueadd")



@bot.tree.command(name="valueadd")
@commands.has_permissions(administrator = True)
@app_commands.describe(item = "The item you want to add", value = "Value", dupe_value = "Duped value", demand = "Demand", image ="Link to image")
@app_commands.checks.has_permissions(administrator=True)
async def valueadd(interaction : discord.Interaction, item : str, value : str, dupe_value : str, demand : str, image :str):
    try:
        item = item.lower()
        item = item.capitalize()

        update_date = str(date.today())
        update_date = datetime.strptime(update_date, '%Y-%m-%d').strftime('%d/%m/%Y')

        values[item] = [image, value, dupe_value, demand, update_date]

        names = list(values.keys())

        np.save('ValueList.npy',values)
        await interaction.response.send_message(f'Added {item} with the value {value}, duped value {dupe_value} and demand {demand}')
    except:
        await interaction.response.send_message('Some error')   




@valuechange.error
async def valuechange_error(interaction :  discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("You have no permissions to run this command", ephemeral=True)
    #await interaction.response.send_message("No perms", ephemeral=True)



@valueadd.error
async def valueadd_error(interaction :  discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("You have no permissions to run this command", ephemeral=True)
'''


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
    await interaction.response.send_message(embed=embed)



@bot.event
async def on_message(message):
    channel_dict = dict(np.load('Channel_Dict.npy', allow_pickle=True).item())
    if(message.guild.id not in list(channel_dict.keys())):
        return
    if(str(message.channel.id) != channel_dict[message.guild.id]):
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

        itemlow = get_close_matches(user_message,names,1,0.4)[0]
        item = itemlow.capitalize()
        update_date = str(values[itemlow][4])
        embed=discord.Embed(title=item, color=0x00ff1e)
        embed.set_thumbnail(url = (values[itemlow][0]))
        embed.add_field(name="Clean Value", value = f"`{values[itemlow][1]}`", inline=False)
        embed.add_field(name="Duped Value", value = f"`{values[itemlow][2]}`", inline=False)
        embed.add_field(name="Demand", value = f"`{values[itemlow][3]}`", inline=False)
        embed.add_field(name="Last Updated", value = f"`{update_date}`", inline=False)
        embed.set_footer(text= f"Powered by JBC | discord.gg/jbc")
        await message.channel.send(embed=embed)



@bot.event
async def on_guild_join(guild):
    channel = guild.text_channels[0]
    await channel.send("Hello! Thank you for using the JBC value bot.\nIt uses JBC's value list | discord.gg/jbc\nPlease set the bot up by using /setup and select the channel you want the bot to be used in.\nUse /help for the list of commands")

bot.run(Token.TOKEN)
