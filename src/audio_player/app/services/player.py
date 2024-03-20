from pathlib import Path

import pygame as pg


def get_file_path(file_name: str):
    return Path("file_storage") / file_name


def play_file(file_path: Path):
    print(f"Playing {file_path}")
    pg.mixer.init()
    pg.mixer.music.load(str(file_path))
    pg.mixer.music.play()
