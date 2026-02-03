import asyncio
import os
import pyautogui
import threading
from flask import Flask, request
from flask_cors import CORS
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# --- КОНФИГУРАЦИЯ ---
API_TOKEN = '8463083247:AAEAVSlHKZWjDhPklFR6nty4rCNAuUKDFYs'
ADMIN_ID = 6699202743
# Ссылка на твой сайт с index.html (например, на GitHub Pages)
WEB_APP_URL = "https://your-username.github.io/remote-touchpad/" 

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
pyautogui.FAILSAFE = False 

# --- FLASK SERVER ---
app = Flask(__name__)
CORS(app)

@app.route('/mouse', methods=['POST'])
def mouse_control():
    data = request.json
    action = data.get('action')
    
    if action == 'move':
        dx, dy = data.get('dx', 0), data.get('dy', 0)
        # Ускорение движения для отзывчивости
        pyautogui.moveRel(dx * 1.8, dy * 1.8)
    elif action == 'left_click':
        pyautogui.click()
    elif action == 'right_click':
        pyautogui.rightClick()
    elif action == 'double_click':
        pyautogui.doubleClick()
        
    return {"status": "success"}

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# --- BOT HANDLERS ---
def main_kb():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🖱 Тачпад', web_app=WebAppInfo(url=WEB_APP_URL))],
        [KeyboardButton(text='📸 Скриншот'), KeyboardButton(text='🔊 Громкость +')],
        [KeyboardButton(text='💤 Сон'), KeyboardButton(text='🔌 Выключить ПК')]
    ], resize_keyboard=True)

@dp.message(Command("start"))
async def start(msg: types.Message):
    if msg.from_user.id == ADMIN_ID:
        await msg.answer("🖥 ПК Дистанция запущена!", reply_markup=main_kb())

@dp.message(F.text == '📸 Скриншот')
async def screen(msg: types.Message):
    pyautogui.screenshot("s.png")
    await msg.answer_photo(types.FSInputFile("s.png"))
    os.remove("s.png")

# --- ЗАПУСК ---
async def main():
    threading.Thread(target=run_flask, daemon=True).start()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())