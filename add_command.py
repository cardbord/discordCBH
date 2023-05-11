import json, typing, discord, aiohttp
from discord.ext import commands
from discord.http import Route
import errors

class DiscordRequest:
    def __init__(self,
                 _discord_client,
                 application_id
                 ):
        self._discord_client:typing.Union[discord.Client,commands.Bot] = _discord_client
        self.application_id = application_id

    @property
    def application_id(self):
        return self.application_id or self._discord_client.user.id



    def send_http(self,
                    modify_method:str,
                    guild_id,
                    location
                    
                    ):
        url = f"/applications/{self.application_id}"
        url+= "commands" if guild_id is None else "/guilds/{guild_id}/commands"
        url+=location
        return self._discord_client.http.request(Route(modify_method,url))
    


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
    