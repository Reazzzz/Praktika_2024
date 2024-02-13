# Импорт необходимых библиотек
import telebot
import requests
from bs4 import BeautifulSoup

#токен для бота
TOKEN = '6388606159:AAHbK4YUb-PX8u4fufQs9so8TQLcJ3FRVX8'
bot = telebot.TeleBot(TOKEN)


# Обработчик команд /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для поиска картинок на Яндекс. Пожалуйста, отправь мне свой запрос.")


# Обработчик всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def search_images(message):
    # Получение запроса пользователя
    query = message.text
    # Получение ссылок на изображения
    images = get_images(query, 10)

    # Отправка пользователю 10 ссылок на изображения
    for image_url in images:
        bot.send_message(message.chat.id, image_url)


# Функция для получения ссылок на изображения с Яндекс.Картинок
def get_images(query, count):
    # Формирование URL-запроса к Яндекс.Картинкам
    url = f'https://yandex.ru/images/search?text={query}&format=json'
    # Установка заголовков для имитации браузера
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Отправка GET-запроса к Яндекс.Картинкам и получение HTML-страницы
    response = requests.get(url, headers=headers)
    # Создание объекта BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Список для хранения ссылок на изображения
    image_links = []

    # Итерация по всем тегам <a> с классом 'serp-item__link'
    for a_tag in soup.find_all('a', {'class': 'serp-item__link'}):
        # Добавление ссылки в список
        image_links.append(a_tag['href'])
        # Прекращение итерации, если достигнуто нужное количество ссылок
        if len(image_links) == count:
            break

    # Возвращение списка ссылок на изображения
    return image_links


# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
