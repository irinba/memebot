# SQL-запросы

# Запрос на вставку реакции пользователя в таблицу reactions
reactions_query = """
    DECLARE $message_id AS Int64;
    DECLARE $user_reaction AS Utf8;

    INSERT INTO reactions (message_id, user_reaction)
    VALUES ($message_id, $user_reaction);
    """

# Запрос на вставку информации о запросе пользователя и отправленном меме в таблицу sent_messages
user_request_query = """
    DECLARE $message_id AS Int64;
    DECLARE $user_request AS Utf8;
    DECLARE $meme_id AS Int64;

    INSERT INTO sent_messages (message_id, user_request, meme_id)
    VALUES ($message_id, $user_request, $meme_id);
    """
