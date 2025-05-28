# 🚀 TimoReel - Инструкция по установке и настройке

## 📋 Описание проекта

TimoReel - это Telegram-бот с WebApp-приложением для автоматического скачивания видео из Instagram и TikTok. Бот создает "ленту" видео в стиле TikTok с системой лайков, комментариев и уведомлений.

## 🛠 Системные требования

- **Python**: 3.9+ (рекомендуется 3.11+)
- **Node.js**: 16+ (рекомендуется 18+)
- **npm**: 8+
- **Операционная система**: Linux, macOS, Windows
- **Память**: минимум 512MB RAM
- **Место на диске**: 1GB свободного места

## 📦 Установка зависимостей

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd TimoReel
```

### 2. Настройка backend (Python)

```bash
# Переходим в папку backend
cd backend

# Создаем виртуальное окружение
python3 -m venv venv

# Активируем виртуальное окружение
# На Linux/macOS:
source venv/bin/activate
# На Windows:
# venv\Scripts\activate

# Устанавливаем зависимости
pip install -r requirements.txt

# Обновляем yt-dlp до последней версии
pip install --upgrade yt-dlp
```

### 3. Настройка frontend (Node.js)

```bash
# Переходим в папку webapp
cd ../webapp

# Устанавливаем зависимости
npm install

# Проверяем установку
npm run build
```

## ⚙️ Конфигурация

### 1. Создание .env файла

Создайте файл `.env` в папке `backend/`:

```bash
cd backend
touch .env
```

Добавьте в файл `.env` следующие настройки:

```env
# Telegram Bot Token (получить у @BotFather)
BOT_TOKEN=your_bot_token_here

# Настройки сервера
HOST=0.0.0.0
PORT=8000

# Webhook URL (опционально, для production)
# WEBHOOK_URL=https://yourdomain.com
```

### 2. Получение токена бота

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен в файл `.env`

### 3. Создание директории для хранения данных

```bash
# В папке backend создаем папку storage
mkdir -p backend/storage
```

## 🚀 Запуск проекта

### Вариант 1: Запуск всех компонентов отдельно

#### Терминал 1 - API сервер:
```bash
cd backend
source venv/bin/activate  # На Windows: venv\Scripts\activate
python api_server.py
```

#### Терминал 2 - Telegram бот:
```bash
cd backend
source venv/bin/activate  # На Windows: venv\Scripts\activate
python bot.py
```

#### Терминал 3 - WebApp (для разработки):
```bash
cd webapp
npm run dev
```

### Вариант 2: Использование start_system.py

```bash
cd backend
source venv/bin/activate  # На Windows: venv\Scripts\activate
python start_system.py
```

## 🔧 Проверка работоспособности

### 1. Проверка API сервера

```bash
curl http://localhost:8001/api/health
```

Ожидаемый ответ:
```json
{
  "status": "healthy",
  "service": "TimoReel API",
  "version": "1.0.0",
  "stage": "5 - Reaction Notifications"
}
```

### 2. Проверка бота

1. Найдите вашего бота в Telegram
2. Отправьте команду `/start`
3. Бот должен ответить приветственным сообщением

### 3. Проверка WebApp

Откройте в браузере: http://localhost:3000

## 📁 Структура проекта

```
TimoReel/
├── backend/                 # Python backend
│   ├── bot.py              # Основной файл бота
│   ├── api_server.py       # API сервер
│   ├── start_system.py     # Запуск всей системы
│   ├── handlers/           # Обработчики
│   │   ├── link_handler.py # Обработка ссылок
│   │   ├── webapp_handler.py # API для WebApp
│   │   ├── pm_commands.py  # Команды в личных сообщениях
│   │   └── reaction_handler.py # Обработка реакций
│   ├── downloader/         # Загрузчик видео
│   │   └── video_downloader.py
│   ├── utils/              # Утилиты
│   │   ├── config.py       # Конфигурация
│   │   └── cache.py        # Кеширование и хранение
│   ├── storage/            # Хранилище данных
│   │   └── metadata.json   # Метаданные видео
│   ├── requirements.txt    # Python зависимости
│   └── .env               # Конфигурация (создать вручную)
│
├── webapp/                 # React frontend
│   ├── src/               # Исходный код
│   │   ├── App.jsx        # Главный компонент
│   │   ├── components/    # React компоненты
│   │   ├── styles/        # CSS стили
│   │   └── api.js         # API клиент
│   ├── public/            # Статические файлы
│   ├── package.json       # Node.js зависимости
│   └── vite.config.js     # Конфигурация сборки
│
└── docs/                  # Документация
    └── plan.txt           # План разработки
```

## 🐛 Решение проблем

### Проблема: "BOT_TOKEN не установлен"
**Решение**: Проверьте файл `.env` и убедитесь, что токен указан корректно.

### Проблема: "Address already in use"
**Решение**: Остановите запущенные процессы:
```bash
# Найти процессы на портах 8000-8001
lsof -i :8000
lsof -i :8001
# Остановить процесс по PID
kill -9 <PID>
```

### Проблема: "Cannot download video"
**Решение**: 
1. Обновите yt-dlp: `pip install --upgrade yt-dlp`
2. Проверьте, что видео публичное
3. Попробуйте другую ссылку

### Проблема: "CORS error" в WebApp
**Решение**: Убедитесь, что API сервер запущен на порту 8001.

## 📊 Команды бота

### Общие команды:
- `/start` - Запуск бота и приветствие
- `/help` - Справка по использованию

### Команды в личных сообщениях:
- `/status` - Ваш статус и статистика
- `/mute` - Отключить уведомления о реакциях
- `/unmute` - Включить уведомления о реакциях
- `/likes` - История ваших реакций

## 🌐 Production деплой

### 1. Настройка webhook (рекомендуется)

В файле `.env` добавьте:
```env
WEBHOOK_URL=https://yourdomain.com
```

### 2. Настройка HTTPS

Для production обязательно используйте HTTPS для webhook и WebApp.

### 3. Настройка WebApp в BotFather

1. Откройте [@BotFather](https://t.me/BotFather)
2. Выберите вашего бота
3. Нажмите "Bot Settings" → "Menu Button"
4. Укажите URL вашего WebApp: `https://yourdomain.com`

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи в терминале
2. Убедитесь, что все зависимости установлены
3. Проверьте файл `.env`
4. Перезапустите все компоненты

---

**Готово! 🎉 TimoReel настроен и готов к работе.** 