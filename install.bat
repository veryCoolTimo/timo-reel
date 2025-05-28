@echo off
chcp 65001 >nul

REM TimoReel - Скрипт автоматической установки для Windows

echo 🚀 TimoReel - Автоматическая установка
echo ======================================

REM Проверка Python
echo 📋 Проверка системных требований...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден. Установите Python 3.9+ и повторите попытку.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% найден

REM Проверка Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js не найден. Установите Node.js 16+ и повторите попытку.
    pause
    exit /b 1
)

for /f %%i in ('node --version') do set NODE_VERSION=%%i
echo ✅ Node.js %NODE_VERSION% найден

REM Проверка npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm не найден. Установите npm и повторите попытку.
    pause
    exit /b 1
)

for /f %%i in ('npm --version') do set NPM_VERSION=%%i
echo ✅ npm %NPM_VERSION% найден

echo.
echo 📦 Установка зависимостей...

REM Установка backend зависимостей
echo 🐍 Настройка Python backend...
cd backend

REM Создание виртуального окружения
if not exist "venv" (
    echo    Создание виртуального окружения...
    python -m venv venv
)

REM Активация виртуального окружения
echo    Активация виртуального окружения...
call venv\Scripts\activate.bat

REM Установка зависимостей
echo    Установка Python зависимостей...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Обновление yt-dlp
echo    Обновление yt-dlp...
pip install --upgrade yt-dlp

echo ✅ Backend настроен

REM Установка frontend зависимостей
echo.
echo ⚛️ Настройка React frontend...
cd ..\webapp

echo    Установка Node.js зависимостей...
npm install

echo    Проверка сборки...
npm run build

echo ✅ Frontend настроен

REM Создание директории storage
echo.
echo 📁 Создание директорий...
cd ..\backend
if not exist "storage" mkdir storage
echo ✅ Директория storage создана

REM Проверка .env файла
echo.
echo ⚙️ Проверка конфигурации...
if not exist ".env" (
    echo ⚠️  Файл .env не найден. Создание шаблона...
    (
        echo # Telegram Bot Token ^(получить у @BotFather^)
        echo BOT_TOKEN=your_bot_token_here
        echo.
        echo # Настройки сервера
        echo HOST=0.0.0.0
        echo PORT=8000
        echo.
        echo # Webhook URL ^(опционально, для production^)
        echo # WEBHOOK_URL=https://yourdomain.com
    ) > .env
    echo 📝 Создан файл .env с шаблоном
    echo ❗ ВАЖНО: Отредактируйте файл backend\.env и добавьте ваш BOT_TOKEN
) else (
    echo ✅ Файл .env найден
)

echo.
echo 🎉 Установка завершена!
echo.
echo 📋 Следующие шаги:
echo 1. Отредактируйте файл backend\.env и добавьте ваш BOT_TOKEN
echo 2. Получите токен у @BotFather в Telegram
echo 3. Запустите проект:
echo.
echo    # Вариант 1 - Все компоненты отдельно:
echo    cd backend ^&^& venv\Scripts\activate ^&^& python api_server.py
echo    cd backend ^&^& venv\Scripts\activate ^&^& python bot.py
echo    cd webapp ^&^& npm run dev
echo.
echo    # Вариант 2 - Автоматический запуск:
echo    cd backend ^&^& venv\Scripts\activate ^&^& python start_system.py
echo.
echo 🔗 Полезные ссылки:
echo    - API Health Check: http://localhost:8001/api/health
echo    - WebApp: http://localhost:3000
echo    - Документация: SETUP_GUIDE.md
echo.
echo ✨ Удачи с TimoReel!
pause 