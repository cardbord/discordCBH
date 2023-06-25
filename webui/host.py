import gradio as gr, pathlib,typing, discord, asyncio

path = pathlib.Path(__file__).parent
blocks = gr.Blocks(css=str(path)+"/app.css", title="CBH webUI")

class _guild_but:
    def __init__(self,g):
        self.g = g
        self.button = None

class create_webui:
    def __init__(self,*,show_guilds:bool=True,guilds:typing.List[discord.Guild]=None):
        self.guilds = guilds
        self.terminal = ""
        self.show_guilds = show_guilds
        

    def restart(self):
        print("This is a test")
        self.terminal += "restart bot command run \n"

    def retrieve_terminal(self):
        return self.terminal


    @property
    def demo(self):

        with blocks as d:
            with gr.Tab("Bot Management"):
                with gr.Row():
                    btn = gr.Button("Restart bot",elem_id="restart",elem_classes="restart")
                if self.show_guilds:
                
                    if self.guilds != None:
                        with gr.Row():
                            guildarr = []
                            for guild in self.guilds:
                                temp = _guild_but(guild)        
                                guildarr.append(temp)
                                
                                with gr.Box(visible=True):
                                    with gr.Row():
                                        
                                        with gr.Column(scale=1):
                                            if guild.icon:
                                                gr.ImageMask(interactive=False,value=(guild.icon.url[:len(guild.icon.url)-4]+"64"),elem_classes="imwrap",elem_id="imwrap")
                                            else:
                                                gr.ImageMask(interactive=False,value="https://media.discordapp.net/attachments/882677741441404938/1112052388031893504/R.jpg?width=662&height=662",elem_classes="imwrap",elem_id="imwrap")
                                        with gr.Column():
                                            gr.Textbox(label="Guild information",value=f"""{guild.name}
{guild.id}
{guild.member_count} members, {len(guild.members)} active
{guild.description if guild.description != None else ""}
""",elem_id="guild-background",elem_classes="guild-info")
                                        with gr.Column():
                                            temp.button = gr.Button(">")
                                

                            #guilds are a pain, figure out how to implement later
                
            with gr.Tab("Terminal"):
                terminal = gr.TextArea(label="Terminal",value="discordCBH output terminal",elem_id="terminal-background",elem_classes="terminal",lines=42)    
            
            

            
            btn.click(self.restart)

            d.load(self.retrieve_terminal,None,terminal,every=1)
            
        
        return d


    def launch(self):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        self.demo.queue().launch()

    def write(self,value:str):
        self.terminal+='\n'+value

    
