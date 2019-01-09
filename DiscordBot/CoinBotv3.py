import json
import time
import random
import discord
import asyncio
from discord.utils import get

# This value can be retrieved by right clicking on server channel

serverID = ""  # INPUT YOUR SERVERID HERE (unused)
client = discord.Client()

# Start buffer time for delay calculation
pasttime = time.time()

with open('Members.json') as f:
    Members = json.load(f)

def get_balance(user):
    lol = str(user)
    abcd = Members[lol]
    strabcd = str(abcd)
    return strabcd


def update_balance(user, newBal):
    struser = str(user)
    Members[struser] = newBal
    with open('Members.json', 'w') as outfile:
        json.dump(Members, outfile)


def get_balance_all():
    return Members


def add_member(user):
    struserr = str(user)
    if user not in Members:
        Members[struserr] = 0
        with open('Members.json', 'w') as outfile:
            json.dump(Members, outfile)

def gamble(user, gambleamount):
    return
    
@client.event
async def on_message(message):

    #check_time()

    if message.author == client.user:
        return

    # Gather UserID and encode values
    userID = message.author
    #userID = userID.encode('utf-8')
    userName = "#" + str(message.author.discriminator)
    userName = userName.encode('utf-8')

    print(userID)

    # !gamble command
    if message.content.startswith('!gamble'):
        intGamble = 99999999999
        userbalance = get_balance(userName)
        await client.send_message(message.channel, "So you think you can beat the LogBot with a measly balance of ?")

        # cut message to only gamble value
        gamblemessage = message.content
        gambleamount = gamblemessage[8:]
                    
        try:
            intGamble = int(gambleamount)
        except:
            await client.send_message(message.channel, "Type !help for commands.  Need to enter gamble value")
                    
        if gambleamount == '':
            await client.send_message(message.channel, "Type !help for commands.  Need to enter gamble value")
                            
        time.sleep(1)
                    
        if intGamble > userbalance:
            await client.send_message(message.channel, "You're too poor to make this bet")
            return
        elif intGamble == 99999999999:
            return

        # for now, hardcode roll to 100
        rollsize = 100
        userroll = random.randint(0, rollsize)
        botroll = random.randint(0, rollsize)
                    
        await client.send_message(message.channel, "Your roll: , LogBot roll: ")
                    
        # Win
        if botroll > userroll:
            NewUserBalance = userbalance - intGamble
            await client.send_message(message.channel, "You lose loser")
                    
        # Lose
        elif botroll < userroll:
            NewUserBalance = userbalance + intGamble
            await client.send_message(message.channel, "Winner winner chickenSoup dinner!")
                    
        # Tie-Lose
        elif botroll == userroll:
            NewUserBalance = userbalance - intGamble
            await client.send_message(message.channel, "Tie goes to the LogBot")
                    
        update_balance(userName, NewUserBalance)
            
    # !help command
    elif message.content == '!help':
        await client.send_message(message.channel, 'Type "!gamble #" to gamble integer amount of coins.\nType !balance to see your current balance.\nType !balanceall to see all balances')

    # !balance command
    elif message.content == '!balance':
        print(Members)
        user_balance = get_balance(userName)
        await client.send_message(message.channel, 'Your balance is ')

        # Chirp Chirp
        if user_balance < 1000:
            await client.send_message(message.channel, 'You gotta pump those numbers up, those are rookie numbers!')
            
    elif message.content == '!balanceall':
        all_user_balance = get_balance_all()
        await client.send_message(message.channel, '')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    # create array of online members
    for member in client.get_all_members():
        # add member if they are new
        if member not in Members:
            add_member(member)

def check_time():
    # check current time
    currtime = time.time()
    global pasttime
    # update balance every X seconds
    delay = 5
        
    # calculate when to update
    timediff = currtime - delay
        
    # update balance for online member
    if pasttime <= timediff:
        # reset memory time
        pasttime = time.time()
                
        # create array of online members
        for member in client.get_all_members():
        
            # add member if they are new
            if member not in Members:
                add_member(member)
            
            # if member is online give them +1 coin
            if str(member.status) == 'online':
            
                currbalance = get_balance(member)
                currbalance = currbalance + 1 
                update_balance(member, currbalance)

   
if __name__ == "__main__":
    # discordToken is the value you get when creating the bot
    discordToken = 'NTI2MDk0MzY5MjYzMTkwMDQx.DxbtFQ.E9rkdlsiKxcrKyDMsA9m2vF-AuQ' ##//Input your DiscordToken here
    client.run(discordToken)
