import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command, StateFilter, Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher.filters.state import State, StatesGroup

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token="6056253732:AAGWlJCRZ_kb63dyj3eKuVIOebZ-uLP9A6M")

# Диспетчер
dp = Dispatcher(bot, storage=MemoryStorage())

class Number(StatesGroup):
    start = State()
    number = State()

# Хэндлер на команду /start
@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(Number.start)
    await Number.start.set()
    await bot.send_message(message.chat.id, f"Привет, чтобы начать игру напиши цифру от 1 до 10")

@dp.message_handler(state=Number.start, content_types=['text'])
async def get_number(message: types.Message, state: FSMContext):
    if message.from_user.id != bot.id:
        try:
            number = int(message.text)
            await state.update_data({'number': message.text})
            data = await state.get_data()
            #random_int = random.randint(1, 10)     
            random_int = 7
            if random_int == number:
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text="Попробовать снова", callback_data="try_again"))
                await bot.send_message(message.chat.id, f"Поздравляю, вы выйграли!!!\nВы выбрали:  {data['number']}\nБот задал: {random_int}", reply_markup=keyboard)
                await state.finish()
            else:
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text="Попробовать снова", callback_data="try_again"))
                await bot.send_message(message.chat.id, f"К сожалению вы проиграли\nВы выбрали:  {data['number']}\nБот задал: {random_int}", reply_markup=keyboard)
                await state.finish()
        except ValueError:
            await bot.send_message(message.chat.id, "Пожалуйста, введите число!")

@dp.callback_query_handler(text="try_again")
async def try_again(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Игра началась! Введите число от 1 до 10.")
    await call.answer()
    await state.set_state(Number.start)  # Устанавливаем состояние в Number.start
    await call.message.answer("Игра началась! Введите число от 1 до 10.")

# Запуск процесса поллинга новых апдейтов

async def setup_bot_commands():
    bot_commands = [
        types.BotCommand(command="/start", description="Запуск бота"),
        types.BotCommand(command="/help", description="Помощь"),
        types.BotCommand(command="/stats", description="Статистика пользователей")
    ]
    await bot.set_my_commands(bot_commands)

async def main():
    await setup_bot_commands()
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
