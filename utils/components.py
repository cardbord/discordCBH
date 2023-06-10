import uuid,typing
from ..errors import IncorrectFormat
from enum import IntEnum
'''Text inputs deprecated in favour of dPY's version. Please read dPY's
documentation on how to implement them.



The MIT License (MIT)

Copyright (c) 2022-present cardboard box

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

An extension to the discord.py library, bringing some features that do not
exist, or may not be included in the library. 


File to easily create JSON for message components.


::Example with 2 buttons, discord.py command::

import discord
from discordcbh.utils.components import Button, actionrow

@client.command()
async def blurple_and_danger(ctx):
    buttons = [
        Button(style=1,label="blurple"),
        Button(style=4,label="danger")
        ]
    action_row=actionrow(*buttons)
   
    message = await ctx.send(components=[action_row])

    button_response = await client.wait_for('component')
    
    if button_response.custom_id == buttons[0].custom_id:
        await button_response.send("you clicked blurple!")
    if button_response.custom_id == buttons[1].custom_id:
        await button_response.send("you clicked danger!")
    
    buttons = [
        Button(style=1,label="blurple",disabled=True),
        Button(style=4,label="danger",disabled=True)
        ]
    action_row=actionrow(*buttons)


    await message.edit(content="Sorry, someone has done this command!",components=[action_row])


'''

class ButtonType(IntEnum):
    '''
    Represents a button style
    '''
    blue = 1
    standard = 1
    blurple = 1
    green = 3
    red = 4
    danger = 4
    URL = 5


class PartialEmoji:
    '''
    Represents an emoji
    '''
    def __init__(self,name,emoji_id,animated):
        self.name = name
        self.id = emoji_id
        self.animated = animated
           
    def __repr__(self):
        return {"name":f"{self.name}","id":f"{self.id}","animated":f"{str(self.animated).lower()}"}
    
class Button:

    r"""Represents a button component

    params:
    style(int) = the style of the button, can be found here https://discord.com/developers/docs/interactions/message-components#buttons, or use ButtonType 
    label(str) = label on the button
    emoji(PartialEmoji) = emoji to display on the button
    url(str) = (only required if style is 5), any URL 
    disabled(bool) = whether the button is disabled or not
    custom_id(str) = the ID of the button
    """


    def __init__(self,
                 style:typing.Union[ButtonType,int]=1,
                 label:str="Button",
                 emoji:PartialEmoji=None,
                 disabled:bool=False,
                 url:str=None,
                 custom_id:str=None):
        self.style = style
        self.label = label
        self.emoji = emoji
        self.disabled = disabled
        self.url = url
        self.custom_id = custom_id if custom_id else str(uuid.uuid4())

    @property
    def button_json(self) -> dict:

        data = {
        "type":2,
        "style":self.style,
        }
        if self.label != None:
            data["label"] = self.label
        if self.emoji != None:
            data["emoji"] = self.emoji     
        if self.style == 5:
            if self.url is None:
                raise IncorrectFormat("Button style is 5 without a URL specified.")
            else:
                data["url"] = self.url
        if self.disabled:
            data["disabled"] = self.disabled    
        else:
            data["custom_id"] = self.custom_id

        return data
    
    def __repr__(self):
        return self.button_json
    


def create_button(style:typing.Union[ButtonType,int]=1,
                  label:str="Button",
                  emoji:PartialEmoji=None,
                  custom_id:str=None,
                  url:str=None,
                  disabled:bool=False) -> Button:
    '''
    returns json for a button

    deprecated, please use ``Button`` instead.

    returns a button component

    params:
    style(int) = the style of the button, can be found here https://discord.com/developers/docs/interactions/message-components#buttons 
    label(str) = label on the button
    emoji(PartialEmoji) = emoji to display on the button
    url(str) = (only required if style is 5), any URL 
    disabled(bool) = whether the button is disabled or not
    custom_id(str) = the ID of the button

    '''
    
    data = {
        "type":2,
        "style":style,

    }
    if label != None:
        data["label"] = label
    if emoji != None:
        data["emoji"] = emoji
    if style == 5:
        if url is None:
            raise IncorrectFormat("Button style is 5 without a URL specified.")
        else:
            data["url"] = url
    if disabled:
        data["disabled"] = disabled
    else:
        data["custom_id"] = custom_id or str(uuid.uuid4())

    return data

class ActionRow:
    
    '''
    Represents an action row to send within a message

    params:
    components(tuple) = components to store in the action row
    '''
    
    
    def __init__(self,*components):
        self.components = components
    
    @property
    def row_json(self) -> dict:
        data = {'type':1}
        if isinstance(self.components[0],list):
            row = []
            for item in self.components:
                for comp in item:
                    row.append(comp)
            row=tuple(row)

            data['components'] = row
        data['components'] = self.components
        
    def __repr__(self):
        return self.row_json
    


def actionrow(*components) -> dict:

    '''
    deprecated, please use ``ActionRow`` instead.

    returns an actionrow to send within a message
    
    params:
    components = all components to store in the actionrow

    '''

    row = []
    for item in components:
        row.append(item)
    data = {'type':1}
    row = tuple(row)
    data['components'] = row


    return data
     
def menucomponent(label:str,value:str,description:str,emoji:PartialEmoji=None) -> dict:
    '''
    returns a selectmenu choice
    
    params:
    label(str) = label on the choice
    value(str) = the ID returned to the program once selected
    description(str) = the description of the option
    emoji(PartialEmoji) = an emoji displayed on the option

    '''

    return {
        "label":label,
        "value":value,
        "description":description,
        "emoji":emoji,
    }

def selectmenu(placeholder:str,min_values:int=1,max_values:int=10,disabled:bool=False,custom_id:str=None,*choices) -> dict:
    '''
    placeholder(str) = the placeholder on the selectmenu
    min_values(int) = the minimum options a user can select
    max_values(int) = the maximum options a user can select
    custom_id(str) = the custom ID for the menu
    choices = all choices to send within the selectmenu


    '''
    
    row = []
    for item in choices:
        row.append(item)
    
    data = {
        "type":3,
        "options":row,
        "placeholder": placeholder,
        "min_values": min_values,
        "max_values": max_values
    }
    data['custom_id'] = custom_id or str(uuid.uuid4)
    return data