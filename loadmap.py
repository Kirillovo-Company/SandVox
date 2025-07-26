import subprocess
import sys
import os
from ursina import *

def load_map(map_folder):
    """Загружает карту и запускает игру в новом окне"""
    map_path = os.path.abspath(os.path.join("maps", map_folder))
    
    if not os.path.exists(map_path):
        print(f"Ошибка: папка карты '{map_folder}' не найдена!")
        return
    
    # Ищем game.py в папке карты
    if not os.path.exists(os.path.join(map_path, "game.py")):
        print(f"Ошибка: в карте '{map_folder}' нет game.py!")
        return
    
    # Закрываем текущее окно с меню (если есть)
    if 'app' in globals():
        app.quit()
    
    # Запускаем карту в новом окне
    if sys.platform == "win32":
        subprocess.Popen(
            [sys.executable, os.path.join(map_path, "game.py")],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    elif sys.platform == "linux":
        subprocess.Popen([
            "x-terminal-emulator", "-e", 
            sys.executable, os.path.join(map_path, "game.py")
        ])
    else:  # MacOS
        subprocess.Popen([
            "open", "-a", "Terminal", 
            os.path.join(map_path, "game.py")
        ])