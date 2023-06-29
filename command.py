import context,datetime,discord,asyncio, errors,uuid,typing,functools
from client import Client
import errors
from enum import IntEnum

#THIS -> https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure

async def _assign_coroutine_as_invoke(coro,command):
        if not asyncio.iscoroutinefunction(coro):
            raise errors.IncorrectType(f"Provided function {coro.__name__} is not asynchronous, please convert to a coroutine.")
        def wrap_funct(funct):
            @functools.wraps(funct)
            async def wrapped():
                failed = False
                try:
                    works = await funct()
                except Exception as e:
                    failed = True
                finally:
                    if failed:
                        command.client.webui.write(f"""{command.name}'s pre/post-invoke command {coro.__name__} contains the exception
                                                {e}
                                                that cannot be resolved.""")
                        raise errors.CommandCreationException(f"""{command.name}'s pre/post-invoke command {coro.__name__} contains the exception
                                                            {e}
                                                            that cannot be resolved.""")
                return works
            return wrapped
        return wrap_funct(coro)


class OptionType(IntEnum):
    subcommand = 1
    subcommand_group = 2
    string = 3
    integer = 4
    boolean = 5
    user = 6
    channel = 7
    role = 8
    mentionable = 9
    number = 10
    attachment = 11

class Choice:
    def __init__(self,name:str,value:str):
        self.name = name
        self.value = value

    @property
    def json(self):
        return {
            "name":self.name,
            "value":self.value
        }
    
    def __repr__(self):
        return self.json
    



class Option:
    def __init__(self,
                 *,
                 type:typing.Union[OptionType,int],
                 name:str,
                 description:str,
                 required:bool=True,
                 choices:typing.List[Choice]=None,
                 min_value:int=0,
                 max_value:int=20,
                 min_length:int=0,
                 max_length:int=100,
                 channel_types:typing.List[discord.Channel]=None):
        self.type = type
        self.description = description
        self.name = name
        self.required = required
        self.choices = choices
        self.min_value = min_value
        self.max_value = max_value
        self.min_length = min_length
        self.max_length = max_length
        self.channel_types = channel_types

    @property
    def json(self):
        data = {
            "name":self.name,
            "description":self.description,
            "type":self.type,
            "required":self.required,
        }
        if self.choices != None:
            data['choices'] = self.choices
        if self.max_length != None:
            data['max_length'] = self.max_length
        if self.min_length != None:
            data['min_length'] = self.min_length
        if self.max_value != None:
            data['max_value'] = self.max_value
        if self.min_value != None:
            data['min_value'] = self.min_value
        if self.channel_types != None:
            data['channel_types'] = self.channel_types
        return data

    def __repr__(self):
        return self.json
    
class AppCommandType(IntEnum):
    chat_input = 1
    user = 2
    message = 3

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
        self.type = kwargs.get('type') or AppCommandType.chat_input
        self.id = kwargs.get('id') or str(uuid.uuid4())
        self.client = client;self.client._append_checked_command(self,0)
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



def Command(*,name:str=None,client:Client,description:str=None,guild_ids:typing.List[int]=None,options:typing.List[dict]=None,nsfw:bool):
    '''
    deprecated, please use ``Client.Command()`` instead.

    alternative method for command creation, requiring discord client as a parameter instead. 
    
    '''

    def wrap(cmd):
        return DiscordCommand(cmd,client,name=name,description=description,guild_ids=guild_ids,options=options,nsfw=nsfw)
    return wrap
