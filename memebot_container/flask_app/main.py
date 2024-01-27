import os
from flask import Flask, request, jsonify
from search_model.language_model import EmbeddingModel
from search.faiss_search import FaissSearch
from utils import load_data
from typing import Any

# Инициализация приложения Flask
app = Flask(__name__)
# Инициализация классов языковой модели и поиска Faiss
embedding_model = EmbeddingModel()
faiss_search = FaissSearch()
# Загрузка Pandas DataFrame с данными о мемах
all_data = load_data()


@app.route('/', methods=['POST'])
def process_request() -> Any:
    """
    Обрабатывает POST-запросы, получая текст сообщения и возвращая результаты поиска.

    :return: JSON-ответ с финальным сообщением, содержащим ссылки, тексты и идентификаторы найденных элементов.
             В случае ошибки возвращает сообщение об ошибке и соответствующий HTTP-статус код.
    """
    try:
        data = request.json
        user_response = str(data['message'])

        # Получаем эмбеддинг запроса пользователя и выполняем поиск faiss
        user_response = 'query: ' + user_response
        question_embedding = embedding_model.get_embedding(user_response)
        distances, indices = faiss_search.search(question_embedding)

        # Формируем ответ для передачи в облачную функцию
        final_message = {'query_links': [], 'query_text': [], 'query_ids': []}
        for i in indices[0]:
            final_message['query_links'].append(all_data['link'][i])
            final_message['query_text'].append(all_data['header'][i])
            final_message['query_ids'].append(str(i))

        return jsonify({'final_message': final_message})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400  # Возвращаем ошибку с кодом 400
    except Exception as e:
        return jsonify({'error': f"Внутренняя ошибка сервера: {e}"}), 500  # Внутренняя ошибка сервера


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ['PORT']) # Переменная port определяется автоматически и содержится в переменных окружения
