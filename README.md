# мемебот

"мемебот" - это serverless телеграм-бот для семантического поиска мемов на русском языке. Доступен по ссылке: [https://t.me/find_text_meme_bot](https://t.me/find_text_meme_bot).

## Как это работает

Пользователи отправляют короткие текстовые запросы с описанием какой-либо жизненной ситуации. Запросы обрабатываются языковой моделью, после чего происходит поиск по базе мемов. Пользователь получает пять наиболее релевантных мемов с изображениями. Также предусмотрена возможность оценки результатов.

<details>
<summary>Пример работы бота </summary>
<br>
<img src="screenshots/img1-3.png" alt="Пример работы бота">
</details>

<details>
<summary>Пример работы бота </summary>
<br>
<img src="screenshots/img2-2.png" alt="Пример работы бота">
</details>

<details>
<summary>Пример работы бота </summary>
<br>
<img src="screenshots/img3-2.png" alt="Пример работы бота">
</details>

<details>
<summary>Пример работы бота </summary>
<br>
<img src="screenshots/img4-2.png" alt="Пример работы бота">
</details>

<details>
<summary>Пример работы бота </summary>
<br>
<img src="screenshots/img5-2.png" alt="Пример работы бота">
</details>

## Инфраструктура

- **Размещение**: Yandex Cloud
- **Реализация**: 
  - Бот работает через Yandex Cloud Function
  - Языковая модель и процесс поиска находятся в serverless контейнере
  - Оценки сохраняются в Yandex DataBase

## Содержание репозитория

1. **Jupiter Notebook**: Описание процесса fine-tuning модели и поискового алгоритма faiss
2. **Код облачной функции**
3. **Код Docker-контейнера** Содержит модель и реализацию процесса поиска.

## Используемые языки и фреймворки

- Языки: Python, SQL
- Фреймворки и платформы: Flask, Docker

## Используемые библиотеки и технологии

- Telebot (pyTelegramBotAPI), Pandas, Numpy, HuggingFace, Sentence Transformers, Faiss, Torch, Selenium, BeautifulSoup

## Данные

- Источник: Данные о мемах были собраны с сайта [memepedia.ru](https://memepedia.ru)
- Метод сбора: Selenium и BeautifulSoup
- Размер датасета: Около 2000 мемов
- Дополнение: Также был использован ChatGPT для генерации примеров пользовательских запросов для fine-tuning модели

## Используемая модель

Модель [intfloat/multilingual-e5-small](https://huggingface.co/intfloat/multilingual-e5-small) была дообучена с использованием MultipleNegativesRankingLoss. Модель базируется на XLM-RoBERTa и представляет из себя bidirectional encoder, что делает ее подходящей для извлечения эмбеддингов предложений на русском языке.

## Как работает поиск

Модель превращает текстовый запрос в эмбеддинг предложения и сравнивает его с эмбеддингами описаний мемов с помощью библиотеки faiss.
Сравнение происходит с помощью оценки косинусного расстояния между эмбеддингами.

