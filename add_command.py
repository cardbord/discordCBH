import json, typing, discord, aiohttp, asyncio,sys,requests
from discord.ext import commands
from discord.http import Route
import client
from globals import __version__
import errors
from command import DiscordCommand
class DiscordHTTPGateway:
    def __init__(self,token,client:client.Client,loop=None):
        self.__httpsession = None #init through _create_dcHTTPgateway_session()
        self._token = token
        self.client = client
        self._loop = asyncio.get_event_loop() if loop is None else loop
        self.user_agent = f'DiscordBot (https://github.com/cardbord/discordCBH {__version__}) Python/{sys.version_info[0]}.{sys.version[1]} aiohttp/{aiohttp.__version__}'

    async def _create_dcHTTPgateway_session(self):
        self.__httpsession = aiohttp.ClientSession(connector=None)
        #maybe create some token checking here like discord.py does?

    async def request(self,method:str,url:str,json:dict):
        
        async with self.__httpsession.request(method,url) as req:
            pass #finish later

    async def _call_initial_command_post(self):
        reqs = DiscordRequest(self.client,self.client.application_id)
        current_commands_registered:list[dict] = reqs._get_global_slash_commands()
        
        client_registered = self.client._current_commands

        to_register = []
        #find commands not mentioned at all, delete them
        #register them
        client_registered:list[DiscordCommand]
        for network in client_registered:
            for command in network:
                found = False
                for command_registered_at_discord in current_commands_registered:
                    command:DiscordCommand
                    if command._cmd_json.get('name') == command_registered_at_discord.get('name'): 
                        if command._cmd_json

                    
                    




class DiscordRequest:
    def __init__(self,
                 _discord_client,
                 application_id
                 ):
        self._discord_client:client.Client = _discord_client
        self.application_id = application_id

    @property
    def application_id(self):
        return self.application_id or self._discord_client.user.id



    def send_http(self,
                    modify_method,
                    guild_id,
                    location
                    
                    ):
        url = f"/applications/{self.application_id}"
        url+= "commands" if guild_id is None else "/guilds/{guild_id}/commands"
        url+=location
        return self._discord_client.http.request(Route(modify_method,url))
    

    def command_response(
            self,
            token,
            use_webhook,
            modify_method,
            interaction_id=None,
            location="",
            **kwargs
    ):
        url = f"/interactions/{interaction_id}/{token}/callback" if use_webhook is False else f"/webhooks/{self.application_id}/{token}"

        url+=location
        return self._discord_client.http.request(Route(modify_method,url),**kwargs)

    
    
    
    
    def add_global_slash_command(self,
                                 cmdjson):
        url = f"https://discord.com/api/v10/applications/{self.application_id}/commands"
        headers = f'Bot {self._discord_client.dcHTTP._token}'
        r = requests.post(url=url,data=cmdjson,headers=headers)
        if r.status_code in range(200,299):
            return
        elif r.status_code == errors.HTTPResponseException.forbidden:
            raise errors.HTTPException.Forbidden('This slash command cannot be added.')
        else:
            raise errors.HTTPException(f'command failed with code {r.status_code}')
        

    def add_slash_command(self,
                            guild_id,
                            name:str,
                            description:str,
                            options:list=None,
                            context:dict=None 
                            ):
        cmdjson = {"name":name,
                    "description":description,
                    "options":options or []
                    }
        if context != None:
            new_cmdjson = {"type": context["type"], "name": context["name"]}
            return self.send_http(json=new_cmdjson,modify_method="POST",guild_id=guild_id)
        return self.send_http(json=cmdjson,modify_method="POST",guild_id=guild_id)
    
    def request_with_files(self,_resp,files:typing.List[discord.File],token,modify_method,location=""):
        form = aiohttp.FormData()
        form.add_field("payload_json",json.dumps(_resp))
        for i in range(len(files)):
            name = f"file{i if len(files) > 1 else ''}"
            bru = files[i]
            form.add_field(name,bru.fp,filename=bru.filename,content_type="application/octet-stream")
        
        return self.command_response(token,True,modify_method,data=form,files=files,location=location)

    def _get_global_slash_commands(self,
                                   with_locals:bool=False):
        url = f'https://discord.com/api/v10/applications/{self.application_id}/commands'
        headers = {'Authorization' :f'Bot {self._discord_client.dcHTTP._token}'}
        if with_locals:
            data = {"with_localizations?":True}
            r = requests.get(url=url,data=data,headers=headers)
        else:
            r = requests.get(url=url,headers=headers)
        if r.status_code in range(200,299):
            return r.text


    
    
    def post_initial_response(self,_resp,interaction_id,token):
        return self.command_response(token,False,"POST",interaction_id,json=_resp)
    
    def post_second(self,_resp,token,files:typing.List[discord.File]=None):
        if files != None:
            return self.request_with_files(_resp,files,token,"POST")
        else:
            return self.command_response(token,True,"POST",json=_resp)
    def patch(self,_resp,token,message_id,files:typing.List[discord.File]=None):
        url = f"/messages/{message_id}"
        if files != None:
            return self.request_with_files(_resp,files,token,"PATCH",url)
        else:
            return self.command_response(token,True,"PATCH",location=url,json=_resp)