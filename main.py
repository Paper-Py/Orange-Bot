#Do you want to steal my code?
import discord
from discord.ext import commands
import random
import wikipedia
import os
import keep_alive
import asyncio
from discord.ext.commands import has_permissions
import datetime
import json
from discord.ext.commands import BucketType
from discord.ext.commands import CommandOnCooldown
import math

from io import BytesIO

client = commands.Bot(command_prefix="%")

client.remove_command("help")

footer = "Orange Bot made by Not a vibing cat#5692"
ecolor = discord.Colour.red()


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('Do you like oranges? | Say "%cmds" for a list of commands.'))
    print("Bot operational.")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("This command is on cooldown, please retry in {}s.".format(math.ceil(error.retry_after)))
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing argument(s)!")
    if isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
            await ctx.send(_message)
            return
    

def wikis(sub):
    definition = wikipedia.summary(
        sub, sentences=3, chars=1000, auto_suggest=False, redirect=True)
    return definition


mainshop = [{"name":"Super-Orange", "price":100000000, "description":"This is the supreme orange!!!!!"},{"name":"Car", "price":20000, "description":"Move fast with this luxury vehicle!"},{"name":"Cookie", "price":10, "description": "Mmmm, it tastes so good, but an orange would be better!"},{"name":"Orange", "price":50, "description": "The best fruit!"},{"name":"Diamond", "price":1000000, "description": "Only the richest guys have this!"},{"name":"Phone", "price":200, "description": "Everybody has a smartphone this days!"},{"name":"Laptop", "price":500, "description": "Just an average laptop."}]

async def update_bank(user,change=0, mode = "wallet"):
    users = await get_bank_data()
    users[str(user.id)][mode] = users[str(user.id)][mode] + change
    with open('mainbank.json',"w") as f:
        json.dump(users,f)
    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return bal

async def get_bank_data():
        with open('mainbank.json', "r") as f:
            users = json.load(f)
        return users


async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False

    users[str(user.id)] = {"wallet": 0, "bank": 0}

    with open('mainbank.json',"w") as f:
        json.dump(users,f)
    return True

async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]


@client.command()
async def invite(ctx):
    await ctx.author.send(
        "Invite Link: https://discord.com/api/oauth2/authorize?client_id=782229157333434368&permissions=8&scope=bot"
    )


@client.command(aliases=["help"])
async def cmds(ctx):
    modadm = discord.Embed(
        title="Moderation & Administration:",
        description=
        "%clear `<amount>` - Clean a certain amount of messages from the current channel (mannage messages perm. required);\n%kick `<member>` `<reason>` - Kick a user (kick members perm. required);\n%ban `<member>` `<reason>` - Ban a user (ban members perm. required);\n%poll `<text>` - Makes a pool (mannage messages perm. required);\n%slowmode `<seconds>` - Sets slowmode in the current channel (manage channels perm. required);\n%nick `<target>` `<nick>` - Changes nickname (manage nicknames perm. required);\n%gstart `<mins>` `<prize>` - Starts a giveaway(manage messages perm. required);", colour = ecolor)
    fun = discord.Embed(title="Fun", description="%8ball `<question>` - Ask the magic 8ball a question;\n%say `<message>` - Makes the bot say a message;\n%wiki `<subject>` - Search wikipedia;\n%whois `<user>` - Get info about a user;", colour = ecolor)
    botinfo = discord.Embed(title="Bot Information", description="%ping - See bot latency;\n%info - Get info about the bot;\n%invite - Gives you the invite link for the bot;\n%servers - Shows in how many servers the bot is;\n%status - Get the link for the status dashboard;\n%support - Get the invite link for the Orange Bot official server;", colour = ecolor)
    ecom = discord.Embed(title = "Economy", description = "%balance - Checks balance;\n%beg - Beg for currency (45 sec. cooldown);\n%buy `<item>` `<amount>` - Buy an item from the shop;\n%deposit `<amount>` - Deposit an amount of currency in the bank;\n%give `<member>` `<amount>` - Transfer an amount of currency form your bank account to another bank account;\n%inventory - Shows your inventory;\n%leaderboard - Shows the leader board;\n%sell `<item>` - Sell an item from your inventory;\n%shop - Open shop;\n%withdraw `<amount>` - Withdraws an amount from the bank;\n%work - Work for some currency(24h cooldown);", colour=ecolor) 
    await ctx.author.send(embed=modadm)
    await ctx.author.send(embed=fun)
    await ctx.author.send(embed=botinfo)
    await ctx.author.send(embed=ecom)
    await ctx.send("Sent in DMs!")
    print("Help cmd used.")


