import discord,typing,asyncio
import networks
import errors
from webui.host import create_webui
from command import DiscordCommand
from add_command import  DiscordHTTPGateway
class Client(discord.Client):
    def __init__(self, 
                 intents, #make intents maybe?
                **options
                 ):
        super().__init__(intents,**options)
        self._current_commands = [[]]
        self.__current_command_names = []
        self.networks = []
        self.loop = asyncio.get_event_loop()
        self.dcHTTP = DiscordHTTPGateway(None,self,self.loop) #assign token in run()

    def _append_checked_command(self,command:typing.Union[networks.Network.DiscordNetworkCommand,DiscordCommand],position:int=0):
      """
      used as a check for matching command names in _current_commands before finally appending.
      don't use unless you're registering your command without using DiscordCommand or DiscordNetworkCommand.
      param position is unnecessary unless networks are used.
      """
      
      if command.name in self.__current_command_names:
          raise errors.CommandCreationException(f"Command {command.name} has a matching name with an already registered command")
      else:
         self._current_commands[position].append(command)
         self.__current_command_names.append(command.name)
          

    def create_webui_overwritten(self,show_guids:bool=True,guilds:typing.List[discord.Guild]=None):
       '''alternative creation of webui that can be used before `Client.run` or replacing a current webui
       when created, webui will not be created again in `Client.run`'''
       self.webui = create_webui(show_guilds=show_guids,guilds=guilds)

    def run(self, #overriding run() is sketch, but should work
          token:str,
          with_webui:bool=True,
          *,
          show_guilds:bool=True,
          ):
        token = token.strip()
        self.dcHTTP._token = token
        #make login function here (probably just initialise DiscordHTTPGateway and then run _create_dcHTTPgateway_session())
        
        #self.dc_login()?

        #then we make an event loop init

        #self.init_event_loop()? 

        #require a connection to d.py (or at least an initialisation of it's client's http for dpy commands)
        loop = asyncio.get_event_loop()
        #self.start() or self.login() and self.connect()

        #AFTER BOT HAS STARTED, MAKE REQ FOR GUILDS AND RUN create_webui()
        
        #(assuming bot has started and made connection to dpy:)
        if with_webui:
          if not hasattr(self,'webui'):
            
            guilds = []
            if show_guilds:
              for guild in self.guilds:
                  guilds.append(guild)
            self.webui = create_webui(self,show_guilds=show_guilds,guilds=guilds)
          try: #method already run in webui.host.launch(), but we run it here too to ensure gradio doesn't throw any RuntimeErrors (it seems to differ for different devices)
            loop = asyncio.get_event_loop()
          except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
              
          loop.run_in_executor(None,self.webui.launch)

    def Command(self,*,name:str=None,description:str=None,guild_ids:typing.List[int],options:typing.List[dict]):
      def wrap(cmd):
          return DiscordCommand(cmd,self,name,description,guild_ids,options)
      return wrap
    
    async def add_network(self,network:networks.Network):
      """
      A method for adding networks to the client
      """


      await network._assign_network_client(self)
      self.networks.append((f"{network.name}",len(self.networks+1)))
      self._current_commands.append([])
      for command in network._network_commands:
        self._append_checked_command(command,len(self.networks)-1)