# config.py — настройки аккаунтов для парсинга и активации чеков

# Настройки API для парсера (первый аккаунт)
api_id_parser =   # API ID для парсера от my.telegram.org
api_hash_parser = ''  # API Hash для парсера

# Настройки API для активатора (второй аккаунт)
api_id_activator =   # API ID для активатора от my.telegram.org
api_hash_activator = ''  # API Hash для активатора

# Канал с логами об активации чеков
channel = ''  # Канал для логов (без @). Укажите существующий канал

# Автовывод средств через чек
avto_vivod = True  # Если True — чек будет отправляться на указанный аккаунт раз в сутки
avto_vivod_tag = ''  # Telegram username без @, куда будет идти перевод

# Автоматическая отписка от неактивных каналов
avto_otpiska = False  # Если True — скрипт будет отписываться от каналов без чеков за сутки

# Поддержка капчи (если CryptoBot требует её)
anti_captcha = True  # Если True — скрипт будет использовать OCR для обхода капчи

# API ключ OCR сервиса (например, https://ocr.space/ или cap.guru)
ocr_api_key = ''  # Ваш ключ API для распознавания капчи
