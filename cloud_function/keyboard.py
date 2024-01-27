from telebot import types


def reaction_keyboard():
    """
    Создаёт и возвращает объект клавиатуры с inline-кнопками для Telegram бота.

    Клавиатура содержит две кнопки: "👍" (like) и "👎" (dislike), которые пользователь
    может использовать для выражения своего отношения к сообщению бота.

    :return: Объект InlineKeyboardMarkup, содержащий две inline-кнопки.
    """
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    like_button = types.InlineKeyboardButton(text="👍", callback_data="like")
    dislike_button = types.InlineKeyboardButton(text="👎", callback_data="dislike")
    keyboard.add(like_button, dislike_button)
    return keyboard
