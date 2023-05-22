import gradio as gr, pathlib,asyncio
path = pathlib.Path(__file__).parent
blocks = gr.Blocks(css=str(path)+"/app.css")

class _guild_but:
    def __init__(self,g):
        self.g = g
        self.button = None

class create_webui:
    def __init__(self,*,show_guilds:bool=True,guilds:list=None):
        self.guilds = guilds
        self.terminal = ""
        self.show_guilds = show_guilds
        

    def restart(self):
        print("This is a test")

    def retrieve_terminal(self):
        return self.terminal


    @property
    def demo(self):

        with blocks as d:
            with gr.Tab("Bot Management"):
                with gr.Row():
                    btn = gr.Button("Restart bot",elem_id="restart",elem_classes="restart")
            with gr.Tab("Terminal"):
                terminal = gr.TextArea(label="Terminal",value="discordCBH output terminal",elem_id="terminal-background",elem_classes="terminal")    
            if self.show_guilds:
                if self.guilds != None:
                    guildarr = []
                    for guild in self.guilds:

                        temp = _guild_but(guild)
                        temp.button = gr.Button(guild.name)
                        guildarr.append(temp)

                        #guilds are a pain, figure out how to implement later

            
            btn.click(self.restart)

            d.load(self.retrieve_terminal,None,terminal,every=1)
            


        
        return d
    
    


    def launch(self):
        self.demo.queue().launch()
    


x = create_webui()
x.launch()
