import discord,typing
from discord.ext import commands
class Client(discord.Client):
    def __init__(self, 
                 intents, #make intents maybe?
                **options
                 ):
        super().__init__(intents,**options)

    def run(self, #overriding run is sketch, but should work
          token:str,
          *,
          reconnect:bool=True
          ):
        
        pass
    