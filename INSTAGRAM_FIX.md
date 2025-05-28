# Решение проблем с Instagram на серверах

## Проблема

На серверах Instagram часто блокирует загрузку видео из-за:
- Rate-limit (ограничение запросов)
- Блокировка серверных IP адресов
- Требование аутентификации
- Антибот защита

**Ошибка в логах:**
```
ERROR: [Instagram] DKJzBhlJJ7i: Requested content is not available, rate-limit reached or login required
```

## Решения

### 🔧 Быстрое решение

1. **Запустите диагностику:**
```bash
cd backend
python instagram_diagnostic.py
```

2. **Получите cookies из браузера:**
```bash
python get_instagram_cookies.py
```

3. **Перезапустите бота:**
```bash
python run_background.py restart
```

### 🛠️ Подробные решения

#### 1. Использование Cookies (рекомендуется)

**Автоматически:**
```bash
cd backend
python get_instagram_cookies.py
```

**Вручную:**
1. Откройте Instagram в браузере
2. Войдите в аккаунт
3. Откройте Developer Tools (F12)
4. Network → найдите запрос к instagram.com
5. Скопируйте Cookie заголовок
6. Сохраните в `backend/cookies/instagram.txt`

#### 2. Обновление yt-dlp

```bash
pip install -U yt-dlp
```

#### 3. Использование прокси

Отредактируйте `backend/downloader/instagram_fix.py`:
```python
PROXY_LIST = [
    'http://user:pass@proxy1.com:8080',
    'http://user:pass@proxy2.com:8080',
]
```

#### 4. Настройка задержек

Система автоматически добавляет задержки между запросами:
- 2-5 секунд между обычными запросами
- 3-6 секунд на серверах
- Дополнительные задержки при rate-limit

### 📊 Мониторинг

**Проверка логов:**
```bash
# Общие логи бота
tail -f backend/logs/bot.log

# Ошибки Instagram
tail -f backend/logs/instagram_errors.log

# Поиск rate-limit ошибок
grep "rate-limit" backend/logs/bot.log
```

**Статистика ошибок:**
```bash
# Количество ошибок за сегодня
grep "$(date +%Y-%m-%d)" backend/logs/instagram_errors.log | wc -l

# Последние 10 ошибок
tail -10 backend/logs/instagram_errors.log
```

### 🔍 Диагностика проблем

**Полная диагностика:**
```bash
cd backend
python instagram_diagnostic.py
```

**Проверка конкретной ссылки:**
```bash
cd backend
python -c "
from downloader.video_downloader import downloader
result = downloader.extract_info('YOUR_INSTAGRAM_URL')
print('Success!' if result else 'Failed!')
"
```

### 🌐 Серверные особенности

**Проблемы серверных IP:**
- VPS/Cloud IP часто блокируются
- Используйте residential прокси
- Рассмотрите смену провайдера

**Рекомендуемые настройки для серверов:**
- Обязательно используйте cookies
- Добавьте прокси
- Увеличьте задержки
- Ротируйте User-Agent

### 🔒 Безопасность

**Cookies:**
- Никогда не делитесь cookies файлами
- Используйте отдельный аккаунт для бота
- Регулярно обновляйте cookies
- Добавьте `cookies/` в `.gitignore`

**Прокси:**
- Используйте надежные прокси сервисы
- Избегайте бесплатных прокси
- Ротируйте прокси регулярно

### 📈 Оптимизация производительности

**Настройки качества:**
```python
# В instagram_fix.py
'format': 'best[height<=720]',  # Ограничение качества
'socket_timeout': 60,           # Увеличенный таймаут
```

**Кеширование:**
- Система автоматически кеширует успешные запросы
- Избегает повторных запросов к тем же URL

### 🚨 Troubleshooting

**Ошибка: "No cookies file found"**
```bash
python get_instagram_cookies.py
```

**Ошибка: "Rate limit detected"**
- Подождите 10-15 минут
- Используйте cookies
- Добавьте прокси

**Ошибка: "Login required"**
- Обязательно используйте cookies
- Проверьте валидность cookies

**Ошибка: "IP blocked"**
- Смените IP/прокси
- Используйте VPN
- Подождите несколько часов

### 📝 Логи и отладка

**Включение подробных логов:**
```python
# В bot.py добавьте:
logging.getLogger('downloader.video_downloader').setLevel(logging.DEBUG)
logging.getLogger('downloader.instagram_fix').setLevel(logging.DEBUG)
```

**Анализ ошибок:**
```bash
# Группировка ошибок по типу
grep -o "ERROR:.*" backend/logs/bot.log | sort | uniq -c

# Статистика по времени
grep "rate-limit" backend/logs/bot.log | cut -d' ' -f1-2 | sort | uniq -c
```

### 🔄 Автоматическое восстановление

Система автоматически:
- Пробует fallback конфигурации
- Добавляет задержки при rate-limit
- Ротирует User-Agent строки
- Логирует ошибки для анализа

### 📞 Поддержка

Если проблемы продолжаются:

1. Запустите полную диагностику
2. Проверьте логи ошибок
3. Убедитесь что cookies актуальные
4. Рассмотрите использование прокси
5. Попробуйте с другого IP

**Полезные команды:**
```bash
# Полная диагностика
python instagram_diagnostic.py

# Получение cookies
python get_instagram_cookies.py

# Перезапуск с новыми настройками
python run_background.py restart

# Мониторинг логов
tail -f logs/bot.log | grep -i instagram
``` 