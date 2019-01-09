import json
import time

with open('Members.json') as f:
    Members = json.load(f)

def create_user(user):
    if user not in Members:
        Members[user] = 0

def get_balance(user):
    return Members[user]

def update_balance(user):
    currBalance = get_balance(user)
    newBalance = currBalance + 1
    Members[user] = newBalance
    with open('Members.json', 'w') as outfile:
        json.dump(Members, outfile)


users = ['Soup', 'Buckwheat', 'Logan', 'Kris', 'Brittin']
for x in users:
    create_user(x)

pasttime = time.time()

while 1:
    #check current time
    currtime = time.time()
    
    #update balance every X seconds
    delay = 1

    #calculate when to update
    timediff = currtime - delay

    #update balance for online members
    if pasttime <= timediff:

        pasttime = time.time()

        for a in users:
            update_balance(a)