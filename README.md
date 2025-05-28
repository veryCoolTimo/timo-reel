# TimoReel 🎬

Telegram-бот с WebApp для автоматического скачивания видео из Instagram и TikTok. Создает ленту видео в стиле TikTok с системой лайков и комментариев.

## 🚀 Быстрый старт

### 1. Настройка бота

```bash
cd backend
source venv/bin/activate
python setup_env.py
```

Следуйте инструкциям для получения токена от @BotFather в Telegram.

### 2. Запуск системы

**Вариант 1: Полная система (бот + API)**
```bash
cd backend
source venv/bin/activate
python start_system.py
```

**Вариант 2: Раздельный запуск**

Терминал 1 - API сервер:
```bash
cd backend
source venv/bin/activate
python api_server.py
```

Терминал 2 - Telegram бот:
```bash
cd backend
source venv/bin/activate
python bot.py
```

Терминал 3 - WebApp:
```bash
cd webapp
npm run dev
```

### 3. Проверка работы

- **Бот**: Отправьте `/start` боту в Telegram
- **API**: http://localhost:8001/api/health
- **WebApp**: http://localhost:3000

## 📱 Функции

### Telegram Bot
- ✅ Команда `/start` - приветствие и инструкции
- ✅ Команда `/help` - подробная помощь
- ✅ Автоматическое скачивание видео по ссылкам Instagram/TikTok
- ✅ Команды в личных сообщениях:
  - `/status` - ваш статус и статистика
  - `/mute` - отключить уведомления
  - `/unmute` - включить уведомления
  - `/likes` - история реакций

### WebApp
- ✅ Лента видео в стиле TikTok
- ✅ Темная тема с градиентами
- ✅ Кнопки лайков и комментариев
- ✅ Полноэкранный видео-плеер
- ✅ Responsive дизайн

### API Server
- ✅ REST API для WebApp
- ✅ CORS поддержка
- ✅ Endpoints:
  - `GET /api/feed?chat_id=<id>` - лента видео
  - `POST /api/react` - отправка реакций
  - `GET /api/stats` - статистика
  - `GET /api/health` - health check

## 🔧 Поддерживаемые ссылки

### Instagram
- `https://instagram.com/p/ABC123/`
- `https://instagram.com/reel/ABC123/`
- `https://instagram.com/tv/ABC123/`

### TikTok
- `https://tiktok.com/@user/video/123456`
- `https://vm.tiktok.com/ABC123/`
- `https://vt.tiktok.com/ABC123/`

## 📊 Текущий статус

✅ **Этап 1**: Подготовка окружения  
✅ **Этап 2**: Базовый бот и автозагрузка  
✅ **Этап 3**: Хранение и доступ к метаданным  
✅ **Этап 4**: Веб-приложение (WebApp)  
🔄 **Этап 5**: Обработка реакций и личные уведомления  

## 🛠 Технологии

- **Backend**: Python 3.13, python-telegram-bot, aiohttp, yt-dlp
- **Frontend**: React, Vite, Telegram WebApp SDK
- **Storage**: JSON файлы (локальное хранение)

## 📁 Структура проекта

```
TimoReel/
├── backend/                 # Python backend
│   ├── bot.py              # Telegram бот
│   ├── api_server.py       # API сервер
│   ├── start_system.py     # Запуск всей системы
│   ├── setup_env.py        # Настройка .env
│   ├── handlers/           # Обработчики
│   ├── downloader/         # Загрузчик видео
│   ├── storage/            # JSON хранилище
│   └── utils/              # Утилиты
├── webapp/                 # React frontend
│   ├── src/                # Исходники
│   ├── public/             # Статика
│   └── dist/               # Сборка
└── docs/                   # Документация
```

## 🐛 Решение проблем

### Бот не отвечает
1. Проверьте токен в `.env` файле
2. Убедитесь что бот запущен: `python bot.py`
3. Проверьте логи в терминале

### WebApp не загружается
1. Убедитесь что API сервер запущен на порту 8001
2. Проверьте CORS настройки
3. Откройте DevTools в браузере для ошибок

### Видео не скачиваются
1. Проверьте что ссылка публичная
2. Убедитесь что видео не превышает 50MB
3. Проверьте подключение к интернету

## 📞 Поддержка

Если возникли проблемы:
1. Проверьте логи в терминале
2. Убедитесь что все зависимости установлены
3. Проверьте что порты 8000, 8001, 3000 свободны

---

**TimoReel** - создано для удобного просмотра видео из социальных сетей в Telegram! 🎬✨
