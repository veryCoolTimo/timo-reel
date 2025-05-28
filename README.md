# TimoReel

TimoReel — это Telegram-бот и встроенное WebApp-приложение, которое автоматически скачивает видео по ссылкам из Instagram и TikTok, присылаемые в любой чат, и собирает их в «ленту» наподобие TikTok/Instagram.

## Особенности

- 🤖 Автоматическое скачивание видео из Instagram и TikTok
- 📱 WebApp интерфейс в стиле TikTok с темной темой
- ❤️ Система лайков и комментариев
- 🔇 Возможность отключения уведомлений
- 📊 История реакций пользователя
- 💾 Локальное хранение метаданных в JSON

## Структура проекта

```
timo-reel/
├── backend/                    # Python Telegram Bot
│   ├── handlers/              # Обработчики сообщений
│   ├── downloader/            # Загрузка видео (yt-dlp)
│   ├── storage/               # JSON хранилище
│   ├── utils/                 # Конфигурация и кеш
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

### Шаг 3: Сборка frontend

```bash
cd webapp
npm run build
```

### Шаг 4: Запуск (в разработке)

#### Frontend dev server
```bash
cd webapp
npm run dev
```

#### Backend (будет реализован в следующих этапах)
```bash
cd backend
source venv/bin/activate
python bot.py
```

## Статус разработки

✅ **Этап 1: Подготовка окружения** (завершен)
- Создана структура проекта
- Настроены виртуальные окружения
- Установлены зависимости
- Создан базовый React интерфейс
- Настроена система сборки

🔄 **Следующие этапы:**
- Этап 2: Базовый бот и автозагрузка видео
- Этап 3: Хранение и доступ к метаданным
- Этап 4: Веб-приложение (WebApp)
- Этап 5: Обработка реакций и личные уведомления
- Этап 6: Интеграция WebApp с ботом
- Этап 7: Тестирование и отладка
- Этап 8: Деплой и запуск

## Технологии

- **Backend:** Python, python-telegram-bot, yt-dlp, aiohttp
- **Frontend:** React, Vite, CSS3 (градиенты, темная тема)
- **Хранение:** JSON файлы
- **Деплой:** Docker (опционально)

## Лицензия

MIT
