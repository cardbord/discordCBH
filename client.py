import discord,typing,asyncio
from webui.host import create_webui
from discord.ext import commands
class Client(discord.Client):
    def __init__(self, 
                 intents, #make intents maybe?
                **options
                 ):
        super().__init__(intents,**options)

    def run(self, #overriding run() is sketch, but should work
          token:str,
          with_webui:bool=True,
          *,
          show_guilds:bool=True,
          guilds:typing.List[discord.Guild] = None
          ):
        token = token.strip()
        #make login function here
        #then we make a connect function



        #AFTER BOT HAS STARTED, MAKE REQ FOR GUILDS AND RUN create_webui()
        
        if with_webui:
          webui = create_webui(show_guilds=show_guilds,guilds=guilds)
          try: #method already run in webui.host.launch(), but we run it here to ensure gradio doesn't throw any RuntimeErrors
            loop = asyncio.get_event_loop()
          except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
              
          loop.run_in_executor(None,webui.launch)