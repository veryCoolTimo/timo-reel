#!/usr/bin/env python3
"""
Скрипт для настройки .env файла TimoReel
"""

import os
from pathlib import Path

def create_env_file():
    """Создает .env файл с настройками"""
    env_path = Path(__file__).parent / ".env"
    
    print("🔧 Настройка TimoReel Bot")
    print("=" * 40)
    
    if env_path.exists():
        print("⚠️  Файл .env уже существует!")
        overwrite = input("Перезаписать? (y/N): ").lower().strip()
        if overwrite != 'y':
            print("❌ Настройка отменена")
            return False
    
    print("\n📱 Получение токена бота:")
    print("1. Откройте Telegram и найдите @BotFather")
    print("2. Отправьте команду /newbot")
    print("3. Выберите имя для бота (например: TimoReel Bot)")
    print("4. Выберите username для бота (например: timoreel_bot)")
    print("5. Скопируйте полученный токен")
    print()
    
    while True:
        token = input("🔑 Введите токен бота: ").strip()
        
        if not token:
            print("❌ Токен не может быть пустым!")
            continue
            
        if not token.startswith(('1', '2', '5', '6', '7')):
            print("❌ Токен должен начинаться с цифры!")
            continue
            
        if ':' not in token:
            print("❌ Неверный формат токена! Должен содержать ':'")
            continue
            
        break
    
    # Создаем .env файл
    env_content = f"""# Telegram Bot Configuration
BOT_TOKEN={token}

# Server Configuration  
HOST=0.0.0.0
PORT=8000

# Webhook Configuration (оставьте пустым для polling)
WEBHOOK_URL=
"""
    
    try:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print(f"✅ Файл .env создан: {env_path}")
        print("\n🚀 Теперь можно запустить систему:")
        print("   python start_system.py")
        print("\n📱 Или запустить только бота:")
        print("   python bot.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания файла: {e}")
        return False

if __name__ == '__main__':
    try:
        create_env_file()
    except KeyboardInterrupt:
        print("\n❌ Настройка прервана пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}") 