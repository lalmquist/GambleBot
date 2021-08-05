import json
import time
import datetime
import random
import discord
import asyncio
from discord.utils import get

intents = discord.Intents.all()
client = discord.Client(intents=intents)

with open('Members.json') as f:
    Members = json.load(f)

with open('GambleHistory.json') as f:
    GambleHistory = json.load(f)

def get_balance(user):
    intBalance = Members[user]
    strBalance = str(intBalance)
    return strBalance

def get_gamble_history(user):
    intBalance = GambleHistory[user]
    strBalance = str(intBalance)
    return strBalance

def update_balance(user, newBal):
    Members[user] = newBal
    with open('Members.json', 'w') as outfile:
        json.dump(Members, outfile)

def update_gamble_history(user, newBal):
    GambleHistory[user] = newBal
    with open('GambleHistory.json', 'w') as outfile:
        json.dump(GambleHistory, outfile)

def get_balance_all():
    return Members

def get_ghist_all():
    return GambleHistory

def add_member(user):
    if user != 'LogBot#2779' and user != 'Rythm#3722' and user != 'BuckBot#0937':
        Members[user] = 0
        with open('Members.json', 'w') as outfile:
            json.dump(Members, outfile)

def add_member_gh(user):
    if user != 'LogBot#2779' and user != 'Rythm#3722' and user != 'BuckBot#0937':
        GambleHistory[user] = 0
        with open('GambleHistory.json', 'w') as outfile:
            json.dump(GambleHistory, outfile)

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

def check_user(user):
    try:
        test = Members[user]
        return True
    except:
        return False

        
