#!/bin/bash

# TimoReel - Скрипт автоматической установки
# Для Linux и macOS

set -e  # Остановка при ошибке

echo "🚀 TimoReel - Автоматическая установка"
echo "======================================"

# Проверка Python
echo "📋 Проверка системных требований..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python 3.9+ и повторите попытку."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION найден"

# Проверка Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js не найден. Установите Node.js 16+ и повторите попытку."
    exit 1
fi

NODE_VERSION=$(node --version)
echo "✅ Node.js $NODE_VERSION найден"

# Проверка npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm не найден. Установите npm и повторите попытку."
    exit 1
fi

NPM_VERSION=$(npm --version)
echo "✅ npm $NPM_VERSION найден"

echo ""
echo "📦 Установка зависимостей..."

# Установка backend зависимостей
echo "🐍 Настройка Python backend..."
cd backend

# Создание виртуального окружения
if [ ! -d "venv" ]; then
    echo "   Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активация виртуального окружения
echo "   Активация виртуального окружения..."
source venv/bin/activate

# Установка зависимостей
echo "   Установка Python зависимостей..."
pip install --upgrade pip
pip install -r requirements.txt

# Обновление yt-dlp
echo "   Обновление yt-dlp..."
pip install --upgrade yt-dlp

echo "✅ Backend настроен"

# Установка frontend зависимостей
echo ""
echo "⚛️ Настройка React frontend..."
cd ../webapp

echo "   Установка Node.js зависимостей..."
npm install

echo "   Проверка сборки..."
npm run build

echo "✅ Frontend настроен"

# Создание директории storage
echo ""
echo "📁 Создание директорий..."
cd ../backend
mkdir -p storage
echo "✅ Директория storage создана"

# Проверка .env файла
echo ""
echo "⚙️ Проверка конфигурации..."
if [ ! -f ".env" ]; then
    echo "⚠️  Файл .env не найден. Создание шаблона..."
    cat > .env << EOF
# Telegram Bot Token (получить у @BotFather)
BOT_TOKEN=your_bot_token_here

# Настройки сервера
HOST=0.0.0.0
PORT=8000

# Webhook URL (опционально, для production)
# WEBHOOK_URL=https://yourdomain.com
EOF
    echo "📝 Создан файл .env с шаблоном"
    echo "❗ ВАЖНО: Отредактируйте файл backend/.env и добавьте ваш BOT_TOKEN"
else
    echo "✅ Файл .env найден"
fi

echo ""
echo "🎉 Установка завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Отредактируйте файл backend/.env и добавьте ваш BOT_TOKEN"
echo "2. Получите токен у @BotFather в Telegram"
echo "3. Запустите проект:"
echo ""
echo "   # Вариант 1 - Все компоненты отдельно:"
echo "   cd backend && source venv/bin/activate && python api_server.py"
echo "   cd backend && source venv/bin/activate && python bot.py"
echo "   cd webapp && npm run dev"
echo ""
echo "   # Вариант 2 - Автоматический запуск:"
echo "   cd backend && source venv/bin/activate && python start_system.py"
echo ""
echo "🔗 Полезные ссылки:"
echo "   - API Health Check: http://localhost:8001/api/health"
echo "   - WebApp: http://localhost:3000"
echo "   - Документация: SETUP_GUIDE.md"
echo ""
echo "✨ Удачи с TimoReel!" 