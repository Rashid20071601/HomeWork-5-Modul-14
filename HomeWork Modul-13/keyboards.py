# Import
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



start_kb = ReplyKeyboardMarkup(
  keyboard=[
    [KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация')],
    [KeyboardButton(text='Купить'), KeyboardButton(text='Регистрация')]
  ],
  resize_keyboard=True
)


сalculate_calorie = InlineKeyboardMarkup(
  inline_keyboard=[
    [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
    [InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
  ]
)


catalog = InlineKeyboardMarkup(
  inline_keyboard=[
    [
      InlineKeyboardButton(text='Продукт 1', callback_data='product_buying'),
      InlineKeyboardButton(text='Продукт 2', callback_data='product_buying'),
      InlineKeyboardButton(text='Продукт 3', callback_data='product_buying'),
      InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
    ]
  ]
)