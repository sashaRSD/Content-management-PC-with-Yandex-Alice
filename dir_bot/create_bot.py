from aiogram import Bot
from aiogram import Dispatcher
import configparser
import sys
import os


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = 'dir_bot'
    return os.path.join(base_path, relative_path)


config = configparser.ConfigParser()
config.read(resource_path('config.ini'))
token = config["DATA"]["token_bot_alice"]
id_channel = config["DATA"]["id_channel"]

bot = Bot(token=token)
dp = Dispatcher()
