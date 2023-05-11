import discord
from discord.ext import commands
import datetime
import typing
from warnings import warn
from discord.utils import snowflake_time
import errors



class Context:
    def __init__(self,
                 _command_json:dict,
                 _discord_client:typing.Union[discord.Client,commands.Bot],
                 log
                 ):
        self._full_command_json = _command_json
        self._token = _command_json["token"]
        self.message = None
        self.data = _command_json["data"]
        self.interaction_id = _command_json["id"]
        self.time_created_at: datetime.datetime = snowflake_time(int(self.interaction_id))
        self.bot = _discord_client
        self._log = log
        self.responded = False
        self.deferred = False
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
    
    @property
    def me(self) -> typing.Union[discord.Member, discord.ClientUser]:
        """
        Bot member instance of the command invoke.
        Will return ``discord.Member`` normally.
        If the command was invoked in a DM, then this is ``discord.ClientUser``
        """

        return self.guild.me if self.guild != None else self.bot.user
    
    async def send(self,
                content:str="",
                *,
                embed:discord.Embed=None,
                tts:bool=False,
                file:discord.File=None,
                allowed_mentions:discord.AllowedMentions=None,
                hidden:bool=False,
                delete_after:float=None,
                components:typing.List[dict] = None,
                   ):
        if embed:
            embeds = [embed]
        if not isinstance(embeds,list):
            raise errors.IncorrectFormat("No embed passed")
        
        #UNFINISHED. DO LATER.
        
