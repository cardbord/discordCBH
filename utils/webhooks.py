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

import aiohttp, requests, typing
from errors import HTTPException
from ..context import Context
from ..client import Client
from enum import IntEnum

class WebhookType(IntEnum):
    incoming = 1
    channel_follower = 2
    application = 3

class webhook:
    '''Represents a discord webhook
    
    uses POST, PATCH, DELETE requests to manipulate a specific webhook from discord's API
    requires full ownership of the webhook and administrator permissions

    webhook.execute(content,username,avatar_url)
    webhook.edit_message(message_id, content)
    webhook.delete_message(message_id) 
    webhook.modify(new_name,new_avatar,new_channel) -> webhook

    '''

    def __init__(self,id:int,type:int,guild_id:int,channel_id:int,name:str,application_id:int,webhook_token:str,avatar:str,token:str,client:Client):
        self.webhook_id = id
        self.client = client
        self.channel_id = channel_id
        self.name = name
        self.application_id = application_id
        self.guild = guild_id
        self.token = webhook_token
        self.avatar = avatar
        self.client_token = token
        self.type = type
        self._client_session = self.client.dcHTTP.__httpsession



    async def execute(self,*,content:str,username:str=None, avatar_url:str=None):
        
        if username is None:
            username = self.name
        url = f"https://discord.com/api/v9/webhooks/{self.webhook_id}/{self.token}"
        headers = {"Authorization": f"Bot {self.client_token}"}
        json = {'content':content,
        'username':username if username else self.name,
        'avatar_url':avatar_url if avatar_url else self.avatar
        }
        async with self._client_session.post(url,headers=headers,json=json) as session:
            if session.status in range(200,299):
                
                return
            
            
            raise HTTPException(f"command failed with code {session.status}")#<- make actual response messages later!
            
            
            

    async def edit_message(self,*,message_id:int,content:str):
        self._client_session = aiohttp.ClientSession()
        url = f"https://discord.com/api/v9/webhooks/{self.webhook_id}/{self.token}/messages/{message_id}"
        headers = {"Authorization": f"Bot {self.client_token}"}
        json = {'content':content}
        async with self._client_session.patch(url,headers=headers,json=json) as session:
            if session.status in range(200,299):
                
                return
            
            
            raise HTTPException(f"command failed with code {session.status}")

    async def delete_message(self,*,message_id:int):
        self._client_session = aiohttp.ClientSession()
        url = f"https://discord.com/api/v9/webhooks/{self.webhook_id}/{self.token}/messages/{message_id}"
        headers = {"Authorization": f"Bot {self.client_token}"}
        async with self._client_session.delete(url,headers=headers) as session:
            if session.status == 204:
                
                return
            
            
            raise HTTPException(f"command failed with code {session.status}")
            


    async def modify(self,new_name:str=None,new_avatar:str=None,new_channel:int=None):

        '''Modifies an existing webhook with a new name, avatar and channel, provided a webhook ID is given
        returns a new webhook class on success'''
        
        self._client_session = aiohttp.ClientSession()
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
        async with self._client_session.post(url,headers=headers,json=json) as session:
            if session.status in range(200,299):
                webhook_status = await session.text()
                webhook_status = eval(webhook_status.replace('null','None').replace('true','True').replace('false','False'))
                
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



            raise HTTPException(f"command failed with code {session.status}")

    @classmethod
    async def from_id(cls,ctx:Context,webhook_id:int):
        headers = {"Authorization":f"Bot {ctx._token}"}
        r = requests.get(f"https://discord.com/api/v9/webhooks/{webhook_id}",headers=headers)
        if r.status_code in range(200,299):
            webhook_status = await r.text()
            webhook_status = eval(webhook_status.replace('null',None).replace('true','True').replace('false','False'))

            return cls(
            id=webhook_status['id'],
            type=webhook_status['type'],
            guild_id=webhook_status['guild_id'],
            channel_id=webhook_status['channel_id'],
            name=webhook_status['name'],
            avatar=webhook_status['avatar'],
            application_id=webhook_status['application_id'],
            webhook_token=webhook_status['token'],
            token=ctx._token
        )
        raise HTTPException(f"command failed with code {r.status_code}")

        


