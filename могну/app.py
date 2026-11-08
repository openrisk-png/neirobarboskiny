from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'neurobarboskins_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Хранение сообщений чата и текущей темы
chat_messages = []
current_topic = "Ожидание темы стрима..."
online_users = set()

@app.route('/')
def index():
    return render_template('index.html', current_topic=current_topic)

@socketio.on('connect')
def handle_connect():
    online_users.add(request.sid)
    emit('online_count', {'count': len(online_users)}, broadcast=True)
    # Отправляем историю сообщений новому пользователю
    emit('chat_history', {'messages': chat_messages})
    emit('topic_update', {'topic': current_topic})

@socketio.on('disconnect')
def handle_disconnect():
    online_users.discard(request.sid)
    emit('online_count', {'count': len(online_users)}, broadcast=True)

@socketio.on('send_message')
def handle_message(data):
    username = data.get('username', 'Аноним')[:20]
    message = data.get('message', '')[:500]
    
    if not message.strip():
        return
    
    # Проверка на команду /тема
    if message.startswith('/тема '):
        global current_topic
        new_topic = message[6:].strip()
        if new_topic:
            current_topic = new_topic
            emit('topic_update', {'topic': current_topic}, broadcast=True)
            # Добавляем системное сообщение о смене темы
            system_msg = {
                'username': 'Система',
                'message': f'🎯 Тема стрима изменена: {current_topic}',
                'is_system': True,
                'timestamp': ''
            }
            chat_messages.append(system_msg)
            emit('new_message', system_msg, broadcast=True)
        return
    
    # Обычное сообщение
    msg_data = {
        'username': username,
        'message': message,
        'is_system': False,
        'timestamp': ''
    }
    chat_messages.append(msg_data)
    
    # Ограничиваем историю последними 100 сообщениями
    if len(chat_messages) > 100:
        chat_messages.pop(0)
    
    emit('new_message', msg_data, broadcast=True)

if __name__ == '__main__':
    print("🚀 НейроБарбоскины сервер запущен на http://localhost:8000")
    socketio.run(app, host='0.0.0.0', port=8000, debug=False)