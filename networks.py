from client import Client
import asyncio,errors,functools,context,uuid,typing

class Network:
    def __init__(self,name):
        self.client = None #assigned with _assign_network_client executed by Client's network assignment function 
        self.name = name
        self._network_commands = []
        

    async def _assign_network_client(self,client):
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
            self.id = kwargs.get('type') or uuid.uuid4()
            self.client = None
            

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
            await comm_to_run(*args,**kwargs)

    def Command(self,*,name:str=None,description:str=None,guild_ids:typing.List[int],options:typing.List[dict]):
        '''
        Method of command creation within a network
        '''

        def wrap(cmd):
            new_command = self.DiscordNetworkCommand(cmd,name,description,guild_ids,options)
            self._network_commands.append(new_command)
            return new_command
        return wrap