@client.command()
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, nick):
    await member.edit(nick=nick)
    nicke = discord.Embed(title='Nickname changed.', colour=ecolor)
    nicke.set_footer(text=footer)
    await ctx.send(embed=nicke)


@client.command()
async def ping(ctx):
    raspuns = discord.Embed(
        title="Pong!",
        description=f"Bot latency: {round(client.latency * 1000)}ms",
        colour=ecolor)
    raspuns.set_footer(text=footer)
    raspuns.set_thumbnail(
        url=
        "https://cdn.discordapp.com/app-icons/782229157333434368/f9f3b1c437705d79ce262d16dcfafb74.png?size=64"
    )
    await ctx.send(embed=raspuns)


@client.command(aliases=["boardcast"])
async def say(ctx, *, msg):
    await ctx.send(msg)

@client.command(aliases=["8orange", "8ball", "eightball"])
async def eightorange(ctx, *, question):
    responses = [
        "Of course!", "Definitely!", "That's sure!", "I would bet on it!",
        "Is the orange orange?", "Idk, man. Ask later!",
        "Not sure! Ask later!", "Not so sure.", "Don't count on it!",
        "Definitely not!"
    ]
    ball = discord.Embed(
        title="8ball | My answer is:",
        description=random.choice(responses),
        colour=ecolor)
    ball.set_footer(text=footer)
    await ctx.send(embed=ball)


@client.command(aliases=["purge"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)
    feedback = discord.Embed(title="Messages Cleared!", colour=ecolor)
    feedback.set_footer(text=footer)
    await ctx.send(embed=feedback)
@clear.error
async def clear_error(error, ctx):
    await ctx.send(
        "There was an error. Make sure you have the permission to execute this command. Also make sure I have permission to do it."
    )


@client.command(aliases=["k"])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided."):
    try:
        await member.send(f"You were kicked from **{ctx.message.guild.name}**: " +
                      reason)
    except:
        await ctx.send("Failed to DM member.")
    await member.kick(reason=reason)
    kick = discord.Embed(title="User Kicked!", colour=ecolor)
    kick.set_footer(text=footer)
    await ctx.send(embed=kick)
@kick.error
async def kick_error(error, ctx):
    await ctx.send(
        "There was an error. Make sure you have the permission to execute this command. Also make sure I have permission to do it."
    )


@client.command(aliases=["b"])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided."):
    try:
        await member.send(f"You were banned from **{ctx.message.guild.name}**: " +
                      reason)
    except:
        await ctx.send("Failed to DM member.")
    await member.ban(reason=reason)
    ban = discord.Embed(title="User Banned", colour=ecolor)
    ban.set_footer(text=footer)
    await ctx.send(embed=ban)


@ban.error
async def ban_error(error, ctx):
    await ctx.send(
        "There was an error. Make sure you have the permission to execute this command. Also make sure I have permission to do it."
    )


@client.command(aliases=["vote"])
@commands.has_permissions(manage_messages=True)
async def poll(ctx, *, text):
    poll = discord.Embed(title="Poll Time!", description=text, colour=ecolor)
    poll.set_footer(text=footer)
    msg = await ctx.send(embed=poll)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")


@client.command()
async def info(ctx):
    dev = "Not a vibing cat#5692"
    info = discord.Embed(
        title="Orange Bot made by Not a vibing cat#0001",
        description="Thanks for using Orange Bot!\nVersion: 1.5\nDeveloper: " +
        dev + " \nMade with: discord.py\n",
        colour=ecolor)
    await ctx.author.send(embed=info)
    await ctx.send("Sent in DMs!")


@client.command()
async def wiki(ctx, *, subject):
    result = discord.Embed(
        title=subject, description=wikis(subject), colour=ecolor)
    await ctx.send(embed=result)


@client.command(aliases=["sm"])
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds):
    await ctx.channel.edit(slowmode_delay=seconds)
    suc = discord.Embed(
        title=f"Slowmode set to " + seconds + "sec.", colour=ecolor)
    suc.set_footer(text=footer)
    await ctx.send(embed=suc)


@slowmode.error
async def slowmode_error(error, ctx):
    await ctx.send(
        "There was an error. Make sure you have the permission to execute this command. Also make sure I have permission to do it."
    )


@client.command()
async def servers(ctx):
    ser = discord.Embed(
        title=f"The bot is in {len(client.guilds)} servers.", colour=ecolor)
    await ctx.send(embed=ser)

@client.command()
async def status(ctx):
    await ctx.author.send("See the status live here! https://stats.uptimerobot.com/g6BjnTlkJv")

