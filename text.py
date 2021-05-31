import discord
from discord.ext import commands, tasks
#print(discord.__version__)
import random # cause to give random responses in _8ball command below
import os # for cogs
import asyncio # for to sleep , (for converters)
from itertools import cycle  # for looping 

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='.',intents=intents )


@client.event
async def on_ready():
    #message.start()
    #code to change status of the bot
    await client.change_presence(status= discord.Status.idle, activity=discord.Game('Hello everyone!! Nice to have you guys over here'))
    change_status.start()  # for loop to change status 
    # Need to add bot activity
    print("BOT is ready")


@client.event
async def on_member_join(member):
    await member.send(f"Hello, {member.mention}! Great to have you here!")
    await client.get_channel(848570120611168329).send(f"Hello {member.mention} welcome to our channel , Let's have fun time !")
    print(f'{member}has joined') #it dispalys the message on powershell


@client.event
async def on_member_remove(member):
    await client.get_channel(848570120611168329).send(f"I hope {member.mention} had fun!")
    print(f'{member}has left the server') #it displays the meaage on powershell



@client.command()
async def ping(ctx):
    await ctx.send(f"Ping: {round(client.latency * 1000)} ms") # time to take to reply to msg with ping in ms
# type .ping to execute this command on discord


@client.command(aliases=['8ball','test']) # aliases is the function that holds a list of strings, all the strings in the list are used to envoke the command 
async def _8ball(ctx,*,question):
    responses = ['yes',
                 'Cannot predict you idiot',
                 'My reply is no',
                 'concentrate and ask again',
                 'very doubtful.',
                 'better not tell you now',
                 'you suck',
                 'you are very ugly UKT?.',
                 'Outlook is good',
                 'Hell yeah bitch',
                 'Most likely',
                 'My sources says no'
                 'ask someone else'
                 'i am pretty busy right now']
    await ctx.send(f'Questions : {question} \nAnswer :  {random.choice(responses)}')
# for this type [ .8ball (your random question) ] on discord , you will get reply with the question you asked and with random reply


@client.command()
async def hello(ctx):
    # Accesses member object (in this case the author of the message) and sends them a DM while mentioning them
    await ctx.send(f"Hello {ctx.author.mention}!")


# @client.command()
# async def clear(ctx,amount=10):
#     # Purges last 10 messages in the channel
#     await ctx.channel.purge(limit=amount)


@client.command()
async def kick(ctx, member : discord.Member,*, reason= None): # discord.member helps us to see the person who got kicked out from the server
    await member.kick(reason=reason)



############################ Ban and Unban #######################
#Ban is similer to kick
# @client.command()
# async def ban(ctx, member : discord.Member,*, reason= None):
#     await member.ban(reason=reason)
#     await ctx.send(f'Banned {member.mention}')
#check whether the person is banned or not by going to the server setting and check in Audit log

#Unban command
@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator =  member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'unbanned {user.mention}')
            return


#########___COGS____#########################

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')  # :-3 eliminates the last 3 character from the filename

#############################################


@client.command()
async def greet(ctx, greeting, *, name):
    await ctx.send(f"{greeting}, {name}")


##################loop########################

status = cycle(['status 1', 'status 2'])
@tasks.loop(seconds=2)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

# async def message():
#     # Creates a loop that sends messages to a particular channel on 2 second intervals
#     await client.get_channel(848570120611168326).send("Hello")

############################################



#############EROR ##########################

# @client.command()
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send('Please pass in all required arguemnts')

   
#if wrong tests are used,then it will warn you   
@client.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command is used, so make sure you're right")

  

@client.command()
async def clear(ctx,amount : int):
    # Purges last 10 messages in the channel
    await ctx.channel.purge(limit=amount)
  


# @client.command(pass_context=True)
# async def clear(ctx, amount=100):
#     channel = ctx.message.channel
#     messages = []
#     async for message in client.logs_from(channel,limit=int(amount) + 1 ):
#         messages.append(message)
#     await client.delete_messages(messages)    
#     await client.say('messages deleted')


@clear.error
async def clear_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an amount of message to delete')

###############################################


#############Check to permisssions############

# @client.command()
# @commands.has_permissions(manage_messages=True)  #it changes a permission to other people to clear the messages
# async def clear(ctx,amount=10):
#     # Purges last 10 messages in the channel
#     await ctx.channel.purge(limit=amount)

# ##custom check

# def is_it_me(ctx):
#     return ctx.author.id == 758581998318649364        #This will allow permission to test the program who has the id here

# @client.command()
# @commands.check(is_it_me)
# async def example(ctx):
#     await ctx.send(f'Hi im {ctx.author}')

#################################


############## __converters__ ########################

#########this code bans the user for given amount of time ################
class DurationConverter(commands.Converter):
    async def convert(self,ctx,argument):
        amount= argument[:-1]
        unit= argument[-1]

        if amount.isdigit() and unit in ['s','m']:
            return(int(amount), unit)
        
        raise commands.BadArgument(message='Not a valid duration')

@client.command()
async def temban(ctx, member: commands.MemberConverter, duration : DurationConverter):

    multiplier = {'s':1 ,'m': 60}
    amount, unit = duration


    await ctx.guild.ban(member)
    await ctx.send(f'{member} has been banned for {amount}{unit}.')
    await asyncio.sleep(amount*multiplier[unit])
    await ctx.guild.unban(member)


#this to work give test code as --- .temban @---- 18s 


#######################################################


#####display the deleted msgs by bot and displys the user with messsges on poweshell

# @client.event
# async def on_message(message):
#     author = message.author
#     content = message.content
#     print('{}: {}'.format(author,content))


# @client.event
# async def on_message_delete(message):
#     author = message.author
#     content = message.content
#     channel = message.channel
#     print('{}: {}'.format(author,content))
    #await client.send_message('{}: {}'.format(author,content))


##############################################################




# @client.command()
# async def test(ctx, member: discord.Member):
#     await ctx.send(member.display_name) # first show with .nick



# @client.command(aliases=['embed'])
# async def test_embed(ctx):
#     embed = discord.Embed(title="Discord.py Workshop", color=discord.Color.green())
#     embed.add_field(name="Hello", value="Welcome to the Discord.py Workshop", inline=False)
#     embed.add_field(name="Instructor", value="Suhas Thalanki", inline=False)
#     #https://cog-creators.github.io/discord-embed-sandbox/
#     await ctx.send(embed=embed)

# @client.command()
# async def nick(ctx, member: discord.Member, newname: str):
#     # Gets permissions that the message sender has
#     perms = ctx.channel.permissions_for(ctx.author)
#     if perms.manage_nicknames:
#         # If the sender can edit nicknames, edit
#         await member.edit(nick=newname)
#     else: 
#         await ctx.send("Don't  have necessary permissions")

# @client.command()
# async def role(ctx, member: discord.Member, role: discord.Role):
#     # Give the mentioned person a role
#     await member.add_roles(role)



#Need to add embeds

client.run("ODQ4NTM1NjQ3MTk5MDM1Mzkz.YLOCZw.I24q2CECSuw4tJevJNhqWRocnl8")