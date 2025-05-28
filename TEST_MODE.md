# 🧪 TimoReel - Тестовый режим

## 📝 Настройка тестового токена

Для локальной разработки используется отдельный тестовый бот, чтобы не конфликтовать с продакшн версией.

### 1. Создание тестового бота

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Дайте боту название, например: `TimoReel Test Bot`
4. Дайте username, например: `timoreel_test_bot`
5. Скопируйте полученный токен

### 2. Настройка .env файла

Откройте файл `backend/.env` и замените `TEST_BOT_TOKEN_HERE` на ваш тестовый токен:

```env
# TEST TOKEN для локальной разработки
BOT_TOKEN=your_test_token_here

# PRODUCTION TOKEN (ОТКЛЮЧЕН - используется на сервере)
# BOT_TOKEN=8084528706:AAFZE7AtYlwISq2h3ImypLRO2V82vJdpxsU

# Server settings
HOST=0.0.0.0
PORT=8000
```

### 3. Запуск в тестовом режиме

```bash
cd backend
source venv/bin/activate

# Запуск в фоновом режиме
python run_background.py start

# Или ручной запуск для отладки
python bot.py  # В одном терминале
python api_server.py  # В другом терминале
```

### 4. Проверка работы

```bash
# Статус процессов
python run_background.py status

# Проверка API
curl http://localhost:8001/api/health

# Просмотр логов
tail -f logs/bot.log logs/api.log
```

## 🔄 Переключение между режимами

### На тестовый режим:
```bash
# Остановить все процессы
python run_background.py stop

# Редактировать .env
nano .env
# Убедиться что BOT_TOKEN указывает на тестовый токен
```

### На продакшн режим:
```bash
# Остановить все процессы
python run_background.py stop

# Редактировать .env
nano .env
# Изменить BOT_TOKEN на продакшн токен
```

## 📊 Мониторинг логов

### Просмотр в реальном времени:
```bash
tail -f logs/bot.log logs/api.log
```

### Поиск ошибок:
```bash
grep "ERROR" logs/bot.log | tail -10
grep "ERROR" logs/api.log | tail -10
```

### Последние записи:
```bash
tail -20 logs/bot.log
tail -20 logs/api.log
```

## ⚠️ Важные замечания

1. **Не запускайте одновременно тестовый и продакшн бот** - это вызовет конфликт
2. **Используйте разные чаты** для тестирования и продакшена
3. **Логи сохраняются** в `logs/` даже после остановки процессов
4. **Порты** остаются теми же: 8000 (бот), 8001 (API), 3000 (WebApp)

## 🛑 Экстренная остановка

```bash
# Остановка через скрипт
python run_background.py stop

# Принудительная остановка всех процессов
pkill -f "python.*bot.py"
pkill -f "python.*api_server.py"
pkill -f "npm.*dev"

# Освобождение портов
lsof -ti:8000,8001,3000 | xargs kill -9
```

---

**Тестовый режим готов! 🧪 Теперь можно безопасно разрабатывать локально.** 