@client.command()
@commands.has_permissions(manage_messages=True)
async def gstart(ctx, mins : int, *, prize):
    giveaway = discord.Embed(title="🎉GIVEAWAY🎉", description= f"{prize}", colour=ecolor)
    end = datetime.datetime.utcnow() - datetime.timedelta(seconds = mins * 60)
    giveaway.set_footer(text = f"Ends in {mins}mins from now!")
    gms = await ctx.send(embed = giveaway)
    await gms.add_reaction("🎉")
    await asyncio.sleep(mins * 60)
    nms = await ctx.channel.fetch_message(gms.id)
    users = await nms.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    winner = random.choice(users)
    await ctx.send(f"Congrats, {winner.mention} you won {prize}!")

@client.command(aliases=["whois"])
async def userinfo(ctx, member: discord.Member = None):
    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    roles = [role for role in member.roles]
    embed = discord.Embed(
        colour=ecolor, title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Display Name:", value=member.display_name)

    embed.add_field(
        name="Created Account On:",
        value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(
        name="Joined Server On:",
        value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    roles = [role.mention for role in member.roles[1:]]
    roles.append('@everyone')
    embed.add_field(name="Roles:", value="".join(roles))
    embed.add_field(name="Highest Role:", value=member.top_role.mention)
    await ctx.send(embed=embed)

@client.command()
async def support(ctx):
    await ctx.send("Need support or simply want to hang out with other Orange Bot users? Join the Orange Bot Community! https://discord.gg/CgR3nYGaSE")

##Economy commands start here

@client.command(aliases=["bal"])
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title=f"{ctx.author.name}'s balance", colour = ecolor)
    em.add_field(name="Wallet", value = wallet_amt)
    em.add_field(name="Bank", value = bank_amt)
    await ctx.send(embed=em)

@client.command()
@commands.cooldown(1, 45, BucketType.user)
async def beg(ctx):
    user = ctx.author
    await open_account(ctx.author)
    users = await get_bank_data()

    earnings = random.randrange(100)
    await ctx.send(f"Someone gave you {earnings} oranges.")

    users[str(user.id)]["wallet"] += earnings
    with open('mainbank.json',"w") as f:
        json.dump(users,f)

@client.command()
@commands.cooldown(1, 86400, BucketType.user)
async def work(ctx):
    user = ctx.author
    await open_account(ctx.author)
    users = await get_bank_data()

    earnings = random.randrange(1000)
    worke = discord.Embed(title="Work Pay", description=f"You were paid {earnings} oranges for your work.", colour=ecolor)

    users[str(user.id)]["wallet"] += earnings
    with open('mainbank.json',"w") as f:
        json.dump(users,f)
    await ctx.send(embed=worke)


@client.command(aliases=["with"])
async def withdraw(ctx,amount):
    await open_account(ctx.author)
    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("You dont have enough oranges.")
        return
    if amount < 1:
        await ctx.sent("Please enter a valid amount!")
        return
    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1 * amount, "bank")
    await ctx.send(f"{amount} oranges withdrawed succesfuly!")


@client.command(aliases=["dep"])
async def deposit(ctx,amount):
    await open_account(ctx.author)
    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("You dont have enough oranges.")
        return
    if amount < 1:
        await ctx.sent("Please enter a valid amount!")
        return
    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount, "bank")
    await ctx.send(f"{amount} oranges deposited succesfuly!")

@client.command()
async def give(ctx,member: discord.Member, amount):
    await open_account(ctx.author)
    await open_account(member)
    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("You dont have enough oranges in the bank!")
        return
    if amount < 1:
        await ctx.sent("Please enter a valid amount!")
        return
    await update_bank(ctx.author,-1*amount,"bank")
    await update_bank(member,amount, "bank")
    await ctx.send(f"{amount} oranges transfered succesfuly!")

@client.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop", colour = ecolor)

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name = name, value = f"{price} Oranges\n{desc}")

    await ctx.send(embed = em)

@client.command()
@commands.cooldown(1, 5, BucketType.user)
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return


    await ctx.send(f"You just bought {amount} {item}")


@client.command()
async def inventory(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title = "Inventory", colour=ecolor)
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)    

    await ctx.send(embed = em)    

@client.command()
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have {amount} {item} in your bag.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have {item} in your bag.")
            return

    await ctx.send(f"You just sold {amount} {item}.")

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.9* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]

@client.command(aliases = ["lb"])
async def leaderboard(ctx,x = 1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = ecolor)
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)



keep_alive.keep_alive()
TOKEN = os.environ.get("TOKEN")

client.run(TOKEN)                                                                                                                                                                                                                                                                                                                                                       
