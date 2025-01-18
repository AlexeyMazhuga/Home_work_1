import os
import requests
from dotenv import load_dotenv
import time

# Загрузка переменных из .env файла
load_dotenv()

# Получение API-ключа из .env
FSQ_API_KEY = os.getenv("FSQ_API_KEY")

# Проверка наличия ключа
if not FSQ_API_KEY:
    print("Ошибка: FSQ_API_KEY не найден в .env файле!")
    exit(1)

# Запрос категории у пользователя
category = input("Введите категорию для поиска (например, кофейни, музеи, парки): ")

# Параметры запроса к API Foursquare
url = "https://api.foursquare.com/v3/places/search"
params = {
    "query": category,
    "limit": 10,  # Количество результатов
    "fields": "name,location,rating"  # Запрашиваемые поля
}
headers = {
    "Accept": "application/json",
    "Authorization": FSQ_API_KEY  # Используем API-ключ
}

# Функция для выполнения запроса с повторными попытками
def make_request(url, params, headers, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()  # Проверка на ошибки HTTP
            return response
        except requests.exceptions.RequestException as e:
            print(f"Попытка {attempt + 1} не удалась: {e}")
            time.sleep(2)  # Пауза перед повторной попыткой
    print("Превышено количество попыток. Проверьте соединение или повторите позже.")
    exit(1)

# Выполнение запроса
response = make_request(url, params, headers)

# Парсинг JSON
try:
    data = response.json()
    results = data.get("results", [])

    if not results:
        print("По вашему запросу ничего не найдено.")
    else:
        print(f"Найдено заведений: {len(results)}\n")
        for place in results:
            name = place.get("name", "Название не указано")
            address = place.get("location", {}).get("formatted_address", "Адрес не указан")
            rating = place.get("rating", "Рейтинг не указан")
            print(f"Название: {name}")
            print(f"Адрес: {address}")
            print(f"Рейтинг: {rating}")
            print("-" * 40)
except ValueError as e:
    print(f"Ошибка при парсинге JSON: {e}")