async def get_webhook(ctx:Context,webhook_id:int) -> typing.Optional[webhook]:

    '''Gets webhook from ID
    returns a webhook class on success'''


    headers = {"Authorization": f"Bot {ctx._token}"}
    r=requests.get(f"https://discord.com/api/v9/webhooks/{webhook_id}",headers=headers)
    if r.status_code in range(200,299):
        webhook_status = await r.text()
        webhook_status = eval(webhook_status.replace('null','None').replace('true','True').replace('false','False'))
        
        return webhook(
            id=webhook_status['id'],
            type=webhook_status['type'],
            guild_id=webhook_status['guild_id'],
            channel_id=webhook_status['channel_id'],
            name=webhook_status['name'],
            avatar=webhook_status['avatar'],
            application_id=webhook_status['application_id'],
            webhook_token=webhook_status['token'],
            token=ctx._token
        )
    
    raise HTTPException(f"command failed with code {r.status_code}")



async def create_webhook(ctx:Context,client:Client,*,channel_id:int,webhook_name:str,webhook_avatar:str=None) -> typing.Optional[webhook]:

    '''Creates a webhook from a provided channel ID and webhook name
    returns a webhook class on success'''
    
    client_session = client.http.__httpsession
    url = f"https://discord.com/api/v9/channels/{channel_id}/webhooks"
    headers = {"Authorization": f"Bot {ctx._token}"}
    json = {'name':webhook_name,
    'avatar?':webhook_avatar
    }
    async with client_session.post(url,headers=headers,json=json) as session:
        if session.status in range(200,299):
            webhook_status = await session.text()
            webhook_status = eval(webhook_status.replace('null','None').replace('true','True').replace('false','False'))
            
            return webhook(
                id=webhook_status['id'],
                type=webhook_status['type'],
                guild_id=webhook_status['guild_id'],
                channel_id=webhook_status['channel_id'],
                name=webhook_status['name'],
                avatar=webhook_status['avatar'],
                application_id=webhook_status['application_id'],
                webhook_token=webhook_status['token'],
                token=ctx._token
            )


        
        
        raise HTTPException(f"command failed with code {session.status}")         


async def delete_webhook(ctx:Context,client:Client,*,webhook_id:int):

    '''Deletes an existing webhook given the ID
    returns a status 204 (no content) if successful'''

    client_session = client.http.__httpsession
    url = f"https://discord.com/api/v9/webhooks/{webhook_id}"
    headers = {"Authorization": f"Bot {ctx._token}"}
    async with client_session.delete(url,headers=headers) as session:
        if session.status == 204:
            
            return
        
        
        raise HTTPException(f"command failed with code {session.status}") 



async def get_channel_webhooks(ctx:Context,*,channel_id:int)-> typing.Optional[list]:

    '''Requests existing webhooks from a specific channel, given the channel ID
    returns an array on success'''

    headers = {"Authorization": f"Bot {ctx._token}"}
    r=requests.get(f"https://discord.com/api/v9/channels/{channel_id}/webhooks",headers=headers)
    if r.status_code in range(200,299):
        return eval(r.text.replace('null','None').replace('true','True').replace('false','False'))
    
    raise HTTPException(f"command failed with code {r.status_code}")

async def get_guild_webhooks(ctx:Context,*,guild_id:int)-> typing.Optional[list]:

    '''Requests existing webhooks from a specific guild, given the guild ID
    returns an array on success'''

    headers = {"Authorization": f"Bot {ctx._token}"}
    r=requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/webhooks",headers=headers)
    if r.status_code in range(200,299):
        return eval(r.text.replace('null','None').replace('true','True').replace('false','False'))
    raise HTTPException(f"command failed with code {r.status_code}")

async def webhook_from_name(ctx:Context,*,channel_id:int,webhook_name:str)-> typing.Optional[webhook]:  
    
    '''Requests existing webhooks using get_channel_webhooks and then searching the JSON data for the webhook required
    returns webhook on success'''


    current_webhooks = await get_channel_webhooks(ctx,channel_id=channel_id)
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
                avatar=_['avatar'],
                token=ctx._token
            )
    return None