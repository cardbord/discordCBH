import context,datetime,asyncio, errors,uuid,typing,functools
from client import Client
import errors
class DiscordCommand:
    def __init__(self,command,client:Client,**kwargs):

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
        self.client = client;self.client._current_commands+=self

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





def Command(*,name:str=None,client:Client,description:str=None,guild_ids:typing.List[int],options:typing.List[dict]):
    '''
    deprecated, please use ``Client.Command()`` instead.

    alternative method for command creation, requiring discord client as a parameter instead. 
    
    '''

    def wrap(cmd):
        return DiscordCommand(cmd,client,name,description,guild_ids,options)
    return wrap
