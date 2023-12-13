from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from dir_bot import create_bot
import pyautogui as pg
import os, subprocess
import speech_recognition, time


id_channel = -1001853951630
dp = create_bot.dp
bot = create_bot.bot
sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5


@dp.channel_post_handler(lambda message: message.chat.id == id_channel)
async def commands(message: types.Message):
    text = message.text.lower()
    if text in ("play_stop", "пауза", "стоп"):
        pg.press("playpause")
        await bot.edit_message_text(chat_id=id_channel, message_id=message.message_id,
                                    text=f"{'-' * 6} PLAY/STOP {'-' * 7}")

    elif text in ("continue", "продолжить"):
        pg.press("left", presses=2)
        pg.press("playpause")
        await bot.edit_message_text(chat_id=id_channel, message_id=message.message_id,
                                    text=f"{'-' * 6} CONTINUE {'-' * 9}")

    elif text in ("cancel", "назад"):
        pg.press("left", presses=4)
        await bot.edit_message_text(chat_id=id_channel, message_id=message.message_id,
                                    text=f"{'-' * 6} CANCEL {'-' * 13}")

    elif text in ("forward", "вперед"):
        pg.press("right", presses=4)
        await bot.edit_message_text(chat_id=id_channel, message_id=message.message_id,
                                    text=f"{'-' * 6} FORWARD {'-' * 9}")

    elif text in ("game", "игра"):
        pg.hotkey('ctrl', 'alt', 'shift', '1')
        await bot.edit_message_text(chat_id=id_channel, message_id=message.message_id,
                                    text=f"{'-' * 6} GAME {'-' * 16}")

    elif text in ("calculator", "калькулятор"):
        subprocess.call(["calc.exe"])
        await bot.edit_message_text(chat_id=id_channel, message_id=message.message_id,
                                    text=f"{'-' * 6} CALCULATOR {'-' * 4}")

    elif text in ("pictures", "картинка"):
        os.startfile(r"C:\Users\kaa99\Pictures\Camera Roll\WIN_20200102_13_02_48_Pro.jpg")
        await bot.edit_message_text(chat_id=id_channel, message_id=message.message_id,
                                    text=f"{'-' * 6} PICTURES {'-' * 10}")

    elif text in ("sleep", "спать"):
        await bot.edit_message_text(chat_id=id_channel, message_id=message.message_id,
                                    text=f"{'-' * 6} SLEEP {'-' * 16}")
        os.system('rundll32 powrprof.dll,SetSuspendState 0,1,0')

    elif text in ("power", "выключение"):
        await bot.edit_message_text(chat_id=id_channel, message_id=message.message_id,
                                    text=f"{'-' * 6} POWER {'-' * 14}")
        os.system('shutdown /s')

    else:
        post_button = InlineKeyboardMarkup()
        post_button.add(InlineKeyboardButton(text="Пауза", callback_data="Пауза"))
        post_button.insert(InlineKeyboardButton(text="Продолжить", callback_data="Продолжить"))
        post_button.add(InlineKeyboardButton(text="Вперед", callback_data="Вперед"))
        post_button.insert(InlineKeyboardButton(text="Назад", callback_data="Назад"))
        await bot.send_message(id_channel, f"{'-' * 5} О_о Не понимаю {'-' * 5}\n\n"
                                           f"Play_Stop - Пауза - Стоп\n"
                                           f"Continue - Продолжить\n"
                                           f"Cancel - Назад\n"
                                           f"Forward - Вперед\n"
                                           f"Game - Игра\n"
                                           f"Calculator - Калькулятор\n"
                                           f"Pictures - Картинка\n"
                                           f"Sleep - Спать\n"
                                           f"Power - Выключение", reply_markup=post_button)


@dp.callback_query_handler()
async def commands_stop_today(callback: types.CallbackQuery):
    command = callback['data']
    await callback.answer()
    if command == "Пауза":
        pg.press("playpause")
    elif command == "Продолжить":
        pg.press("left", presses=2)
        pg.press("playpause")
    elif command == "Назад":
        pg.press("left", presses=4)
    elif command == "Вперед":
        pg.press("right", presses=4)


@dp.channel_post_handler(lambda message: message.chat.id == id_channel, content_types=['voice'])
async def voice(message: types.Message):
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_dir = f"dir_bot/{file.file_path.replace('oga', 'ogg')}"
    new_file_dir = file_dir.replace('ogg', 'wav')
    await bot.download_file(file.file_path, file_dir)

    os.system(f'ffmpeg -i {file_dir} {new_file_dir}')
    os.remove(file_dir)
    try:
        with speech_recognition.AudioFile(new_file_dir) as source:
            audio = sr.record(source=source)
            sr.adjust_for_ambient_noise(source=source, duration=0.5)
            voice_text = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
    except speech_recognition.UnknownValueError:
        voice_text = "Хмм... Не понял что ты сказал :/"
    time.sleep(1)
    os.remove(new_file_dir)
    print(voice_text)

    if voice_text == "пауза":
        pg.press("playpause")
        await bot.send_message(id_channel, f"{'-' * 6} PLAY/STOP {'-' * 7}")

    elif voice_text == "продолжить":
        pg.press("left", presses=2)
        pg.press("playpause")
        await bot.send_message(id_channel, f"{'-' * 6} CONTINUE {'-' * 9}")

    elif voice_text in ("назад", "повтори"):
        pg.press("left", presses=4)
        await bot.send_message(id_channel, f"{'-' * 6} CANCEL {'-' * 13}")

    elif voice_text in ("вперёд", "реклама"):
        pg.press("right", presses=4)
        await bot.send_message(id_channel, f"{'-' * 6} FORWARD {'-' * 9}")

    elif voice_text == "включи игру":
        pg.hotkey('ctrl', 'alt', 'shift', '1')
        await bot.send_message(id_channel, f"{'-' * 6} GAME {'-' * 16}")

    elif voice_text == "включи калькулятор":
        subprocess.call(["calc.exe"])
        await bot.send_message(id_channel, f"{'-' * 6} CALCULATOR {'-' * 4}")

    elif voice_text == "открой фото":
        os.startfile(r"C:\Users\kaa99\Pictures\Camera Roll\WIN_20200102_13_02_48_Pro.jpg")
        await bot.send_message(id_channel, f"{'-' * 6} PICTURES {'-' * 10}")

    elif voice_text == "отправь ноутбук спать":
        await bot.send_message(id_channel, f"{'-' * 6} SLEEP {'-' * 16}")
        os.system('rundll32 powrprof.dll,SetSuspendState 0,1,0')

    elif voice_text == "выключи ноутбук из розетки":
        await bot.send_message(id_channel, f"{'-' * 6} POWER {'-' * 14}")
        os.system('shutdown /s')

    else:
        await bot.send_message(id_channel, f"{'-' * 5} О_о Не понимаю {'-' * 5}\n\n"
                                           f"Пауза - пауза\n"
                                           f"Продолжить - продолжить\n"
                                           f"Назад или Повтори - назад\n"
                                           f"Вперёд или Реклама - вперёд\n"
                                           f"Включи игру - игра\n"
                                           f"Включи калькулятор - калькулятор\n"
                                           f"Открой фото - фото\n"
                                           f"Отправь ноутбук спать - спать\n"
                                           f"Выключи ноутбук из розетки - выключение")
