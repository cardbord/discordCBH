import discord
from discord.ext import commands
import datetime
import typing
from discord.utils import snowflake_time
import errors
import add_command as http
import client


class Context:
    def __init__(self,
                 _http:http.DiscordRequest,
                 _command_json:dict,
                 _discord_client:client.Client,
                 ):
        self._http = _http
        self._full_command_json = _command_json
        self._token = _command_json["token"]
        self.message = None
        self.data = _command_json["data"]
        self.interaction_id = _command_json["id"]
        self.time_created_at: datetime.datetime = snowflake_time(int(self.interaction_id))
        self.bot = _discord_client
        self.responded = False
        self.command_failed = False
        self.values = _command_json["data"]["values"] if "values" in _command_json else None
        self.guild_id = int(_command_json["guild_id"]) if "guild_id" in _command_json.keys() else None
        self.author_id = int(_command_json["user"]["id"])  if "member" in _command_json.keys() else None
        self.channel_id = int(_command_json["channel_id"])
        if self.guild != None:
            self.author = discord.Member(_command_json["member"],state=self.bot._connection,guild=self.guild) 
        elif self.guild_id != None:
            self.author = discord.User(data=_command_json["member"]["user"],state=self.bot._connection)
        else:
            self.author = discord.User(data=_command_json["user"],state=self.bot._connection)

        
    @property
    def guild(self) -> typing.Optional[discord.Guild]:
        """
        Guild instance where the command was invoked.
        If a command was invoked in a DM, then this is ``None``
        """
        
        return self.bot.get_guild(self.guild_id) if self.guild_id!=None else None
    
    @property
    def channel(self) -> typing.Optional[typing.Union[discord.TextChannel,discord.DMChannel]]:
        """
        Channel instance where the command was invoked.
        If a command was invoked in a DM, then this is ``None``
        """

        return self.bot.get_channel(self.channel_id)
    
    @property
    def voice_client(self) -> typing.Optional[discord.VoiceProtocol]:
        """
        VoiceClient instance where the command was invoked.
        If not connected to voice, then this is ``None``
        """

        return self.guild.voice_client if self.guild!=None else None
    
    async def send(self,
                content:str="",
                *,
                embeds: typing.List[discord.Embed]=None,
                tts:bool=False,
                files: typing.List[discord.File]=None,
                allowed_mentions:discord.AllowedMentions=None,
                hidden:bool=False,
                delete_after:float=None,
                components:typing.List[dict] = None,
                   ) -> typing.Union[discord.Message,dict]:
        

        if hidden is True and delete_after != None:
            raise errors.IncorrectFormat("A hidden message cannot be deleted.")

        if embeds != None:
            if not isinstance(embeds,list):
                raise errors.IncorrectFormat("No embeds passed.")
            elif len(embeds) > 10:
                raise errors.IncorrectFormat(f"Cannot pass more than 10 embeds. Please remove {len(embeds)-10} embeds.")
            else:
                for i in embeds:
                    i.to_dict()
        if files != None:
            if not isinstance(files,list):
                raise errors.IncorrectFormat("No files passed.")
        mes_json = {
            "content":content,
            "tts":tts,
            "embeds":embeds if embeds else [],
            "allowed_mentions":allowed_mentions,
            "components":components or [],
        }
        if hidden != None:
            mes_json["flags"] = 64

        initial = True if self.responded else False
        if initial:
            if files == None:
                jsond = {"type":4,"data":mes_json}

                await self._http.post_initial_response(jsond,self.interaction_id,self._token)
                if hidden is False:
                    resp = await self._http.patch({},self._token,"@original")
                else:
                    resp = {}
            self.responded = True
        else:
            resp = await self._http.post_second(mes_json,self._token,files)
        discord_message = None
        if not hidden:
            discord_message = discord.Message(
                state=self.bot._connection,
                data=resp,
                channel=self.channel,
                
            )
        if discord_message:

            return discord_message
        else:
            return resp
        
    


    async def reply(self,
                    content:str="",
                    *,
                    embeds:typing.List[discord.Embed]=None,
                    tts:bool=False,
                    files:typing.List[discord.File]=None,
                    allowed_mentions:discord.AllowedMentions=None,
                    hidden:bool=False,
                    delete_after:float=None,
                    components:typing.List[dict]=None,
                    ) -> typing.Union[discord.Message,dict]:
        return await self.send(content,embeds=embeds,tts=tts,files=files,allowed_mentions=allowed_mentions,hidden=hidden,delete_after=delete_after,components=components)

    async def say(self,
                    content:str="",
                    *,
                    embeds:typing.List[discord.Embed]=None,
                    tts:bool=False,
                    files:typing.List[discord.File]=None,
                    allowed_mentions:discord.AllowedMentions=None,
                    hidden:bool=False,
                    delete_after:float=None,
                    components:typing.List[dict]=None,
                    ) -> typing.Union[discord.Message,dict]:
        return await self.send(content,embeds=embeds,tts=tts,files=files,allowed_mentions=allowed_mentions,hidden=hidden,delete_after=delete_after,components=components)
