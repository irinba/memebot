import telebot
import os
import ydb
import ydb.iam
import bot_handlers
from telebot.types import Message, CallbackQuery

# Инициализация бота Telegram.
# Получаем токен бота из переменных окружения и создаем экземпляр бота.
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))


# Подключение к базе данных Yandex Database (YDB).
# Создаем драйвер для подключения, используя данные из переменных окружения.
driver = ydb.Driver(
  endpoint=os.getenv('YDB_ENDPOINT'),
  database=os.getenv('YDB_DATABASE'),
  credentials=ydb.iam.MetadataUrlCredentials(),
)

# Ожидаем готовности драйвера к работе в течение 5 секунд.
driver.wait(fail_fast=True, timeout=5)

# Создаем пул сессий для управления сессиями базы данных.
pool = ydb.SessionPool(driver)


@bot.message_handler(commands=['start'])
def send_welcome(message: Message) -> None:
    """
    Обрабатывает команду /start, отправленную пользователем боту.

    :param message: Объект Message, содержащий информацию о полученном сообщении.
    """
    bot_handlers.send_welcome(bot, message)


@bot.message_handler(func=lambda message: True)
def handle_text(message: Message) -> None:
    """
    Обрабатывает текстовые сообщения, отправленные пользователем боту.

    :param message: Объект Message, содержащий информацию о полученном сообщении.
    """
    bot_handlers.handle_text(bot, message, pool)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call: CallbackQuery) -> None:
    """
    Обрабатывает нажатия на inline-кнопки пользователем.

    :param call: Объект CallbackQuery, содержащий информацию о нажатии на inline-кнопку.
    """
    bot_handlers.handle_query(call, pool)