@client.event
async def on_message(message):
    def check_msg_user(m):
        return m.channel == channel and m.author == message.author

    def check_msg_chan(m):
        return m.channel == channel

    channel = message.channel
    
    strchannel = str(message.channel)
    
    if (message.author == client.user) or (str(message.author) == 'Rythm#3722') or (str(message.author) == 'BuckBot#0937'):
        return
            
    if strchannel != "gambling-room":
        return
    
    userID = str(message.author)

    gHistory_u = get_gamble_history(userID)

    userbalance = get_balance(userID)
    intUserBalance = int(userbalance)
    gamblemessage = message.content

    msg_lower = message.content.lower()
    
    # !gamble command multiple
    if msg_lower.startswith('!duel'):
    
        messagestr = str(message.content)
        messagesplit = messagestr.split()
        OpponentID = 'rando'
        OppAccept = 0

        # cut message to only gamble value
        try:
            duelgamble = messagesplit[2]
            opponent = messagesplit[1]        
        except:
            await channel.send('Type "!duel @OpponentName GambleAmount".')
            return
        
        opp = idDict[opponent]
        OpponentID = str(opp)

        if OpponentID == str(message.author):
            await channel.send("You can't duel yourself.")
            return

        if check_user(OpponentID) == False:
            await channel.send("Member does not exist.")
            return
        
        check_results_you = check_gamble_amount(userID, duelgamble)    
        
        #invalid entry
        if check_results_you == 1:
            await channel.send("Type !help for commands.  Need to in format '!duel @user #'.")
            return
        
        #balance too low
        elif check_results_you == 2:
            userb = get_balance(str(message.author))
            await channel.send("You're too poor to make this bet. Your balance is " + str(userb))
            return
        
        check_results_other = check_gamble_amount(OpponentID, duelgamble)

        #balance too low
        if check_results_other == 2:
            oppb = get_balance(str(OpponentID))
            await channel.send("Your opponent is too poor to make this bet. " + OpponentID[:-5] + " balance is " + str(oppb))
            return

        await channel.send(opponent + " do you accept? Type 'Accept' or 'Decline'.")
        
        while OppAccept == 0:
            try:
                OppResponse = await client.wait_for('message', timeout=30, check=check_msg_chan)
            except asyncio.TimeoutError:
                await channel.send("Opponent didn't respond in time.")
                return
            StrResponse = str(OppResponse.content)
            StrAuthor = str(OppResponse.author)
            if (StrResponse == 'Accept' or StrResponse == 'accept') and StrAuthor == OpponentID:
                OppAccept = 1
                pass
            elif StrAuthor == OpponentID:
                await channel.send("Opponent declined.")
                return
        
        oppbalance = get_balance(OpponentID)
        
        gHistory_o = get_gamble_history(OpponentID)
        intOppBalance = int(oppbalance)
        
        intGamble = int(duelgamble)
        guesslimit = random.randint(10, 100)
        BotNumber = random.randint(0,guesslimit)
        await channel.send("I'm thinking of a number between 0 and " + str(guesslimit) + "\nWhat is your guess?")
        check_guess1 = 1
        check_guess2 = 1
        GuessesReceived = 0
        UserGuessReceived = 0
        OppGuessReceived = 0
        loops = 0
        
        while GuessesReceived == 0 and loops < 1:
            while (check_guess1 == 1) or (check_guess2 == 1):

                if UserGuessReceived == 1 and OppGuessReceived == 1:
                    GuessesReceived = 1

                try:
                    msg = await client.wait_for('message', timeout=60, check=check_msg_chan)
                except asyncio.TimeoutError:
                    if UserGuessReceived == 0:
                        New_UserBalance = intUserBalance - intGamble
                        update_balance(userID, New_UserBalance)
                        
                        new_ghist_u = int(gHistory_u) - intGamble
                        update_gamble_history(userID, new_ghist_u)
                
                    if OppGuessReceived == 0:
                        New_OppBalance = intOppBalance - intGamble
                        update_balance(OpponentID, New_OppBalance)
                        
                        new_ghist_o = int(gHistory_o) - intGamble
                        update_gamble_history(OpponentID, new_ghist_o)
                    
                    await channel.send("Too slow, you lose your gamble")
                    return

                if str(msg.author) == str(userID) and UserGuessReceived == 0:
                    UserGuess = msg.content
                    check_guess1 = check_gamble_amount(userID, UserGuess)
                    if check_guess1 == 1:
                        await channel.send("Type !help for commands.  Need to enter guess value.")
                    else:
                        UserGuessReceived = 1
                
                if str(msg.author) == str(OpponentID) and OppGuessReceived == 0:
                    OppGuess = msg.content
                    check_guess2 = check_gamble_amount(OpponentID, OppGuess)
                    if check_guess2 == 1:
                        await channel.send("Type !help for commands.  Need to enter guess value.")
                    else:
                        OppGuessReceived = 1
                loops = loops + 1
        
        intOppGuess = int(OppGuess)
        opponent_guessdiff = abs(intOppGuess-BotNumber)
        intUserGuess = int(UserGuess)
        user_guessdiff = abs(intUserGuess-BotNumber)

        
        await channel.send("LogBot secret number: " + str(BotNumber))
        
        if user_guessdiff and opponent_guessdiff == 0:
            #holy fuck you cheaters
            New_UserBalance = intUserBalance + intGamble*1000
            New_OppBalance = intOppBalance + intGamble*1000
            new_ghist_u = int(gHistory_u) + intGamble*1000
            new_ghist_o = int(gHistory_o) + intGamble*1000
            await channel.send("You both guessed the secret number!, You're rich bitch!!!!!")
        
        if user_guessdiff == 0:
            #user win a bunch
            New_UserBalance = intUserBalance + intGamble*100
            New_OppBalance = intOppBalance - intGamble
            new_ghist_u = int(gHistory_u) + intGamble*100
            new_ghist_o = int(gHistory_o) - intGamble
            await channel.send(userID[:-5] + " guessed the secret number!")
        
        if opponent_guessdiff == 0:
            #opponent win a bunch
            New_UserBalance = intUserBalance - intGamble
            New_OppBalance = intOppBalance + intGamble*100
            new_ghist_u = int(gHistory_u) - intGamble
            new_ghist_o = int(gHistory_o) + intGamble*100
            await channel.send(OpponentID[:-5] + " wins!")
        
        if opponent_guessdiff < user_guessdiff:
            # opponent wins
            New_UserBalance = intUserBalance - intGamble
            New_OppBalance = intOppBalance + intGamble
            new_ghist_u = int(gHistory_u) - intGamble
            new_ghist_o = int(gHistory_o) + intGamble
            await channel.send(OpponentID[:-5] + " wins!")
        
        elif opponent_guessdiff == user_guessdiff:
            # tie goes to opponent
            New_UserBalance = intUserBalance - intGamble
            New_OppBalance = intOppBalance + intGamble
            new_ghist_u = int(gHistory_u) - intGamble
            new_ghist_o = int(gHistory_o) + intGamble
            await channel.send("Tie goes to " + OpponentID[:-5] + " because " + userID[:-5] + " initiated.")
        
        else:
            # initializer wins
            New_UserBalance = intUserBalance + intGamble
            New_OppBalance = intOppBalance - intGamble
            new_ghist_u = int(gHistory_u)
            new_ghist_o = int(gHistory_o) - intGamble
            await channel.send(userID[:-5] + " wins!")
        
        update_balance(userID, New_UserBalance)
        update_balance(OpponentID, New_OppBalance)
        update_gamble_history(userID, new_ghist_u)
        update_gamble_history(OpponentID, new_ghist_o)
        
    
    
    # !gamble command alone
    if msg_lower.startswith('!gamble'):
    
        # cut message to only gamble value
        gambleamount = gamblemessage[8:]
        
        check_results = check_gamble_amount(userID, gambleamount)
        
        #invalid entry
        if check_results == 1:
            await channel.send("Type !help for commands.  Need to enter gamble value.")
            return
        
        #balance too low
        elif check_results == 2:
            userbal = get_balance(userID)        
            await channel.send("You're too poor to make this bet. Your balance is " + str(userbal))
            return
        
        intGamble = int(gambleamount)
        
        rollsize = 100
        userroll = random.randint(0, rollsize)
        botroll = random.randint(0, rollsize)
        
        await channel.send("Your roll: " + str(userroll) + "\nLogBot roll: " + str(botroll))
        
        # Win
        if botroll > userroll:
            NewUserBalance = intUserBalance - intGamble
            new_ghist_u = int(gHistory_u) - intGamble
            await channel.send("You lose loser")
        
        # Lose
        elif botroll < userroll:
            NewUserBalance = intUserBalance + intGamble
            new_ghist_u = int(gHistory_u) + intGamble
            await channel.send("Winner winner chickenSoup dinner!")
        
        # Tie-Lose
        elif botroll == userroll:
            NewUserBalance = intUserBalance - intGamble
            new_ghist_u = int(gHistory_u) - intGamble
            await channel.send("Tie goes to the LogBot")
        
        update_balance(userID, NewUserBalance)
        update_gamble_history(userID, new_ghist_u)
    
    # !help command
    elif msg_lower == '!help':
        await channel.send('Type "!duel @user #" to duel @user in guess game for # coins.\n' +
                            'Type "!gamble #" to gamble integer amount of coins.\n' +
                            'Type "!guess #" to play the guessing game.\n' +
                            'Type "!guessrules" to see guess game rules.\n' +
                            'Type "!balance" to see your current balance.\n' +
                            'Type "!balanceall" to see all balances.\n' +
                            'Type "!ghistoryall" to see all gamble history.')
    
    # !balance command
    elif msg_lower == '!balance':
        user_balance = get_balance(userID)
        ghistory = get_gamble_history(userID)
        await channel.send("Your balance is: " + str(user_balance) + ". Your gambling has changed your balance by: "+ str(ghistory))
        
        # Chirp Chirp
        intuser_balance = int(user_balance)
        if intuser_balance < 1000:
            await channel.send('You gotta pump those numbers up, those are rookie numbers!')
    
    # !balanceall command
    elif msg_lower == '!balanceall':
        all_user_balance = get_balance_all()
        newD = {}
        def keyfunction(k):
            return all_user_balance[k]
        for key in sorted(all_user_balance, key=keyfunction, reverse=True):
            shortkey = key[:-5]
            newD[shortkey] = all_user_balance[key]
        
        await channel.send(dict_print(newD))

    elif msg_lower == '!ghistoryall':
        all_user_ghist = get_ghist_all()
        newD = {}
        def keyfunction(k):
            return all_user_ghist[k]
        for key in sorted(all_user_ghist, key=keyfunction, reverse=True):
            shortkey = key[:-5]
            newD[shortkey] = all_user_ghist[key]
        
        await channel.send(dict_print(newD))
        
    elif msg_lower == '!guessrules':
        await channel.send("LogBot will generate a random number and pick another random number between 0 and the first number.  You will have to guess the number.  If you guess within 50 you don't lose your gamble, if you guess closer you are rewarded based on how close to the target you are.")
    
    elif msg_lower.startswith('!guess'):
    
        # cut message to only gamble value
        guessgamble = gamblemessage[7:]
        
        check_results = check_gamble_amount(userID, guessgamble)
        
        #invalid entry
        if check_results == 1:
        
            await channel.send("Type !help for commands.  Need to enter gamble value.")
            return
        
        #balance too low
        elif check_results == 2:
        
            await channel.send("You're too poor to make this bet.")
            return
        
        intGamble = int(guessgamble)
        guesslimit = random.randint(100, 500)
        BotNumber = random.randint(0,guesslimit)
        await channel.send("I'm thinking of a number between 0 and " + str(guesslimit) + "\nWhat is your guess?")
        check_results2 = 1
        
        while check_results2 == 1:

            def check(msg):
                return msg.author == message.author

            try:
                msg = await client.wait_for('message', timeout=30, check=check_msg_user)
            except asyncio.TimeoutError:
                New_UserBalance = intUserBalance - intGamble
                new_ghist_u = int(gHistory_u) - intGamble
                update_balance(userID, New_UserBalance)
                update_gamble_history(userID, new_ghist_u)
                await channel.send("Too slow, you lose your gamble")
                return
            UserGuess = msg.content
            check_results2 = check_gamble_amount(userID, UserGuess)
            if check_results2 == 1:
                await channel.send("Type !help for commands.  Need to enter guess value.")
        
        intUserGuess = int(UserGuess)
        guessdiff = abs(intUserGuess-BotNumber)
        
        await channel.send("LogBot secret number: " + str(BotNumber))
        
        if guessdiff > 50:
            New_UserBalance = intUserBalance - intGamble
            new_ghist_u = int(gHistory_u) - intGamble
            await channel.send("Better luck next time....loser.")
        elif guessdiff == 0:
            New_UserBalance = intUserBalance + intGamble*10
            new_ghist_u = int(gHistory_u) + intGamble*10
            await channel.send("You got it! You must be cheating...You're awarded with 10x your bet")
        elif guessdiff <= 10:
            New_UserBalance = intUserBalance + intGamble*5
            new_ghist_u = int(gHistory_u) + intGamble*5
            await channel.send("Not bad! You're awarded with 5x your bet")
        elif guessdiff <= 20:
            New_UserBalance = intUserBalance + intGamble*4
            new_ghist_u = int(gHistory_u) + intGamble*4
            await channel.send("Not bad! You're awarded with 4x your bet")
        elif guessdiff <= 30:
            New_UserBalance = intUserBalance + intGamble*3
            new_ghist_u = int(gHistory_u) + intGamble*3
            await channel.send("Not bad! You're awarded with 3x your bet")
        elif guessdiff <= 40:
            New_UserBalance = intUserBalance + intGamble*2
            new_ghist_u = int(gHistory_u) + intGamble*2
            await channel.send("Not bad! You're awarded with 2x your bet")
        elif guessdiff <= 50:
            await channel.send("I've seen better.  You're awarded with your bet")
            New_UserBalance = intUserBalance + intGamble
            new_ghist_u = int(gHistory_u) + intGamble
        
        update_balance(userID, New_UserBalance)
        update_gamble_history(userID, new_ghist_u)

