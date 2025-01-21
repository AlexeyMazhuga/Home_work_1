import requests
import re
from bs4 import BeautifulSoup
import json

# URL веб-сайта для парсинга
url = 'http://books.toscrape.com/'

# Отправляем GET-запрос на сайт
response = requests.get(url)
print("Запрос отправлен")

if response.status_code != 200:
    print(f"Ошибка при загрузке страницы: {response.status_code}")
    exit()

print("Страница загружена")

# Парсим HTML-содержимое страницы
soup = BeautifulSoup(response.content, 'html.parser')
print("Парсинг HTML завершен")

# Находим все элементы книги
books = soup.find_all('article', class_='product_pod')
print(f"Найдено {len(books)} книг")

# Список для хранения данных о книгах
books_data = []

# Итерируемся по каждой книге и извлекаем нужную информацию
for book in books:
    # Извлекаем название книги
    title = book.h3.a['title']
    
    # Извлекаем цену книги
    price_text = book.find('p', class_='price_color').text
    price = float(price_text.replace('£', ''))
    
    # Извлекаем количество товара в наличии
    availability_text = book.find('p', class_='instock availability').text.strip()
    match = re.search(r'(\d+)', availability_text)
    if match:
        availability = int(match.group(1))
    else:
        availability = 0
    
    # Извлекаем описание книги (здесь описание отсутствует)
    description = ""
    
    # Создаем словарь с данными о книге
    book_info = {
        "title": title,
        "price": price,
        "availability": availability,
        "description": description
    }
    
    # Добавляем словарь в список
    books_data.append(book_info)

# Сохраняем данные в JSON-файл
with open('books_data.json', 'w', encoding='utf-8') as f:
    json.dump(books_data, f, ensure_ascii=False, indent=4)

print("Парсинг завершен и данные сохранены в books_data.json")