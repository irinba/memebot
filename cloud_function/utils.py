import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any

def get_img_link(all_links_list: List[str]) -> List[str]:
    """
    Получает список ссылок на веб-страницы и возвращает список ссылок на картинки, найденные на этих страницах.

    :param all_links_list: Список строк, каждая из которых является URL-адресом веб-страницы.
    :return: Список строк, каждая из которых является URL-адресом изображения.
    """
    img_links = []
    for i_link in all_links_list:
        html_page = requests.get(i_link)
        soup = BeautifulSoup(html_page.content, 'html.parser')
        img_link = soup.findAll('img')[4]['src'] # предполагается, что нужная картинка - пятая на странице
        img_links.append(img_link)
    return img_links


def get_model_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Отправляет запрос к языковой модели, размещенной в Docker-контейнере. Модель обрабатывает данные и возвращает результаты.
    Используется для получения подборки мемов, соответствующих запросу пользователя.

    :param data: Словарь с данными для отправки в запросе. Эти данные используются моделью для генерации ответа.
    :return: Словарь с ответом от сервера. Возвращает пустой словарь в случае ошибки.
    """
    try:
        response = requests.post('https://bbagnh2nvd3ubbuo83b2.containers.yandexcloud.net', json=data)
        response.raise_for_status()  # Добавляем проверку статуса ответа
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP ошибка: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
    except Exception as e:
        print(f"Общая ошибка: {e}")
    return {}