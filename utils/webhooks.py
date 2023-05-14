"""
The MIT License (MIT)

Copyright (c) 2022-present cardboard box

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

An extension to the discord.py library, bringing some features that do not
exist, or may not be included in the library. 
"""

import aiohttp, requests
from errors import HTTPError


class webhook:
    '''Represents a discord webhook
    
    uses POST, PATCH, DELETE requests to manipulate a specific webhook from discord's API
    requires full ownership of the webhook and administrator permissions

    webhook.execute(content,username,avatar_url)
    webhook.edit_message(message_id, content)
    webhook.delete_message(message_id) 
    webhook.modify(new_name,new_avatar,new_channel) -> webhook

    '''

    def __init__(self,id,type,guild_id,channel_id,name,application_id,webhook_token,avatar):
        self.webhook_id = id
        self.webook_type = type
        self.channel_id = channel_id
        self.name = name
        self.application_id = application_id
        self.guild = guild_id
        self.token = webhook_token
        self.avatar = avatar
        self.client_token = tooken
        self.client = clientses
        



    async def execute(self,*,content:str,username:str=None, avatar_url:str):
        self.client.session = aiohttp.ClientSession()
        if username is None:
            username = self.name
        url = f"https://discord.com/api/v9/webhooks/{self.webhook_id}/{self.token}"
        headers = {"Authorization": f"Bot {self.client_token}"}
        json = {'content':content,
        'username':username,
        'avatar_url':avatar_url
        }
        async with self.client.session.post(url,headers=headers,json=json) as session:
            if session.status in range(200,299):
                await self.client.session.close()
                return
            
            await self.client.session.close()
            raise HTTPError(f"command failed with code {session.status}")
            
            
            

    async def edit_message(self,*,message_id:int,content:str):
        self.client.session = aiohttp.ClientSession()
        url = f"https://discord.com/api/v9/webhooks/{self.webhook_id}/{self.token}/messages/{message_id}"
        headers = {"Authorization": f"Bot {self.client_token}"}
        json = {'content':content}
        async with self.client.session.patch(url,headers=headers,json=json) as session:
            if session.status in range(200,299):
                await self.client.session.close()
                return
            
            await self.client.session.close()
            raise HTTPError(f"command failed with code {session.status}")

    async def delete_message(self,*,message_id:int):
        self.client.session = aiohttp.ClientSession()
        url = f"https://discord.com/api/v9/webhooks/{self.webhook_id}/{self.token}/messages/{message_id}"
        headers = {"Authorization": f"Bot {self.client_token}"}
        async with self.client.session.delete(url,headers=headers) as session:
            if session.status == 204:
                await self.client.session.close()
                return
            
            await self.client.session.close()
            raise HTTPError(f"command failed with code {session.status}")
            


    async def modify(self,new_name:str=None,new_avatar:str=None,new_channel:int=None):

        '''Modifies an existing webhook with a new name, avatar and channel, provided a webhook ID is given
        returns a new webhook class on success'''
        
        self.client.session = aiohttp.ClientSession()
        url = f"https://discord.com/api/v9/webhooks/{self.webhook_id}"

        params = [new_name,new_avatar,new_channel]
        
        if params[0] is None:
            params[0] = self.name
        if params[1] is None:
            params[1] = self.avatar
        if params[2] is None:
            params[2] = self.channel_id

        headers = {"Authorization": f"Bot {self.token}"}
        json = {'name':params[0],
        'avatar?':params[1],
        'channel_id':params[2]
        }
        async with self.client.session.post(url,headers=headers,json=json) as session:
            if session.status in range(200,299):
                webhook_status = await session.text()
                webhook_status = eval(webhook_status.replace('null','None').replace('true','True'))
                await self.client.session.close()
                return webhook(
                    id=webhook_status['id'],
                    type=webhook_status['type'],
                    guild_id=webhook_status['guild_id'],
                    channel_id=webhook_status['channel_id'],
                    name=webhook_status['name'],
                    avatar=webhook_status['avatar'],
                    application_id=webhook_status['application_id'],
                    webhook_token=webhook_status['token']
                )



            
            await self.client.session.close()
            raise HTTPError(f"command failed with code {session.status}")




