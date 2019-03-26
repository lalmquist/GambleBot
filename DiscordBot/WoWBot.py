import asyncio
import aiohttp
import os
import json
import time
import datetime
import random
import discord
from discord.utils import get

client = discord.Client()

wow_bot_channel = 'general'
REGION = 'us'
REALM = "Kel'Thuzad"
WOW_CLIENT_ID = ''
WOW_CLIENT_SECRET = ''
LOCALE = str(os.environ.get('LOCALE'))
past_time = datetime.datetime.now()

########################################

char_list = ['Bearoplane' , 'Buckwheat' , 'Logman']

########################################

async def get_data(region, access_token, **kwargs):
    """Helper function that grabs data from the World of Warcraft API."""

    if access_token == 'credential_error':
        return access_token

    else:
        base_api_path = 'https://%s.api.blizzard.com' % (region)
        
        try:
            async with aiohttp.ClientSession() as _client:
                # Fires off a different API call depending on the type of requested content.
                api_path = '%s/wow/character/%s/%s?fields=%s&locale=%s&access_token=%s' % (base_api_path, kwargs.get('realm'), kwargs.get('name'), kwargs.get('field'), LOCALE, access_token)
                    
                async with _client.get(api_path, headers={'Authorization': 'Bearer %s' % (access_token)}) as api_response:
                    
                    if api_response.status == 200:
                        api_json = await api_response.json()
                        return api_json

                    elif api_response.status == 404:
                        print('Error: Character not found')

                    else: return

        except Exception as error:
            # Error receiving game data:
            print(error)
            print('Error: Connection error occurred when retrieving game data.')
            return 'connection_error'

async def character_info(name, realm, region):

    # Grabs overall character data including their ilvl.
    access_token = await get_access_token(region)
    info = await get_data(region, access_token, name=name, realm=realm)
    
    #print(info)

    if info == 'not_found' or info == 'connection_error' or info == 'credential_error':
        return info

    # If the data returned isn't an error string assume it found a character.
    else:
        try:
            character_sheet = {
                'name': info['name'],
                'level': info['level'],
                'race': 'null',
                'class': 'NULL'
            }
            return character_sheet
        except:
            print('failed')
            return

async def get_access_token(region):
    auth_path = 'https://%s.battle.net/oauth/token' % (region)
    auth_credentials = aiohttp.BasicAuth(login=WOW_CLIENT_ID, password=WOW_CLIENT_SECRET)

    try:
        async with aiohttp.ClientSession(auth=auth_credentials) as _client:
            async with _client.get(auth_path, params={'grant_type': 'client_credentials'}) as auth_response:
                assert auth_response.status == 200
                auth_json = await auth_response.json()
                return auth_json['access_token']

    except:
        # Error receiving token:
        print('Error: Unable to retrieve auth token')
        return 'credential_error'

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

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
        current_time = datetime.datetime.now()
        str_current_time = str(current_time)
        str_past_time = str(past_time)

        if str_current_time[0:10] != str_past_time[0:10]:

            data = []
            for x in char_list:
                data.append(await character_info(x,REALM,REGION))

            new_data = add_extras(data)
            final_data = process_data(new_data)
            await client.send_message((client.get_channel('534045914227277847')), final_data)

            past_time == current_time
        
        else:
            return

    async def looping_function(self):
        while True:
            await self.do_stuff()
            await asyncio.sleep(3600)

loop = asyncio.get_event_loop()
Daily_Poster = MyCog
Daily_Poster(loop)

@client.event
async def on_message(message):

    if (message.author == client.user):
        return
    
    if message.content == '!levels':

        data = []

        for x in char_list:
            data.append(await character_info(x,REALM,REGION))
        
        new_data = add_extras(data)
        final_data = process_data(new_data)
        await client.send_message(message.channel, final_data)

def add_extras(inpdata):
    
    j = 0

    while j < len(inpdata) :
        
        if inpdata[j]['name'] == "Logman" : 
            
            inpdata[j]['race'] = 'Dwarf'
            inpdata[j]['class'] = 'Hunter'
            match_found = True

        if inpdata[j]['name'] == "Xsmqt" : 
            
            inpdata[j]['race'] = 'Dwarf'
            inpdata[j]['class'] = 'Priest'
            match_found = True

        if inpdata[j]['name'] == "Raltick" : 
            
            inpdata[j]['race'] = 'Night Elf'
            inpdata[j]['class'] = 'Druid'
            match_found = True
        
        if match_found:
            j += 1
            match_found = False

    return inpdata


def process_data(data):
    i = 0
    k = 0

    name_order = []
    order_dict = {}
    final_str = ""
    
    while i < len(data):
        order_dict[data[i]['name']] = data[i]['level']
        i += 1

    def keyfunction(k):
        return order_dict[k]
    for key in sorted(order_dict, key=keyfunction, reverse=True):
        name_order.append(key)

    while k < len(data):
        j = 0
        match = False
        name = name_order[k]
        while match != True and j < len(data) :
            if data[j]['name'] == name : 
                final_str = final_str + str(data[j]['name']) + " - " + str(data[j]['race']) + " " + str(data[j]['class'])+ " - Level : " + str(data[j]['level']) +"\n"
                match = True
            else:
                j += 1
        k += 1
    return final_str


if __name__ == "__main__":
    
    f=open("wow_discord_token.txt","r")
    if f.mode == 'r':
        discordToken = f.read()

    f=open("wow_client_id.txt","r")
    if f.mode == 'r':
        WOW_CLIENT_ID = f.read()

    f=open("wow_client_secret.txt","r")
    if f.mode == 'r':
        WOW_CLIENT_SECRET = f.read()

    client.run(discordToken)
