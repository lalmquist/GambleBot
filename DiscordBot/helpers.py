import globals
import json

# helper functions

def get_balance(user):
    intBalance = globals.Members[user]
    strBalance = str(intBalance)
    return strBalance

def get_gamble_history(user):
    intBalance = globals.GambleHistory[user]
    strBalance = str(intBalance)
    return strBalance

def update_balance(user, newBal):
    globals.Members[user] = newBal
    with open('Members.json', 'w') as outfile:
        json.dump(globals.Members, outfile)

def update_gamble_history(user, newBal):
    globals.GambleHistory[user] = newBal
    with open('GambleHistory.json', 'w') as outfile:
        json.dump(globals.GambleHistory, outfile)

def get_balance_all():
    return globals.Members

def get_ghist_all():
    return globals.GambleHistory

def add_member(user):
    if user != 'LogBot#2779' and user != 'Rythm#3722' and user != 'BuckBot#0937':
        globals.Members[user] = 0
        with open('Members.json', 'w') as outfile:
            json.dump(globals.Members, outfile)

def add_member_gh(user):
    if user != 'LogBot#2779' and user != 'Rythm#3722' and user != 'BuckBot#0937':
        globals.GambleHistory[user] = 0
        with open('GambleHistory.json', 'w') as outfile:
            json.dump(globals.GambleHistory, outfile)

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
        test = globals.Members[user]
        return True
    except:
        return False