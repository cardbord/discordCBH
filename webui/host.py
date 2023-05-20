import gradio as gr


def placeholder(x):
    #this will be our link to grad with the bot's code
    
    return x

demo = gr.Interface(placeholder,inputs="text",outputs="text")
demo.launch()