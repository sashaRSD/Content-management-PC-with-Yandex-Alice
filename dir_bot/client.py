from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types, F
from dir_bot import create_bot
import speech_recognition, time, asyncio
import pyautogui as pg
import ffmpeg, os
import logging


logging.basicConfig(filename='logfile.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')
os.environ["PATH"] = r'dir_bot\voice' + os.pathsep + os.environ["PATH"]
id_channel = int(create_bot.id_channel)
dp = create_bot.dp
bot = create_bot.bot
sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5


@dp.channel_post(lambda message:  message.chat.id == id_channel, F.voice)
async def voice(message: types.voice):
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_dir = os.path.abspath(f"dir_bot/{file.file_path.replace('oga', 'ogg')}")
    new_file_dir = file_dir.replace('ogg', 'wav')
    await bot.download_file(file.file_path, file_dir)

    ffmpeg.input(file_dir).output(new_file_dir).run()
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
    logging.debug(voice_text)
    await bot.delete_message(chat_id=id_channel, message_id=message.message_id)
    await work_of_functions(voice_text)


@dp.channel_post(lambda message:  message.chat.id == id_channel)
async def commands(message: types.Message):
    text = message.text
    await bot.delete_message(chat_id=id_channel, message_id=message.message_id)
    await work_of_functions(text)


@dp.callback_query()
async def commands_callback(callback: types.CallbackQuery):
    command = callback.data
    await callback.answer()
    await work_of_functions(command)


async def work_of_functions(text):
    text = text.lower()
    if text in ("play_stop", "пауза", "стоп"):
        print("play_stop")
        pg.press("playpause")
        logging.info('play_stop')

    elif text in ("continue", "продолжить"):
        print("continue")
        pg.press("left", presses=2)
        pg.press("playpause")
        logging.info('continue')

    elif text in ("cancel", "назад"):
        print("cancel")
        pg.press("left", presses=4)
        logging.info('cancel')

    elif text in ("forward", "вперед"):
        print("forward")
        pg.press("right", presses=4)
        logging.info('forward')

    elif text == "информация" or text == "инструкция":
        print("Информация")
        post_button = InlineKeyboardBuilder()
        post_button.add(InlineKeyboardButton(text="Пауза", callback_data="play_stop"))
        post_button.add(InlineKeyboardButton(text="Продолжить", callback_data="continue"))
        post_button.row(InlineKeyboardButton(text="Вперед", callback_data="forward"))
        post_button.add(InlineKeyboardButton(text="Назад", callback_data="cancel"))
        await bot.send_message(id_channel, f"Play_Stop - Пауза - Стоп\n"
                                           f"Continue - Продолжить\n"
                                           f"Cancel - Назад\n"
                                           f"Forward - Вперед\n", reply_markup=post_button.as_markup())
        logging.info('Информация')

    else:
        print("Error")
        smile = await bot.send_message(id_channel, '🗿')
        await asyncio.sleep(5)
        await bot.delete_message(chat_id=id_channel, message_id=smile.message_id)
        logging.info('Error')
