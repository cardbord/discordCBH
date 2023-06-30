import asyncio,errors,functools,context,uuid,typing
from command import _assign_coroutine_as_invoke

class Network:
    '''
    Multi-file management of commands.

    After creating a network, `Network.Command()` returns a `DiscordNetworkCommand`, same as `DiscordCommand` except without a client attribute.
    This is assigned during `Client.add_network()`

    '''
    def __init__(self,name:str=None):
        self.client = None #assigned with _assign_network_client executed by Client's network assignment function 
        self.name = name if name else self.__class__.__name__
        self._network_commands = []
        

    async def _assign_network_client(self,client):
        """
        Method of assigning a client to the network post init
        """
        self.client = client
        for netzwerkcommand in self._network_commands:
            netzwerkcommand.client = client


    class DiscordNetworkCommand:
        def __init__(self,command,**kwargs):

            if not asyncio.iscoroutinefunction(command):
                raise errors.IncorrectType(f"Provided function {command} is not asynchronous, please convert to a coroutine.")
            if (not isinstance(kwargs.get('name'),str) and kwargs.get('name') != None) or len(kwargs.get('name')) not in range(1,32):
                raise errors.IncorrectFormat(f"Provided name {kwargs.get('name')} must be a string between 1 to 32 characters.")
            self.funct = command
            self.name = kwargs.get('name') or self.funct.__name__
            self.description = kwargs.get('description') or f"{self.name}"
            self.options = kwargs.get('options') or None
            self.guild_ids = kwargs.get('guild_ids')
            self.type = kwargs.get('type') or 1
            self.id = kwargs.get('id') or str(uuid.uuid4())
            self.client = None
            self.nsfw = kwargs.get('nsfw') or False
            self.__before_invoke = None
            self.__after_invoke = None

        async def before_invoke(self,coro):
            """
            Assigns a coroutine to be executed before the invoke of a command.
            """
            
            self.__before_invoke = _assign_coroutine_as_invoke(coro,self)

        async def post_invoke(self,coro):
            """
            Assigns a coroutine to be executed after the invoke of a command.
            """

            self.__after_invoke = _assign_coroutine_as_invoke(coro,self)



        async def invoke(self,ctx:context.Context,*args,**kwargs):
            def wrap_invoke(ctx:context.Context,funct):
                @functools.wraps(funct)
                async def wrapped(*args,**kwargs):
                    try:
                        works = await funct(*args,**kwargs)
                    except Exception as e:
                        ctx.command_failed = True
                    finally:
                        if ctx.command_failed:
                            self.client.webui.write(f"""{self.name} raised an error:
                            {e}""")
                            raise errors.CommandInvokeException(f"""{self.name} raised an error:
                                                            {e}""")
                    return works
                return wrapped
            
                
            comm_to_run = wrap_invoke(ctx,self.funct)
            if self.__before_invoke:
                await self.__before_invoke()
            
            await comm_to_run(*args,**kwargs)

            if self.__after_invoke:
                await self.__after_invoke()


        @property
        def _cmd_json(self):
            cmdjson = {"name":self.name,
                        "description":self.description,
                        "options":self.options or []
                        }
            if self.type:
                cmdjson['type'] = self.type or 1
            if self.nsfw!=False:
                cmdjson['nsfw?'] = self.nsfw
            return cmdjson



    def Command(self,*,name:str=None,description:str=None,guild_ids:typing.List[int]=None,options:typing.List[dict]=None,nsfw:bool=False):
        '''
        Method of command creation within a network
        '''

        def wrap(cmd):
            new_command = self.DiscordNetworkCommand(cmd,name,description,guild_ids,options,nsfw=nsfw)
            self._network_commands.append(new_command)
            return new_command
        return wrap
