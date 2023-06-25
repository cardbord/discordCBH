import json, typing, discord, aiohttp, asyncio
from discord.ext import commands
from discord.http import Route
import client

class DiscordHTTPGateway:
    def __init__(self,token,loop=None):
        __httpsession = aiohttp.ClientSession()
        _token = token
        _loop = asyncio.get_event_loop() if loop is None else loop


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