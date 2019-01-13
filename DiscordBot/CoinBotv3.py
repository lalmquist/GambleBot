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

def gamble(user, gambleamount):
    return
    
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

#add a command that makes fun of whatever game soup starts playing client.member.game

if __name__ == "__main__":

    # discordToken is the value you get when creating the bot
    discordToken = '' ##//Input your DiscordToken here
    client.run(discordToken)
