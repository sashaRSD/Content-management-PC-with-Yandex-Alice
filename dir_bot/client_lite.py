from aiogram import types
from dir_bot import create_bot
import pyautogui as pg
import os, subprocess


id_channel = -1001853951630
dp = create_bot.dp
bot = create_bot.bot


@dp.channel_post_handler(lambda message: message.chat.id == id_channel)
async def commands(message: types.Message):
    if message.text == "Play_Stop":
        pg.press("playpause")
        await bot.edit_message_text(chat_id=id_channel, message_id=message.message_id,
                                    text=f"{'-' * 5} PLAY/STOP command {'-' * 5}")

    elif message.text == "Continue":
        pg.press("left", presses=2)
        pg.press("playpause")
        await bot.edit_message_text(chat_id=id_channel, message_id=message.message_id,
                                    text=f"{'-' * 5} Continue command {'-' * 5}")

    elif message.text == "Cancel":
        pg.press("left", presses=4)
        await bot.edit_message_text(chat_id=id_channel, message_id=message.message_id,
                                    text=f"{'-' * 5} Cancel command {'-' * 5}")

    elif message.text == "Forward":
        pg.press("right", presses=4)
        await bot.edit_message_text(chat_id=id_channel, message_id=message.message_id,
                                    text=f"{'-' * 5} Forward command {'-' * 5}")

    elif message.text == "Game":
        pg.hotkey('ctrl', 'alt', 'shift', '1')
        await bot.edit_message_text(chat_id=id_channel, message_id=message.message_id,
                                    text=f"{'-' * 5} Game command {'-' * 5}")

    elif message.text == "Calculator":
        subprocess.call(["calc.exe"])
        await bot.edit_message_text(chat_id=id_channel, message_id=message.message_id,
                                    text=f"{'-' * 5} Calculator command {'-' * 5}")

    elif message.text == "Pictures":
        os.startfile(r"C:\Users\kaa99\Pictures\Camera Roll\WIN_20200102_13_02_48_Pro.jpg")
        await bot.edit_message_text(chat_id=id_channel, message_id=message.message_id,
                                    text=f"{'-' * 5} Pictures command {'-' * 5}")

    elif message.text == "Sleep":
        await bot.edit_message_text(chat_id=id_channel, message_id=message.message_id,
                                    text=f"{'-' * 5} Sleep command {'-' * 5}")
        os.system('rundll32 powrprof.dll,SetSuspendState 0,1,0')

    elif message.text == "Power":
        await bot.edit_message_text(chat_id=id_channel, message_id=message.message_id,
                                    text=f"{'-' * 5} Power command {'-' * 5}")
        os.system('shutdown /s')

    else:
        await bot.send_message(id_channel, f"{'-' * 5} О_о Не понимаю {'-' * 5}\n\n"
                                           f"Play_Stop - пауза\n"
                                           f"Continue - продолжить\n"
                                           f"Cancel - назад\n"
                                           f"Forward - вперед\n"
                                           f"Game - игра\n"
                                           f"Calculator - калькулятор\n"
                                           f"Pictures - картинка\n"
                                           f"Sleep - спать\n"
                                           f"Power - выключение")