#!/usr/bin/env python3
"""
НейроБарбоскины - Запуск сервера стрима
Запуск: python run.py
Сервер будет доступен на http://localhost:8000
"""

import subprocess
import sys
import os

def check_dependencies():
    """Проверяет и устанавливает зависимости"""
    try:
        import flask
        import flask_socketio
        print("[OK] Все зависимости установлены")
        return True
    except ImportError as e:
        print(f"[ERROR] Отсутствует зависимость: {e}")
        print("[INFO] Установка зависимостей...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("[OK] Зависимости установлены успешно")
            return True
        except subprocess.CalledProcessError:
            print("[ERROR] Ошибка при установке зависимостей")
            return False

def main():
    print("=" * 50)
    print("НЕЙРОБАРБОСКИНЫ - СТРИМ СЕРВЕР")
    print("=" * 50)
    
    if not check_dependencies():
        sys.exit(1)
    
    print("\n[INFO] Запуск сервера на порту 8000...")
    print("[INFO] Откройте в браузере: http://localhost:8000")
    print("[INFO] Для остановки нажмите Ctrl+C")
    print("-" * 50)
    
    # Запускаем основной сервер
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    from app import socketio, app
    socketio.run(app, host='0.0.0.0', port=8000, debug=False, allow_unsafe_werkzeug=True)

if __name__ == '__main__':
    main()