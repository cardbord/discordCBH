import gradio as gr, pathlib
path = pathlib.Path(__file__).parent
blocks = gr.Blocks(css=str(path)+"/app.css")

class create_webui:

    def restart(self):
        print("This is a test")

    def retrieve_terminal(self):
        return "test"

    @property
    def demo(self):

        with blocks as d:
            with gr.Tab("Bot Management"):
                with gr.Row():
                    btn = gr.Button("Restart bot",elem_id="restart",elem_classes="restart")
            with gr.Tab("Terminal"):
                terminal = gr.TextArea(label="Terminal",value="discordCBH output terminal",elem_id="terminal-background",elem_classes="terminal")    
            
            
            btn.click(self.restart)

            d.load(self.retrieve_terminal,None,terminal,every=1)

        
        return d
    
    


    def launch(self):
        self.demo.queue().launch()
    


x = create_webui()
x.launch()
