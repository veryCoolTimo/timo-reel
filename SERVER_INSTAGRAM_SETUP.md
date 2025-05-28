# Настройка Instagram на сервере

## Проблема на сервере

На вашем сервере Instagram блокирует загрузку из-за:
- Серверный IP адрес (VPS/Cloud)
- Rate-limit ограничения
- Отсутствие аутентификации

## Решение

### 1. Загрузите обновленные файлы на сервер

```bash
# На сервере, в директории TimoReel/backend
git pull  # или загрузите файлы вручную

# Убедитесь что есть новые файлы:
ls -la downloader/instagram_fix.py
ls -la get_instagram_cookies.py
ls -la instagram_diagnostic.py
```

### 2. Получите cookies с локальной машины

**На локальной машине (где Instagram работает):**

```bash
cd backend
source venv/bin/activate
python get_instagram_cookies.py
```

Это создаст файл `cookies/instagram.txt` с вашими cookies.

### 3. Скопируйте cookies на сервер

```bash
# Скопируйте файл cookies/instagram.txt на сервер
scp cookies/instagram.txt user@your-server:/path/to/TimoReel/backend/cookies/

# Или создайте файл вручную на сервере:
mkdir -p cookies
nano cookies/instagram.txt
# Вставьте содержимое файла cookies
```

### 4. Проверьте настройки на сервере

```bash
# На сервере
cd /path/to/TimoReel/backend
source venv/bin/activate

# Запустите диагностику
python instagram_diagnostic.py

# Проверьте cookies
ls -la cookies/instagram.txt
```

### 5. Обновите зависимости

```bash
# Установите новые зависимости
pip install browser_cookie3 requests

# Обновите yt-dlp
pip install -U yt-dlp
```

### 6. Перезапустите бота

```bash
# Остановите бота
python run_background.py stop

# Запустите заново
python run_background.py start

# Проверьте логи
tail -f logs/bot.log | grep -i instagram
```

### 7. Тестирование

```bash
# Протестируйте Instagram загрузку
python test_instagram.py

# Или отправьте Instagram ссылку боту в Telegram
```

## Мониторинг

### Проверка логов

```bash
# Общие логи
tail -f logs/bot.log

# Instagram ошибки
tail -f logs/instagram_errors.log

# Поиск успешных загрузок
grep "Instagram download successful" logs/bot.log

# Поиск ошибок rate-limit
grep "rate-limit" logs/bot.log
```

### Статистика

```bash
# Количество Instagram ошибок сегодня
grep "$(date +%Y-%m-%d)" logs/instagram_errors.log | wc -l

# Последние 10 ошибок
tail -10 logs/instagram_errors.log

# Успешные загрузки за сегодня
grep "$(date +%Y-%m-%d)" logs/bot.log | grep "Instagram download successful" | wc -l
```

## Дополнительные настройки

### Использование прокси (опционально)

Если cookies не помогают, добавьте прокси:

```python
# В файле downloader/instagram_fix.py
PROXY_LIST = [
    'http://user:pass@proxy1.com:8080',
    'http://user:pass@proxy2.com:8080',
]
```

### Увеличение задержек

```python
# В файле downloader/instagram_fix.py
# Увеличьте задержки для серверов:
'sleep_interval': random.uniform(5, 10),  # Было 3-6
'max_sleep_interval': 15,                 # Было 10
```

## Troubleshooting

### Ошибка: "No cookies file found"

```bash
# Проверьте наличие файла
ls -la cookies/instagram.txt

# Если файла нет, скопируйте с локальной машины
# или создайте заново
```

### Ошибка: "Rate limit detected"

```bash
# Подождите 15-30 минут
# Проверьте что cookies актуальные
# Рассмотрите использование прокси
```

### Ошибка: "Login required"

```bash
# Обновите cookies с локальной машины
# Убедитесь что вы залогинены в Instagram в браузере
```

### Ошибка: "IP blocked"

```bash
# Используйте VPN или прокси
# Смените IP сервера
# Подождите несколько часов
```

## Автоматическое обновление cookies

Создайте cron job для регулярного обновления cookies:

```bash
# На локальной машине создайте скрипт
nano update_cookies.sh
```

```bash
#!/bin/bash
cd /path/to/TimoReel/backend
source venv/bin/activate
python get_instagram_cookies.py
scp cookies/instagram.txt user@server:/path/to/TimoReel/backend/cookies/
ssh user@server "cd /path/to/TimoReel/backend && python run_background.py restart"
```

```bash
# Добавьте в crontab (обновление каждые 12 часов)
crontab -e
0 */12 * * * /path/to/update_cookies.sh
```

## Проверка работы

После настройки:

1. ✅ Cookies файл существует: `ls cookies/instagram.txt`
2. ✅ Диагностика проходит: `python instagram_diagnostic.py`
3. ✅ Бот запущен: `python run_background.py status`
4. ✅ Логи показывают "Using cookies": `grep "Using cookies" logs/bot.log`
5. ✅ Instagram ссылки загружаются в Telegram

## Поддержка

Если проблемы продолжаются:

1. Запустите полную диагностику: `python instagram_diagnostic.py`
2. Проверьте логи: `tail -50 logs/bot.log`
3. Убедитесь что cookies актуальные
4. Рассмотрите использование прокси
5. Попробуйте с другого сервера/IP 