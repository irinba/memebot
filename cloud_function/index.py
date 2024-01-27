import telebot
from main import bot
from typing import Dict, Any


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Обрабатывает входящие HTTP-запросы от Telegram и передает их боту для дальнейшей обработки.

    Эта функция предназначена для использования в облачной функции, которая обрабатывает вебхуки от Telegram.

    :param event: Словарь, содержащий информацию о входящем запросе.
    :param context: Информация о контексте выполнения облачной функции (не используется в данной функции).
    :return: Словарь с кодом состояния HTTP и телом ответа.
    """
    try:
        if 'body' in event and event['body'] is not None:
            message = telebot.types.Update.de_json(event['body'])
            bot.process_new_updates([message])
        else:
            print("Пустое тело запроса")
    except Exception as e:
        print("Ошибка при обработке запроса:", e)

    return {
        'statusCode': 200,
        'body': '!',
    }