idDict = {}

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    # create array of server members
    for member in client.get_all_members():
        str_member = str(member)
        idDict['<@!' + str(member.id) + '>'] = str_member

        # add member if they are new
        if str_member not in Members:
            add_member(str_member)
            add_member_gh(str_member)
    
class MyCog(object):
    def __init__(self,bot):
        self.bot = bot
        self.looped_task = bot.create_task(self.looping_function())
        self.data = {}
    
    def __unload(self):
        try:
            self.looped_task.cancel()
        except (AttributeError, asyncio.CancelledError):
            pass
    
    async def do_stuff(self):
        for member in client.get_all_members():
            str_member = str(member)
            idDict['<@!' + str(member.id) + '>'] = str_member
    
            # add member if they are new
            if str_member not in Members:
                add_member(str_member)
                add_member_gh(str_member)
            if str_member != 'LogBot#2779' and str_member != 'Rythm#3722' and str_member != 'BuckBot#0937':    
                # if member is online give them points
                if str(member.status) == 'online':
            
                    currbalance = get_balance(str_member)
                        
                    intcurr_balance = int(currbalance)
                    intcurr_balance = intcurr_balance + 1
                        
                    #make sure member is str
                    update_balance(str_member, intcurr_balance)


    async def looping_function(self):
        while True:
            await self.do_stuff()
            await asyncio.sleep(30)

loop = asyncio.get_event_loop()
Banker = MyCog
Banker(loop)

if __name__ == "__main__":
    
    f=open("token.txt","r")
    if f.mode == 'r':
        discordToken = f.read()

    # discordToken is the value you get when creating the bot

    client.run(discordToken)
