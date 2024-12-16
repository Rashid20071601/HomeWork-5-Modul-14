# Импорт библиотек
from aiogram import Bot, Dispatcher, executor, types  # Основные модули для работы с Telegram Bot API
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
import logging
from config import *
from keyboards import *
from admin import *
from crud_functions import *
import texts


# Создание объектов бота и диспетчера
bot = Bot(token=API_TOKEN)  # Инициализация бота
dp = Dispatcher(bot, storage=MemoryStorage())  # Инициализация диспетчера с хранением состояний
logging.basicConfig(level=logging.INFO)



class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000


# Обработка сообщений
@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer(f'Привет {message.from_user.username}. {texts.start}', reply_markup=start_kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=сalculate_calorie)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer(texts.age)
    await UserState.age.set()
    await call.answer()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(texts.formula)
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    if message.text.isdigit():  # Проверяем, является ли введенный текст числом
        await state.update_data(age=int(message.text))
        await message.answer(texts.growth)
        await UserState.growth.set()
    else:
        await message.answer(texts.error)


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    if message.text.isdigit():  # Проверяем, является ли введенный текст числом
        await state.update_data(growth=int(message.text))
        await message.answer(texts.weight)
        await UserState.weight.set()
    else:
        await message.answer(texts.error)


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    if message.text.isdigit():  # Проверяем, является ли введенный текст числом
        await state.update_data(weight=int(message.text))
        data = await state.get_data()

        # Расчет калорийности
        result = round(10*int(data['weight']) + 6.25*int(data['growth']) - 5*int(data['age']) + 5, 2)
        await message.answer(f'Ваша норма калорий {result}')
        await state.finish()
    else:
        await message.answer(texts.error)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    products = get_all_products()

    if not products:
        message.answer('На данный момент список товаров пуст. Пожалуйста, загляните позже!')
        return

    for index, product in enumerate(products, start=1):
        try:
            title, description, price = product[1], product[2], product[3]
            with open(f'./img/{index}.jpg', 'rb') as img:
                await message.answer_photo(img, f'Название: {title} | Описание: {description} | Цена: {price}')
        except FileNotFoundError:
            # Если изображения нет, отправляем только текст
            await message.answer(f'Название: {title} | Описание: {description} | Цена: {price}')

    await message.answer(texts.selection, reply_markup=catalog)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer(texts.purchase)
    await call.answer()


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer(texts.name_info)
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await message.answer("Пользователь существует, введите другое имя")
        return
    
    await state.update_data(username=message.text)
    await message.answer("Введите свой email:")
    await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    try:
        await state.update_data(age=int(message.text))
        if int(message.text) < 0:
            await message.answer("Возраст должен быть положительным числом. Попробуйте снова.")
            return
    except ValueError:
        await message.answer("Пожалуйста, введите числовое значение возраста.")
        return

    data = await state.get_data()
    username = data.get('username')
    email = data.get('email')
    age = data.get('age')

    try:
        add_users(username, email, age)
        await message.answer('Регистрация прошла успешно!')
    except Exception as e:
        await message.answer(f'Ошибка регистрации: {e}')
    finally:
        await state.finish()



@dp.message_handler()
async def all_message(message):
    await message.answer(texts.help_start)



# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)  # Запуск long-polling для обработки сообщений
