# 🐧 TimoReel - Установка на Ubuntu Server

## Быстрая установка

### 1. Обновление системы
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Установка зависимостей
```bash
# Python 3.9+
sudo apt install python3 python3-pip python3-venv -y

# Node.js 16+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Дополнительные пакеты
sudo apt install git curl wget -y
```

### 3. Клонирование и установка
```bash
git clone <your-repo-url> TimoReel
cd TimoReel
chmod +x install.sh
./install.sh
```

### 4. Настройка
```bash
cd backend
nano .env
```

Добавьте ваш токен:
```env
BOT_TOKEN=your_bot_token_here
HOST=0.0.0.0
PORT=8000
```

### 5. Запуск в фоновом режиме
```bash
cd backend
source venv/bin/activate
python run_background.py start
```

## Проверка работы

```bash
# Статус процессов
python run_background.py status

# Проверка API
curl http://localhost:8001/api/health

# Просмотр логов
tail -f logs/bot.log logs/api.log
```

## Автозапуск (systemd)

### 1. Создание сервиса
```bash
sudo nano /etc/systemd/system/timoreel.service
```

```ini
[Unit]
Description=TimoReel Telegram Bot
After=network.target

[Service]
Type=forking
User=your_username
WorkingDirectory=/path/to/TimoReel/backend
ExecStart=/path/to/TimoReel/backend/venv/bin/python run_background.py start
ExecStop=/path/to/TimoReel/backend/venv/bin/python run_background.py stop
Restart=always

[Install]
WantedBy=multi-user.target
```

### 2. Активация сервиса
```bash
sudo systemctl daemon-reload
sudo systemctl enable timoreel
sudo systemctl start timoreel
sudo systemctl status timoreel
```

## Решение проблем Ubuntu

### "terser not found"
```bash
cd webapp
npm install terser --save-dev
npm run build
```

### Права доступа
```bash
chmod +x backend/run_background.py
chown -R $USER:$USER TimoReel/
```

### Firewall (если нужен внешний доступ)
```bash
sudo ufw allow 8000
sudo ufw allow 8001
sudo ufw allow 3000
```

---

**TimoReel готов к работе на Ubuntu! 🚀** 