import discord,typing,asyncio
from webui.host import create_webui
from discord.ext import commands
from command import DiscordCommand
class Client(discord.Client):
    def __init__(self, 
                 intents, #make intents maybe?
                **options
                 ):
        super().__init__(intents,**options)
        self._current_commands = []

    def create_webui_overwritten(self,show_guids:bool=True,guilds:typing.List[discord.Guild]=None):
       '''alternative creation of webui that can be used before `Client.run` or replacing a current webui
       when created, webui will not be created again in `Client.run`'''
       self.webui = create_webui(show_guilds=show_guids,guilds=guilds)

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
        #then make guild reqs for webui (if with_webui)



        #AFTER BOT HAS STARTED, MAKE REQ FOR GUILDS AND RUN create_webui()
        
        if with_webui:
          if not hasattr(self,'webui'): 
            self.webui = create_webui(show_guilds=show_guilds,guilds=guilds)
          try: #method already run in webui.host.launch(), but we run it here to ensure gradio doesn't throw any RuntimeErrors
            loop = asyncio.get_event_loop()
          except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
              
          loop.run_in_executor(None,self.webui.launch)

    def Command(self,*,name:str=None,description:str=None,guild_ids:typing.List[int],options:typing.List[dict]):
      def wrap(cmd):
          return DiscordCommand(cmd,self,name,description,guild_ids,options)
      return wrap
    