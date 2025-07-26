from ursina import *
import os
import time
from typing import Sequence
from ursina.prefabs.ursfx import ursfx
from other.startgame import ifstartgame
from loadmap import load_map as load_map_script  # Импорт функции загрузки карты

menuelements = []
maps_elements = []
current_screen = "main_menu"  # main_menu или map_selection
maps_container = None
        
def mainmenu():
    global maps_container

    def mapselect_pressed():
        global current_screen
        current_screen = "map_selection"
        title_text.visible = False
        mapselect.visible = False
        show_map_selection()
    
    # Создаем элементы главного меню
    title_text = Text(
        text='SandVox Alpha',
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
    
    menuelements.extend([title_text, mapselect])
    
    # Создаем контейнер для списка карт (изначально скрыт)
    maps_container = Entity(parent=camera.ui, y=0.3, visible=False)
    create_maps_screen()

def create_maps_screen():
    # Заголовок экрана карт
    maps_title = Text("Доступные карты:", 
                    parent=camera.ui, 
                    y=0.4,
                    visible=False)
    
    # Кнопка "Назад"
    back_button = Button(text="Назад в меню",
                       parent=camera.ui,
                       y=-0.4,
                       scale=(0.3, 0.05),
                       color=color.orange,
                       visible=False)
    back_button.on_click = back_to_menu
    
    maps_elements.extend([maps_title, back_button])

def back_to_menu():
    global current_screen
    current_screen = "main_menu"
    
    # Скрываем элементы карт
    maps_container.visible = False
    for element in maps_elements:
        element.visible = False
    
    # Показываем главное меню
    for element in menuelements:
        element.visible = True

def show_map_selection():
    # Показываем элементы карт
    maps_container.visible = True
    for element in maps_elements:
        element.visible = True
    
    # Обновляем список карт
    refresh_maps_list()

def refresh_maps_list():
    # Очищаем предыдущий список
    for child in maps_container.children:
        destroy(child)
    
    # Проверяем существование папки maps
    if not os.path.exists('maps'):
        os.makedirs('maps')
    
    # Получаем список папок с картами
    map_folders = [f for f in os.listdir('maps') 
                  if os.path.isdir(os.path.join('maps', f))]
    
    # Создаем элементы для каждой карты
    for i, map_folder in enumerate(map_folders):
        # Проверяем наличие python файлов
        has_python = any(f.endswith('.py') 
                        for f in os.listdir(os.path.join('maps', map_folder)))
        
        # Название карты
        text_color = color.green if has_python else color.gray
        Text(text=map_folder, 
             parent=maps_container, 
             origin=(-0.5, 0.5), 
             y=-i * 0.05, 
             x=-0.2,
             color=text_color)
        
        # Кнопка загрузки
        btn = Button(text='Загрузить' if has_python else 'Нет кода',
                    parent=maps_container,
                    y=-i * 0.05,
                    x=0.2,
                    scale=(0.2, 0.04),
                    color=color.azure if has_python else color.gray,
                    enabled=has_python)
        btn.on_click = Func(load_map, map_folder)  # передаём только имя карты

def load_map(map_folder):
    try:
        from loadmap import load_map as load_map_script
        load_map_script(map_folder)  # Теперь это запустит игру в новом окне
    except Exception as e:
        print(f"Ошибка: {e}")

def update():
    # Автоматическое обновление списка карт каждые 2 секунды
    if current_screen == "map_selection":
        if not hasattr(update, 'last_update'):
            update.last_update = time.time()
        
        if time.time() - update.last_update > 2:  # 2 секунды
            refresh_maps_list()
            update.last_update = time.time()