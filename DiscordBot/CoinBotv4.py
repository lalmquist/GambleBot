import json
import time
import datetime
import random
import discord
import asyncio
from discord.utils import get

serverID = ""  # INPUT YOUR SERVERID HERE (unused)
client = discord.Client()

# Start buffer time for delay calculation
pasttime = time.time()

with open('Members.json') as f:
    Members = json.load(f)

def get_balance(user):
    intBalance = Members[user]
    strBalance = str(intBalance)
    return strBalance


def update_balance(user, newBal):
    Members[user] = newBal
    with open('Members.json', 'w') as outfile:
        json.dump(Members, outfile)


def get_balance_all():
    return Members


def add_member(user):
    Members[user] = 0
    with open('Members.json', 'w') as outfile:
        json.dump(Members, outfile)
    
@client.event
async def on_message(message):

    if message.author == client.user:
        return

    userID = str(message.author)

    # !gamble command
    if message.content.startswith('!gamble'):

        userbalance = get_balance(userID)
        intUserBalance = int(userbalance)
        await client.send_message(message.channel, "So you think you can beat the LogBot with a measly balance of " + str(userbalance) + "?")

        # cut message to only gamble value
        gamblemessage = message.content
        gambleamount = gamblemessage[8:]
                    
        try:
            intGamble = int(gambleamount)
        except:
            await client.send_message(message.channel, "Type !help for commands.  Need to enter gamble value.")
            return
                    
        if gambleamount == '':
            await client.send_message(message.channel, "Type !help for commands.  Need to enter gamble value.")
            return
                            
        time.sleep(1)
                    
        if intGamble > intUserBalance:
            await client.send_message(message.channel, "You're too poor to make this bet.")
            return

        # for now, hardcode roll to 100
        rollsize = 100
        userroll = random.randint(0, rollsize)
        botroll = random.randint(0, rollsize)
                    
        await client.send_message(message.channel, "Your roll: " + str(userroll) + "\nLogBot roll: " + str(botroll))
                    
        # Win
        if botroll > userroll:
            NewUserBalance = intUserBalance - intGamble
            await client.send_message(message.channel, "You lose loser")
                    
        # Lose
        elif botroll < userroll:
            NewUserBalance = intUserBalance + intGamble
            await client.send_message(message.channel, "Winner winner chickenSoup dinner!")
                    
        # Tie-Lose
        elif botroll == userroll:
            NewUserBalance = intUserBalance - intGamble
            await client.send_message(message.channel, "Tie goes to the LogBot")
                    
        update_balance(userID, NewUserBalance)
            
    # !help command
    elif message.content == '!help':
        await client.send_message(message.channel, 'Type "!gamble #" to gamble integer amount of coins.\nType !balance to see your current balance.\nType !balanceall to see all balances')

    # !balance command
    elif message.content == '!balance':
        user_balance = get_balance(userID)
        await client.send_message(message.channel, "Your balance is: " + str(user_balance))

        # Chirp Chirp
        intuser_balance = int(user_balance)
        if intuser_balance < 60:
            await client.send_message(message.channel, 'You gotta pump those numbers up, those are rookie numbers!')

    #make this easier to read        
    elif message.content == '!balanceall':
        all_user_balance = get_balance_all()
        await client.send_message(message.channel, all_user_balance)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    # create array of server members
    for member in client.get_all_members():
        str_member = str(member)

        # add member if they are new
        if str_member not in Members:
            add_member(str_member)


@client.event
#async def on_member_update(before,after):
async def on_typing(channel, user, when):

    # check current time
    currtime = time.time()

    global pasttime

    delay = currtime - pasttime

    delaymin = delay/1

    intdelaymin = int(delaymin)

    for member in client.get_all_members():
        str_member = str(member)
        # add member if they are new
        if str_member not in Members:
            add_member(str_member)
            
        # if member is online give them points
        if str(member.status) == 'online':
            
            currbalance = get_balance(str_member)
            print(currbalance)
            intcurr_balance = int(currbalance)
            intcurr_balance = intcurr_balance + intdelaymin

            print(intcurr_balance)

            #make sure member is str
            update_balance(str_member, intcurr_balance)
            pasttime = time.time()

#add a command that makes fun of whatever game soup starts playing client.member.game

if __name__ == "__main__":

    # discordToken is the value you get when creating the bot
    discordToken = 'NTI2MDk0MzY5MjYzMTkwMDQx.DxbtFQ.E9rkdlsiKxcrKyDMsA9m2vF-AuQ' ##//Input your DiscordToken here
    client.run(discordToken)