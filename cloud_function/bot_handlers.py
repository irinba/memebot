from keyboard import reaction_keyboard
from utils import get_model_response, get_img_link
from insert_to_ydb import insert_data_to_ydb
from queries import reactions_query, user_request_query

from telebot import TeleBot
from telebot.types import Message, CallbackQuery
from ydb import SessionPool

def send_welcome(bot: TeleBot, message: Message) -> None:
    """
    Отправляет приветственное сообщение пользователю при начале взаимодействия с ботом.

    :param bot: Экземпляр бота.
    :param message: Объект Message, содержащий информацию о полученном сообщении.
    """
    bot.reply_to(message, "Привет. Пришли любой текст, а я подберу тебе наиболее подходящие мемы из моей базы.")


def handle_text(bot: TeleBot, message: Message, pool: SessionPool) -> None:
    """
    Обрабатывает текстовые сообщения, отправленные пользователем боту.
    Делает запрос к Docker-контейнеру, в котором находится языковая модель и происходит процесс поиска подходящего мема.
    Отправляет результат пользователю в виде 5 мемов с их текстовым описанием и картинками.
    Вносит информацию о текстовом запросе пользователя и подобранных мемах в базу данных.

    :param bot: Экземпляр бота.
    :param message: Объект Message, содержащий информацию о полученном сообщении.
    :param pool: Пул сессий для работы с базой данных.
    """
    try:
        # Получение текстового запроса пользователя и отправка json-запроса в контейнерное приложение с моделью.
        user_request = message.text
        json_payload = {"message": user_request}
        response = get_model_response(json_payload)

        # Распаковка json-ответа.
        # Он содержит ссылки на страницы подходящих мемов, id мемов из датасета и текстовые описания мемов.
        # Получение ссылок на картинки каждого из найденных мемов.
        if response and 'final_message' in response:
            final_message = response['final_message']
            img_links = get_img_link(final_message['query_links'])

            # Отправка сообщений с результатом поиска пользователю.
            bot.send_message(message.chat.id,
                             "Вот 5 мемов, которые мне удалось подобрать. Пожалуйста, поставь им оценку, это "
                             "поможет мне стать лучше. Введи новый запрос, если хочешь получить новую подборку.")

            # Цикл отправки 5 сообщений с результатом.
            # Сохранение id отправленного сообщения, запроса пользователя и id найденного мема в базу данных.
            for i in range(5):
                text = final_message['query_text'][i]
                link = img_links[i]
                meme_id = int(final_message['query_ids'][i])
                sent_message = bot.send_photo(message.chat.id, photo=link, caption=text,
                                              reply_markup=reaction_keyboard())
                message_id = int(sent_message.message_id)

                # Загрузка в базу данных YDB.
                pool.retry_operation_sync(lambda session: insert_data_to_ydb(session,
                                                                             user_request_query,
                                                                             message_id=message_id,
                                                                             user_request=user_request,
                                                                             meme_id=meme_id))
        else:
            bot.send_message(message.chat.id, "Произошла ошибка при обработке вашего запроса.")
    except Exception as e:
        print(f"Ошибка обработки сообщения: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка при обработке вашего запроса.")


def handle_query(call: CallbackQuery, pool: SessionPool) -> None:
    """
    Обрабатывает нажатия на inline-кнопки, отправленные пользователем в ответ на мемы.
    Загружает результат в базу данных.

    :param call: Объект CallbackQuery, содержащий информацию о нажатии на inline-кнопку.
    :param pool: Пул сессий для работы с базой данных.
    """
    if call.data in ["like", "dislike"]:
        message_id = int(call.message.message_id) # получаем id сообщения, на которое отреагировал пользователь
        user_reaction = call.data # получаем реакцию пользователя
        # загрузка в базу данных YDB
        pool.retry_operation_sync(lambda session: insert_data_to_ydb(session,
                                                                     reactions_query,
                                                                     message_id=message_id,
                                                                     user_reaction=user_reaction))
