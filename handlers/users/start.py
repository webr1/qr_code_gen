import time
from pathlib import Path
import pyqrcode
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from loader import dp, bot
from keyboards.default.defold_keys import main_menu
from states.code_qr import QRStates, Textabout

# Константы для путей
QR_CODES_DIR = Path("E:/qr_code_gen/photoes")
QR_CODES_DIR.mkdir(parents=True, exist_ok=True)


@dp.message_handler(CommandStart())
async def bot_start(msg: types.Message):
    username = msg.from_user.username
    full_name = msg.from_user.full_name
    telegram_id = msg.from_user.id
    await msg.answer(
        f"Привет, [{msg.from_user.full_name}]! 👋 Я твой дружелюбный помощник-бот. Могу создать для тебя QR-код",
        reply_markup=main_menu
    )

    info = (
        f"User haqida informatsiya\n"
        f"User_name: @{username}\n"
        f"User_id: {telegram_id}\n"
        f"User_full_name: {full_name}\n"
    )

    for admin in ADMINS:
        await bot.send_message(admin, info)



@dp.message_handler(text="Создать QRcode💫⭐️")
async def qr_call_handler(msg: types.Message):
    await msg.answer(
        f"Привет, [{msg.from_user.username}]! 😄 Я рад тебя видеть! "
        "Готов создать для тебя QR-код. Просто отправь мне текст, "
        "который нужно закодировать, и я сделаю QR-код!⌨️💻💾"
    )
    await QRStates.waiting_for_text.set()


@dp.message_handler(state=QRStates.waiting_for_text)
async def qr_handler(msg: types.Message, state: FSMContext):
    try:
        # Создаем QR-код
        qr_code = pyqrcode.create(msg.text)

        # Генерируем уникальное имя файла
        timestamp = int(time.time())
        filename = f"{msg.chat.id}_{timestamp}_{msg.from_user.id}.png"
        filepath = QR_CODES_DIR / filename

        # Сохраняем QR-код
        qr_code.png(str(filepath), scale=6)

        # Проверяем, что файл создан
        if not filepath.exists():
            await msg.answer("❌ Ошибка при создании QR-кода")
            return

        # Отправляем пользователю
        with open(filepath, 'rb') as photo:
            await bot.send_photo(
                chat_id=msg.chat.id,
                photo=photo,
                caption=f"✨ <b>Ваш QR-код готов!</b> ✨\n\n"
                        f"🔹 <i>Сканируйте и переходите по ссылке</i> 🔹\n\n"
                        f"▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                        f"<code>Создано: @QRcode_webr1_bot</code>",
                parse_mode="HTML"
            )
    except Exception as e:
        await msg.answer(f"❌ Произошла ошибка: {str(e)}")
    finally:
        await state.finish()


@dp.message_handler(text='Отзыв⌨️📩')
async def comment_handler(message: types.Message):
    await message.answer(
        "📝 *Напишите ваш отзыв*\n\n"
        "Мы ценим ваше мнение! Оставьте несколько слов о работе бота.",
        parse_mode="Markdown"
    )
    await Textabout.text1.set()


@dp.message_handler(state=Textabout.text1)
async def com_handler(message: types.Message, state: FSMContext):
    try:
        text1 = message.text
        await state.update_data({"text1": text1})
        data = await state.get_data()
        comments = data.get("text1")

        info = (
            f"Here is information about comment\n"
            f"Text - {comments}\n"
            f"Info from nameuser {message.from_user.username}\n"
            f"id {message.from_user.id}\n"
            f"fullname {message.from_user.full_name}\n"
        )

        for admin in ADMINS:
            await bot.send_message(admin, info)

        await message.answer("Ваш отзыв принят, спасибо✅")
    finally:
        await state.finish()







