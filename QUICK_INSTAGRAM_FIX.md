# 🚀 Быстрое решение проблемы с Instagram

## Проблема
```
ERROR: [Instagram] DKJzBhlJJ7i: Requested content is not available, rate-limit reached or login required
```

## ⚡ Быстрое решение (5 минут)

### 1. На локальной машине (где Instagram работает):

```bash
cd backend
source venv/bin/activate
python get_instagram_cookies.py
```

### 2. Скопируйте cookies на сервер:

```bash
# Скопируйте содержимое файла cookies/instagram.txt
cat cookies/instagram.txt

# На сервере создайте файл:
mkdir -p cookies
nano cookies/instagram.txt
# Вставьте скопированное содержимое
```

### 3. На сервере перезапустите бота:

```bash
cd /path/to/TimoReel/backend
source venv/bin/activate
python run_background.py restart
```

### 4. Проверьте работу:

```bash
# Проверьте логи
tail -f logs/bot.log | grep -i instagram

# Отправьте Instagram ссылку боту в Telegram
```

## ✅ Готово!

Теперь Instagram должен работать на сервере.

## 📊 Мониторинг

```bash
# Проверка ошибок
grep "rate-limit" logs/bot.log

# Успешные загрузки
grep "Instagram download successful" logs/bot.log
```

## 🔄 Если не работает

1. **Обновите yt-dlp:** `pip install -U yt-dlp`
2. **Проверьте cookies:** `ls -la cookies/instagram.txt`
3. **Запустите диагностику:** `python instagram_diagnostic.py`
4. **Подождите 15-30 минут** (rate-limit)

## 📞 Дополнительная помощь

- Полная инструкция: `SERVER_INSTAGRAM_SETUP.md`
- Диагностика: `INSTAGRAM_FIX.md`
- Техподдержка: проверьте логи в `logs/instagram_errors.log` 