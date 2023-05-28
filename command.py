import context,datetime,asyncio, errors,uuid,typing,functools

class DiscordCommand:
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


    async def invoke(self,ctx:context.Context,*args,**kwargs):
        def wrap_invoke(ctx:context.Context,funct):
            @functools.wraps(funct)
            async def wrapped(*args,**kwargs):
                try:
                    works = await funct(*args,**kwargs)
                except:
                    failed = True
                return works
            return wrapped
        
            
        comm_to_run = wrap_invoke(ctx,self.funct)
        await comm_to_run(*args,**kwargs)





def Command(*,name:str=None,description:str=None,guild_ids:typing.List[int],options:typing.List[dict]):
    def wrap(cmd):
        return DiscordCommand(cmd,name,description,guild_ids,options)
    return wrap
