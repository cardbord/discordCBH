import discord,typing
from discord.ext import commands
class Client(discord.Client):
    def __init__(self, 
                 client:typing.Union[discord.Client,commands.Bot],
                 intents #make intents maybe?

                 ):
        self.client = client

    def run(self, #overriding run is sketch, but should work
          token:str,
          *,
          reconnect:bool=True
          ):
        
        pass
    