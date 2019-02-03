import json
import time
import datetime
import random
import discord
import asyncio
from discord.utils import get

client = discord.Client()

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
    if user != 'LogBot#2779' and user != 'Rythm#3722':
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

def check_user(user):
    try:
        test = Members[user]
        return True
    except:
        return False

        
@client.event
async def on_message(message):

    strchannel = str(message.channel)
    
    if (message.author == client.user) or (str(message.author) == 'Rythm#3722'):
        return

    if message.content.startswith('$play'):
        playbal = get_balance(message.author)
        print(playbal)
        if int(playbal) < 100:
            await client.send_message(message.channel, "$skip")
            await client.send_message(message.channel, "You're too poor to play a song.  Song play requires 100 points. Your balance is " + str(playbal))
        newplaybal = int(playbal) - 100
        update_balance(message.author, newplaybal)
        
    if strchannel != "gambling-room":
        return
    
    userID = str(message.author)
    
    userbalance = get_balance(userID)
    intUserBalance = int(userbalance)
    gamblemessage = message.content
    
    # !gamble command multiple
    if message.content.startswith('!duel'):
    
        messagestr = str(message.content)
        messagesplit = messagestr.split()
        OpponentID = 'rando'
        OppAccept = 0

        # cut message to only gamble value
        try:
            duelgamble = messagesplit[2]
            opponent = messagesplit[1]
        except:
            await client.send_message(message.channel, 'Type "!Duel @OpponentName GambleAmount".')

        opp = idDict[opponent]
        OpponentID = str(opp)

        if OpponentID == str(message.author):
            await client.send_message(message.channel, "You can't duel yourself.")
            return

        if check_user(OpponentID) == False:
            await client.send_message(message.channel, "Member does not exist.")
            return
            
        check_results_you = check_gamble_amount(userID, duelgamble)
        
        #invalid entry
        if check_results_you == 1:
            await client.send_message(message.channel, "Type !help for commands.  Need to in format '!duel @user #'.")
            return
        
        #balance too low
        elif check_results_you == 2:
            userb = get_balance(str(message.author))
            await client.send_message(message.channel, "You're too poor to make this bet. Your balance is " + str(userb))
            return
        
        check_results_other = check_gamble_amount(OpponentID, duelgamble)

        #balance too low
        if check_results_other == 2:
            oppb = get_balance(str(OpponentID))
            await client.send_message(message.channel, "Your opponent is too poor to make this bet. " + OpponentID[:-5] + " balance is " + str(oppb))
            return

        await client.send_message(message.channel, opponent + " do you accept? Type 'Accept' or 'Decline'.")
        
        while OppAccept == 0:
            OppResponse = await client.wait_for_message(timeout=30)
            if OppResponse == None:
                await client.send_message(message.channel, "Opponent didn't respond in time.")
                return
            StrResponse = str(OppResponse.content)
            StrAuthor = str(OppResponse.author)
            if (StrResponse == 'Accept' or StrResponse == 'accept') and StrAuthor == OpponentID:
                OppAccept = 1
                pass
            elif StrAuthor == OpponentID:
                await client.send_message(message.channel, "Opponent declined.")
                return
        
        oppbalance = get_balance(OpponentID)
        intOppBalance = int(oppbalance)
        
        intGamble = int(duelgamble)
        guesslimit = random.randint(10, 100)
        BotNumber = random.randint(0,guesslimit)
        await client.send_message(message.channel, "I'm thinking of a number between 0 and " + str(guesslimit) + "\nWhat is your guess?")
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

                msg = await client.wait_for_message(timeout=60)
                if msg == None:
                    if UserGuessReceived == 0:
                        New_UserBalance = intUserBalance - intGamble
                        update_balance(userID, New_UserBalance)
                
                    if OppGuessReceived == 0:
                        New_OppBalance = intOppBalance - intGamble
                        update_balance(OpponentID, New_OppBalance)
                    
                        await client.send_message(message.channel, "Too slow, you lose your gamble")
                        return

                if str(msg.author) == str(userID) and UserGuessReceived == 0:
                    UserGuess = msg.content
                    check_guess1 = check_gamble_amount(userID, UserGuess)
                    if check_guess1 == 1:
                        await client.send_message(message.channel, "Type !help for commands.  Need to enter guess value.")
                    else:
                        UserGuessReceived = 1
                
                if str(msg.author) == str(OpponentID) and OppGuessReceived == 0:
                    OppGuess = msg.content
                    check_guess2 = check_gamble_amount(OpponentID, OppGuess)
                    if check_guess2 == 1:
                        await client.send_message(message.channel, "Type !help for commands.  Need to enter guess value.")
                    else:
                        OppGuessReceived = 1
                loops = loops + 1
        
        intOppGuess = int(OppGuess)
        opponent_guessdiff = abs(intOppGuess-BotNumber)
        intUserGuess = int(UserGuess)
        user_guessdiff = abs(intUserGuess-BotNumber)
        
        await client.send_message(message.channel, "LogBot secret number: " + str(BotNumber))
        
        if user_guessdiff and opponent_guessdiff == 0:
            #holy moly give everybody a milly
            New_UserBalance = intUserBalance + intGamble*1000
            New_OppBalance = intOppBalance + intGamble*1000
            await client.send_message(message.channel, "You both guessed the secret number!, You're rich bitch!!!!!")
        
        if user_guessdiff == 0:
            #user win a bunch
            New_UserBalance = intUserBalance + intGamble*100
            New_OppBalance = intOppBalance - intGamble
            await client.send_message(message.channel, userID[:-5] + " guessed the secret number!")
        
        if opponent_guessdiff == 0:
            #opponent win a bunch
            New_UserBalance = intUserBalance - intGamble
            New_OppBalance = intOppBalance + intGamble*100
            await client.send_message(message.channel, OpponentID[:-5] + " wins!")
        
        if opponent_guessdiff < user_guessdiff:
            # opponent wins
            New_UserBalance = intUserBalance - intGamble
            New_OppBalance = intOppBalance + intGamble
            await client.send_message(message.channel, OpponentID[:-5] + " wins!")
        
        elif opponent_guessdiff == user_guessdiff:
            # tie goes to opponent
            New_UserBalance = intUserBalance - intGamble
            New_OppBalance = intOppBalance + intGamble
            await client.send_message(message.channel, "Tie goes to " + OpponentID[:-5] + " because " + userID[:-5] + " initiated.")
        
        else:
            # initializer wins
            New_UserBalance = intUserBalance + intGamble
            New_OppBalance = intOppBalance - intGamble
            await client.send_message(message.channel, userID[:-5] + " wins!")
        
        update_balance(userID, New_UserBalance)
        update_balance(OpponentID, New_OppBalance)
    
    
    # !gamble command alone
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
            userbal = get_balance(userID)        
            await client.send_message(message.channel, "You're too poor to make this bet. Your balance is " + str(userbal))
            return
        
        intGamble = int(gambleamount)
        
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
        await client.send_message(message.channel, 'Type "!duel @user #" to duel @user in guess game for # coins.\nType "!gamble #" to gamble integer amount of coins.\nType "!guess #" to play the guessing game.\nType "!guessrules" to see guess game rules.\nType !balance to see your current balance.\nType !balanceall to see all balances')
    
    # !balance command
    elif message.content == '!balance':
        user_balance = get_balance(userID)
        await client.send_message(message.channel, "Your balance is: " + str(user_balance))
        
        # Chirp Chirp
        intuser_balance = int(user_balance)
        if intuser_balance < 1000:
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
        guesslimit = random.randint(100, 500)
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
                await client.send_message(message.channel, "Type !help for commands.  Need to enter guess value.")
        
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
            await client.send_message(message.channel, "I've seen better.  You're awarded with your bet")
            New_UserBalance = intUserBalance + intGamble
        
        update_balance(userID, New_UserBalance)

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
        idDict['<@' + str(member.id) + '>'] = str_member

        # add member if they are new
        if str_member not in Members:
            add_member(str_member)
    
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
            idDict['<@' + str(member.id) + '>'] = str_member
    
            # add member if they are new
            if str_member not in Members:
                add_member(str_member)
            if str_member != 'LogBot#2779' and str_member != 'Rythm#3722':    
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
