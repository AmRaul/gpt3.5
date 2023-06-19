
import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import json


file = open('config.json', 'r')
config = json.load(file)

openai.api_key = (config['openai'])
bot = Bot(config['token_bot'])
dp = Dispatcher(bot)


class BaseModel:
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "My name is Raul. Are you ready help me?"},
        {"role": "assistant", "content": "Hello. Yes"}
    ]

    def clean_base_modal(self):
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "My name is Raul. Are you ready help me?"},
            {"role": "assistant", "content": "Hello. Yes"}
        ]


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton('Чат GPT', callback_data='chat_gpt'))
    markup.add(types.InlineKeyboardButton('Изображение GPT', callback_data='image_generation'))
    await message.answer('Что хотим?', reply_markup=markup)


@dp.callback_query_handler(text='chat_gpt')
async def chat_gpt(call):
    await call.message.answer('Чем я могу тебе помочь?')
# В будущем надо будет добавить сюда выбор кнопок назад к выбору режима



# ---------CHATGPT-------
# messages=[
#         {"role": "system", "content": "You are a helpful assistant"},
#         {"role": "user", "content": "My name is Raul. Are you ready help me?"},
#         {"role": "assistant", "content": "Hello. Yes"}
#     ]

def update(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

@dp.message_handler(commands=['again'])
async def clean_messages(message: types.Message):
    global BaseModel
    await message.answer('Начнем заново')
    BaseModel.messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "My name is Raul. Are you ready help me?"},
        {"role": "assistant", "content": "Hello. Yes"}
    ]


@dp.message_handler()
async def send(message: types.Message):
    global BaseModel
    if message['from'].id == 297936848:
        update(BaseModel.messages, "user", message.text)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=BaseModel.messages
        )
        await message.answer(response['choices'][0]['message']['content'])
    else:
        await message.answer(f'Sorry{message["from"].first_name}, это личный бот')


@dp.callback_query_handler(text='image_generation')
async def chat_gpt(call):
    await call.message.answer(call.data)


# --------IMAGE GENERATION ------

# response = openai.Image.create(
#     prompt='крупный план, студийный фотографический портрет белой сиамской кошки, которая выглядит любопытно, уши с подсветкой',
#     n=1,
#     size="1024x1024"
# )
# image_url = response['data'][0]['url']
# print(image_url)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
