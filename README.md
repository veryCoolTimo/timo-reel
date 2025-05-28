# 🎬 TimoReel

**Telegram-бот с WebApp для автоматического скачивания видео из Instagram и TikTok**

Создает "ленту" видео в стиле TikTok с системой лайков, комментариев и уведомлений.

## ⚡ Быстрый старт

### Автоматическая установка

**Linux/macOS:**
```bash
./install.sh
```

**Windows:**
```cmd
install.bat
```

### Ручная установка

1. **Клонируйте репозиторий:**
```bash
git clone <repository-url>
cd TimoReel
```

2. **Настройте backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Настройте frontend:**
```bash
cd ../webapp
npm install
```

4. **Создайте .env файл:**
```bash
cd ../backend
echo "BOT_TOKEN=your_bot_token_here" > .env
```

## 🚀 Запуск

**Все компоненты сразу:**
```bash
cd backend
source venv/bin/activate
python start_system.py
```

**Или по отдельности:**
```bash
# Терминал 1 - API сервер
cd backend && source venv/bin/activate && python api_server.py

# Терминал 2 - Telegram бот  
cd backend && source venv/bin/activate && python bot.py

# Терминал 3 - WebApp (разработка)
cd webapp && npm run dev
```

## 🔗 Ссылки

- **WebApp**: http://localhost:3000
- **API**: http://localhost:8001/api/health
- **Документация**: [SETUP_GUIDE.md](SETUP_GUIDE.md)

## ✨ Возможности

- 📱 Автоматическое скачивание видео из Instagram/TikTok
- 🎬 Лента видео в стиле TikTok
- ❤️ Система лайков и комментариев
- 🔔 Уведомления авторам видео
- ⚙️ Настройки пользователей (mute/unmute)
- 📊 Статистика реакций

## 🛠 Команды бота

- `/start` - Запуск и приветствие
- `/help` - Справка
- `/status` - Статус пользователя
- `/mute` / `/unmute` - Управление уведомлениями
- `/likes` - История реакций

## 📞 Поддержка

Подробная документация: [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

**Готово к использованию! 🎉**
