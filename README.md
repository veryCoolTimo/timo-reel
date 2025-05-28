# TimoReel

TimoReel — это Telegram-бот и встроенное WebApp-приложение, которое автоматически скачивает видео по ссылкам из Instagram и TikTok, присылаемые в любой чат, и собирает их в «ленту» наподобие TikTok/Instagram.

## Особенности

- 🤖 Автоматическое скачивание видео из Instagram и TikTok
- 📱 WebApp интерфейс в стиле TikTok с темной темой
- ❤️ Система лайков и комментариев
- 🔇 Возможность отключения уведомлений
- 📊 История реакций пользователя
- 💾 Локальное хранение метаданных в JSON
- 🌐 REST API для WebApp

## Структура проекта

```
timo-reel/
├── backend/                    # Python Telegram Bot + API
│   ├── bot.py                 # Точка входа бота
│   ├── api_server.py          # API сервер для WebApp
│   ├── test_bot.py            # Тестовый скрипт модулей
│   ├── test_api.py            # Тестовый скрипт API
│   ├── handlers/              # Обработчики сообщений
│   │   ├── link_handler.py    # Парсинг ссылок и загрузка
│   │   ├── webapp_handler.py  # API endpoints для WebApp
│   │   └── pm_commands.py     # Команды в личных сообщениях
│   ├── downloader/            # Загрузка видео (yt-dlp)
│   │   └── video_downloader.py
│   ├── storage/               # JSON хранилище
│   │   └── metadata.json      # Метаданные видео и реакций
│   ├── utils/                 # Конфигурация и кеш
│   │   ├── config.py          # Настройки
│   │   └── cache.py           # Работа с JSON
│   └── requirements.txt       # Python зависимости
├── webapp/                    # React WebApp
│   ├── src/                   # Исходный код
│   ├── dist/                  # Собранное приложение
│   └── package.json           # Node.js зависимости
└── docs/                      # Документация
```

## Установка и запуск

### Шаг 1: Подготовка окружения

#### Backend (Python)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend (Node.js)
```bash
cd webapp
npm install
```

### Шаг 2: Настройка

1. Скопируйте `backend/env_example.txt` в `backend/.env`
2. Получите токен бота у [@BotFather](https://t.me/BotFather)
3. Заполните файл `.env`:

```env
BOT_TOKEN=your_bot_token_here
HOST=0.0.0.0
PORT=8000
```

### Шаг 3: Тестирование

Проверьте работу всех модулей:
```bash
cd backend
source venv/bin/activate
python test_bot.py
```

### Шаг 4: Запуск системы

#### Запуск бота:
```bash
cd backend
source venv/bin/activate
python bot.py
```

#### Запуск API сервера (в отдельном терминале):
```bash
cd backend
source venv/bin/activate
python api_server.py
```

#### Тестирование API:
```bash
cd backend
source venv/bin/activate
python test_api.py
```

### Шаг 5: Сборка и запуск frontend

```bash
cd webapp
npm run build  # Для production
# или
npm run dev    # Для разработки
```

## API Endpoints

API сервер запускается на порту `8001` (PORT + 1) и предоставляет следующие endpoints:

- `GET /api/health` - Health check
- `GET /api/feed?chat_id=<id>` - Получить ленту видео для чата
- `POST /api/react` - Отправить реакцию (лайк/комментарий)
- `GET /api/video/<file_id>` - Получить информацию о видео
- `GET /api/stats` - Получить общую статистику

### Пример использования API:

```bash
# Health check
curl http://localhost:8001/api/health

# Получить статистику
curl http://localhost:8001/api/stats

# Получить ленту для чата
curl "http://localhost:8001/api/feed?chat_id=123456789"

# Отправить лайк
curl -X POST http://localhost:8001/api/react \
  -H "Content-Type: application/json" \
  -d '{"user_id": 123456789, "file_id": "video_id", "type": "like"}'
```

## Команды бота

### В групповых чатах:
- `/start` - информация о боте
- `/help` - подробная помощь
- Просто отправьте ссылку на видео!

### В личных сообщениях:
- `/start` - приветствие и инструкции
- `/help` - подробная помощь
- `/status` - ваш статус и статистика
- `/mute` - отключить уведомления о реакциях
- `/unmute` - включить уведомления о реакциях
- `/likes` - показать историю ваших реакций

## Поддерживаемые ссылки

### Instagram:
- `https://instagram.com/p/ABC123/`
- `https://instagram.com/reel/ABC123/`
- `https://instagram.com/tv/ABC123/`
- `https://instagram.com/stories/user/123/`

### TikTok:
- `https://tiktok.com/@user/video/123456`
- `https://vm.tiktok.com/ABC123/`
- `https://vt.tiktok.com/ABC123/`
- `https://tiktok.com/t/ABC123/`

## Статус разработки

✅ **Этап 1: Подготовка окружения** (завершен)
- Создана структура проекта
- Настроены виртуальные окружения
- Установлены зависимости
- Создан базовый React интерфейс
- Настроена система сборки

✅ **Этап 2: Базовый бот и автозагрузка** (завершен)
- Создан основной файл бота (`bot.py`)
- Реализован парсинг ссылок Instagram/TikTok
- Подключен yt-dlp для загрузки видео
- Автоматическая отправка видео в чат
- Сохранение метаданных в JSON
- Команды для личных сообщений
- Система тестирования

✅ **Этап 3: Хранение и доступ к метаданным** (завершен)
- Расширена система кеширования метаданных
- Создан API сервер (`api_server.py`) с aiohttp
- Реализованы REST API endpoints для WebApp
- Система реакций (лайки/комментарии)
- CORS поддержка для разработки
- Полное тестирование API
- Ограничение размера хранилища

🔄 **Следующие этапы:**
- Этап 4: Веб-приложение (WebApp)
- Этап 5: Обработка реакций и личные уведомления
- Этап 6: Интеграция WebApp с ботом
- Этап 7: Тестирование и отладка
- Этап 8: Деплой и запуск

## Технологии

- **Backend:** Python, python-telegram-bot, yt-dlp, aiohttp
- **API:** aiohttp, REST endpoints, JSON storage
- **Frontend:** React, Vite, CSS3 (градиенты, темная тема)
- **Хранение:** JSON файлы с автоматическим ограничением размера
- **Деплой:** Docker (опционально)

## Лицензия

MIT
