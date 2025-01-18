import os
import json
import requests
from dotenv import load_dotenv

# Загрузка переменных из .env файла
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print("Файл .env не найден!")
    exit(1)

# Проверка наличия API-ключа
api_key = os.getenv("API_KEY")
if not api_key:
    print("Переменная API_KEY не найдена в .env файле!")
    exit(1)

# Параметры запроса
url = "https://api.giphy.com/v1/gifs/search"
params = {
    "api_key": api_key,
    "q": "programming",
    "limit": 7,
    "offset": 0,
    "rating": "pg-13",
    "lang": "ru",
    "bundle": "messaging_non_clips"
}

# Заголовки запроса
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "*/*"
}

# Выполнение запроса
try:
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()  # Проверка на ошибки HTTP
except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении запроса: {e}")
    exit(1)

# Парсинг JSON
try:
    j_data = response.json()
    if "data" not in j_data:
        print("Ключ 'data' отсутствует в ответе API!")
        exit(1)

    # Сохранение данных в файл
    with open("gifts.json", "w", encoding="utf-8") as f:
        json.dump(j_data, f, ensure_ascii=False, indent=4)  # Записываем данные в файл с форматированием

    # Вывод URL гифок
    for gif in j_data["data"]:
        if "images" in gif and "original" in gif["images"] and "url" in gif["images"]["original"]:
            print(gif["images"]["original"]["url"])
        else:
            print("Некорректная структура данных гифки!")
except ValueError as e:
    print(f"Ошибка при парсинге JSON: {e}")