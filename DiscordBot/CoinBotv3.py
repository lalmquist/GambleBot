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
    if user != 'LogBot#2779':
        Members[user] = 0
        with open('Members.json', 'w') as outfile:
            json.dump(Members, outfile)

def dict_print(d):
    string = ''
    for key, value in d.items():
        string = string + str(key) + ' : ' + str(value) + "\n"
    return string

def check_gamble_amount(user, gamount):
    userbalance = get_balance(user)
    intUserBalance = int(userbalance)
    try:
        intGamble = int(gamount)
    except:
        return 1
                    
    if gamount == '':
        return 1
    
    if intGamble > intUserBalance:
        return 2
    else:
        return 0
    
@client.event
async def on_message(message):

    strchannel = str(message.channel)

    if message.author == client.user:
        return
    if strchannel != "gambling-room":
        return

    userID = str(message.author)

    userbalance = get_balance(userID)
    intUserBalance = int(userbalance)
    gamblemessage = message.content

    # !gamble command
    if message.content.startswith('!gamble'):

        # cut message to only gamble value
        gambleamount = gamblemessage[8:]

        check_results = check_gamble_amount(userID, gambleamount)

        #invalid entry
        if check_results == 1:

            await client.send_message(message.channel, "Type !help for commands.  Need to enter gamble value.")
            return

        #balance too low
        elif check_results == 2:

            await client.send_message(message.channel, "You're too poor to make this bet.")
            return

        intGamble = int(gambleamount)

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
        await client.send_message(message.channel, 'Type "!gamble #" to gamble integer amount of coins.\nType "!guess #" to play the guessing game.\nType "!guessrules" to see guess game rules.\nType !balance to see your current balance.\nType !balanceall to see all balances')

    # !balance command
    elif message.content == '!balance':
        user_balance = get_balance(userID)
        await client.send_message(message.channel, "Your balance is: " + str(user_balance))

        # Chirp Chirp
        intuser_balance = int(user_balance)
        if intuser_balance < 60:
            await client.send_message(message.channel, 'You gotta pump those numbers up, those are rookie numbers!')
    
    # !balanceall command
    elif message.content == '!balanceall':
        all_user_balance = get_balance_all()
        newD = {}
        def keyfunction(k):
            return all_user_balance[k]
        for key in sorted(all_user_balance, key=keyfunction, reverse=True):
            shortkey = key[:-5]
            newD[shortkey] = all_user_balance[key]

        await client.send_message(message.channel, dict_print(newD))

    elif message.content == '!guessrules':
        all_user_balance = get_balance_all()
        await client.send_message(message.channel, "LogBot will generate a random number and pick another random number between 0 and the first number.  You will have to guess the number.  If you guess within 50 you don't lose your gamble, if you guess closer you are rewarded based on how close to the target you are.")

    elif message.content.startswith('!guess'):

        # cut message to only gamble value
        guessgamble = gamblemessage[7:]

        check_results = check_gamble_amount(userID, guessgamble)

        #invalid entry
        if check_results == 1:

            await client.send_message(message.channel, "Type !help for commands.  Need to enter gamble value.")
            return

        #balance too low
        elif check_results == 2:

            await client.send_message(message.channel, "You're too poor to make this bet.")
            return

        intGamble = int(guessgamble)
        guesslimit = random.randint(50, 500)
        BotNumber = random.randint(0,guesslimit)
        await client.send_message(message.channel, "I'm thinking of a number between 0 and " + str(guesslimit) + "\nWhat is your guess?")
        check_results2 = 1
        
        while check_results2 == 1:
            msg = await client.wait_for_message(timeout=30, author=message.author)
            if msg == None:
                New_UserBalance = intUserBalance - intGamble
                update_balance(userID, New_UserBalance)
                await client.send_message(message.channel, "Too slow, you lose your gamble")
                return
            UserGuess = msg.content
            check_results2 = check_gamble_amount(userID, UserGuess)
            if check_results2 == 1:
                await client.send_message(message.channel, "Type !help for commands.  Need to enter gamble value.")
            
        intUserGuess = int(UserGuess)
        guessdiff = abs(intUserGuess-BotNumber)

        await client.send_message(message.channel, "LogBot secret number: " + str(BotNumber))

        if guessdiff > 50:
            New_UserBalance = intUserBalance - intGamble
            await client.send_message(message.channel, "Better luck next time....loser.")
        elif guessdiff == 0:
            New_UserBalance = intUserBalance + intGamble*10
            await client.send_message(message.channel, "You got it! You must be cheating...You're awarded with 10x your bet")
        elif guessdiff <= 10:
            New_UserBalance = intUserBalance + intGamble*5
            await client.send_message(message.channel, "Not bad! You're awarded with 5x your bet")
        elif guessdiff <= 20:
            New_UserBalance = intUserBalance + intGamble*4
            await client.send_message(message.channel, "Not bad! You're awarded with 4x your bet")
        elif guessdiff <= 30:
            New_UserBalance = intUserBalance + intGamble*3
            await client.send_message(message.channel, "Not bad! You're awarded with 3x your bet")
        elif guessdiff <= 40:
            New_UserBalance = intUserBalance + intGamble*2
            await client.send_message(message.channel, "Not bad! You're awarded with 2x your bet")
        elif guessdiff <= 50:
            await client.send_message(message.channel, "I've seen better.  You're awarded with 2x your bet")
            New_UserBalance = intUserBalance + intGamble

        update_balance(userID, New_UserBalance)

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

class MyCog(object):
    def __init__(self,bot):
        self.bot = bot
        
        # AsyncioEventLoop.create_task is a function that begins execution of a coroutine and
        # returns a coroutine object instantly. With a reference to this coroutine object
        # we can check if the coroutine is done, errored, or cancel it ourselves.
        self.looped_task = bot.create_task(self.looping_function())
        
        self.data = {}
        
    def __unload(self):
        # This is a special function that discord.py calls when a cog is unloaded.
        # Basically a cog unload event handler.
        
        # Technically this isn't necessary because the looping_function *should* exit cleanly,
        # but better safe than sorry.
        try:
            self.looped_task.cancel()
        except (AttributeError, asyncio.CancelledError):
            pass
    
    async def do_stuff(self):
        for member in client.get_all_members():
            str_member = str(member)
            # add member if they are new
            if str_member not in Members:
                add_member(str_member)
                
            # if member is online give them points
            if str(member.status) == 'online':
                currbalance = get_balance(str_member)

                intcurr_balance = int(currbalance)
                intcurr_balance = intcurr_balance + 1

                #make sure member is str
                update_balance(str_member, intcurr_balance)

        
    async def looping_function(self):
        # The "is" keyword here checks if two objects are found at the same memory location.
        # So this loop will run for the duration that this cog/plugin is loaded.
        # If the bot shuts down, this function exits cleanly.
        # If the cog is reloaded, this function exits cleanly and start again with the new cog code.
        while True:
            await self.do_stuff()

            # This sleep here is extremely important no matter how short you want your loop interval to be.
            # asyncio can only switch coroutine execution (the process that it uses to run functions in "parallel")
            # when an "await" keyword is found and execution has to pause. Calling "await self.do_stuff()"
            # won't force switching because no waiting actually occurs.

            # If you forget to add this sleep your bot will become entirely unresponsive since it's dedicating
            # 100% of it's execution time to running this function. Try it out sometime!
            await asyncio.sleep(30)
        
loop = asyncio.get_event_loop()
Banker = MyCog
Banker(loop)

if __name__ == "__main__":

    # discordToken is the value you get when creating the bot
    discordToken = '' ##//Input your DiscordToken here
    client.run(discordToken)
