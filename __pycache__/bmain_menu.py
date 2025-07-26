from ursina import *

menuelements = []
def mainmenu():
    def mapselect_pressed():
        print('заглушка')
        title_text.visible = False
        mapselect.visible = False    
    title_text = Text(
        text='SandVox Alphasss',
        scale=3,
        y=0.3,
        x=0.0,
        origin=(0,0),
        color=color.black
    )
    mapselect = Button(
        text='Выбрать карту',
        color=color.black,
        scale=(0.4, 0.1),
        x=-0.7,
        y=0
    )
    mapselect.on_click = mapselect_pressed