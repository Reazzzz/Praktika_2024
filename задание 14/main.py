import requests #запросы на сайт с ии
import json #для конфигурации картинки
from telebot import TeleBot #для использования бота телеграмм
from translate import Translator #переводим запрос с русского на англ
from PIL import Image # преобразование ссылки в картинку
import io
# апи коючи + ссылка
API_AI = "A2pKGNP55EaqTxCynw69ZQnvHmGPhKhDj3mBrLcfoyXDjZZ2tqBsqecHGvF2"  # Ваш API-ключ для взаимодействия с ИИ
API_bot = "6388606159:AAHbK4YUb-PX8u4fufQs9so8TQLcJ3FRVX8"  # Ваш API-ключ для бота Telegram
url = "https://stablediffusionapi.com/api/v3/text2img"
bot = TeleBot(API_bot)

# ответ на команду /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     'Привет! Для того чтобы создать картинку воспользуйтесь командой /draw "Тут пишите запрос"')

# ответ на команду /draw
@bot.message_handler(commands=['draw'])
def draw(message):
    bot.send_message(message.chat.id, "Придется чуть-чуть подождать, я думаю...")
    #срез запроса
    mess_text = message.text[6:]
    print(mess_text)
    # перевод с ру на англ
    translator = Translator(to_lang="en")
    text_Eng = translator.translate(mess_text)
    print(text_Eng)
    # конфигурация фото
    payload = {
        "key": API_AI,
        "prompt": text_Eng,
        "width": "1024",
        "height": "1024",
        "samples": "1",
        "num_inference_steps": "20",
        "seed": "99999999",
        "guidance_scale": 7.5,
        "safety_checker": "yes",
        "multi_lingual": "no",
        "panorama": "no",
        "self_attention": "yes",
        "upscale": "no",
        "embeddings_model": None,
        "webhook": None,
        "track_id": None
    }

    headers = {
        'Content-Type': 'application/json'
    }
    # преобразование с string в json и вытягивание ссылки( по идее)
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    json_object = response.json()
    link = json_object["output"][0]
    #битовая последовательность ссылки и отправка пользователю
    response = requests.get(link)
    byte_io = io.BytesIO(response.content)
    image = Image.open(byte_io)
    image_byte_io = io.BytesIO()
    image.save(image_byte_io, format='PNG')
    image_byte_io.seek(0)
    bot.send_photo(message.chat.id, image_byte_io)


bot.polling()