class discord_webhooks:

    '''Creates and manages webhooks for channels and guilds
    
    uses GET, POST, DELETE requests to manipulate webhooks from discord's API

    requires [MANAGE_WEBHOOKS] permissions

    discord_webhooks.get_webhook(webhook_id) -> webhook
    discord_webhooks.create_webhook(channel_id,webhook_name) -> webhook
    discord_webhooks.delete_webhook(webhook_id) -> None
    discord_webhooks.get_channel_webhooks(channel_id) -> arr
    discord_webhooks.get_guild_webhooks(guild_id) -> arr
    discord_webhooks.webhook_from_name(channel_id,webhook_name) -> webhook

    any failure in any of these functions will return None, promptly resulting in a NoneType error if manipulated. 

    '''

    def __init__(self,client,token):
        self.client = client     
        self.token = token
        global tooken
        tooken = self.token
        global clientses
        clientses = self.client
        


    async def get_webhook(self,webhook_id:int):

        '''Gets webhook from ID
        returns a webhook class on success'''


        headers = {"Authorization": f"Bot {self.token}"}
        r=requests.get(f"https://discord.com/api/v9/webhooks/{webhook_id}",headers=headers)
        if r.status_code in range(200,299):
            webhook_status = await r.text()
            webhook_status = eval(webhook_status.replace('null','None').replace('true','True'))
            
            return webhook(
                id=webhook_status['id'],
                type=webhook_status['type'],
                guild_id=webhook_status['guild_id'],
                channel_id=webhook_status['channel_id'],
                name=webhook_status['name'],
                avatar=webhook_status['avatar'],
                application_id=webhook_status['application_id'],
                webhook_token=webhook_status['token'],
            )
        
        raise HTTPError(f"command failed with code {r.status_code}")



    async def create_webhook(self,*,channel_id:int,webhook_name:str) -> webhook:

        '''Creates a webhook from a provided channel ID and webhook name
        returns a webhook class on success'''
        
        self.client.session = aiohttp.ClientSession()
        url = f"https://discord.com/api/v9/channels/{channel_id}/webhooks"
        headers = {"Authorization": f"Bot {self.token}"}
        json = {'name':webhook_name,
        'avatar?':None
        }
        async with self.client.session.post(url,headers=headers,json=json) as session:
            if session.status in range(200,299):
                webhook_status = await session.text()
                webhook_status = eval(webhook_status.replace('null','None').replace('true','True'))
                await self.client.session.close()
                return webhook(
                    id=webhook_status['id'],
                    type=webhook_status['type'],
                    guild_id=webhook_status['guild_id'],
                    channel_id=webhook_status['channel_id'],
                    name=webhook_status['name'],
                    avatar=webhook_status['avatar'],
                    application_id=webhook_status['application_id'],
                    webhook_token=webhook_status['token'],
                )


            
            await self.client.session.close()
            raise HTTPError(f"command failed with code {session.status}")         
  

    async def delete_webhook(self,*,webhook_id:int):

        '''Deletes an existing webhook given the ID
        returns a status 204 (no content) if successful (the program will manage this for you)'''

        self.client.session = aiohttp.ClientSession()
        url = f"https://discord.com/api/v9/webhooks/{webhook_id}"
        headers = {"Authorization": f"Bot {self.token}"}
        async with self.client.session.delete(url,headers=headers) as session:
            if session.status == 204:
                await self.client.session.close()
                return
            
            await self.client.session.close()
            raise HTTPError(f"command failed with code {session.status}") 



    async def get_channel_webhooks(self,*,channel_id:int):

        '''Requests existing webhooks from a specific channel, given the channel ID
        returns an array on success'''

        headers = {"Authorization": f"Bot {self.token}"}
        r=requests.get(f"https://discord.com/api/v9/channels/{channel_id}/webhooks",headers=headers)
        if r.status_code in range(200,299):
            return eval(r.text.replace('null','None').replace('true','True'))
        
        raise HTTPError(f"command failed with code {r.status_code}")

    async def get_guild_webhooks(self,*,guild_id:int):

        '''Requests existing webhooks from a specific guild, given the guild ID
        returns an array on success'''

        headers = {"Authorization": f"Bot {self.token}"}
        r=requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/webhooks",headers=headers)
        if r.status_code in range(200,299):
            return eval(r.text.replace('null','None').replace('true','True'))
        raise HTTPError(f"command failed with code {r.status_code}")

    async def webhook_from_name(self,*,channel_id:int,webhook_name:str):  
        
        '''Requests existing webhooks using get_channel_webhooks and then searching the JSON data for the webhook required
        returns webhook on success'''


        current_webhooks = await discord_webhooks.get_channel_webhooks(self,channel_id=channel_id)
        for _ in current_webhooks:
            if str(_['name']) == webhook_name:
                return webhook(
                    id=_['id'],
                    type=_['type'],
                    guild_id=_['guild_id'],
                    channel_id=_['channel_id'],
                    name=_['name'],
                    application_id=_['application_id'],
                    webhook_token=_['token'],
                    avatar=_['avatar']
                )
        return None