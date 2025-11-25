from flask import Flask, render_template
from flask_sock import Sock
from datetime import datetime
import json

from user import User
from system import System
from problem_solver import ProblemSolver

app = Flask(__name__, template_folder="templates")
app.config["SECRET_KEY"] = "change_this_secret_key"

# WebSocket-расширение
sock = Sock(app)

# Твои игровые объекты (как в main.py)
user = User("Пользователь")
system = System()
problem_solver = ProblemSolver()

# Общая история чата (для простоты — в памяти процесса)
history = []  # элементы: {"role": "user"/"system", "text": "...", "time": "HH:MM:SS"}


def now_time():
    return datetime.now().strftime("%H:%M:%S")


# Стартовое приветствие от системы — как в main.py через system.greating_message()
greeting = system.greating_message()
user.history.append(greeting)
history.append({
    "role": "system",
    "text": greeting,
    "time": now_time(),
})


@app.route("/")
def index():
    # Отрисовываем начальную страницу, history пробрасываем только для первой загрузки.
    return render_template("chat.html", history=history)


@sock.route("/ws")
def ws_chat(ws):
    """
    Обработчик WebSocket-соединения.
    На каждый подключившийся браузер — отдельный цикл while True.
    """
    # При подключении сразу отправляем клиенту всю историю
    ws.send(json.dumps({
        "type": "history",
        "messages": history,
    }, ensure_ascii=False))

    # Основной цикл обмена
    while True:
        data = ws.receive()
        if data is None:
            # Клиент отключился
            break

        try:
            payload = json.loads(data)
        except Exception:
            # Неверный формат — игнорируем
            continue

        text = str(payload.get("text", "")).strip()
        if not text:
            continue

        # === Сообщение пользователя ===
        send_time = now_time()
        user_msg = {
            "role": "user",
            "text": text,
            "time": send_time,
        }
        history.append(user_msg)

        # Эхо-посылка сообщения пользователя клиенту (чтобы не ждать ответа системы)
        ws.send(json.dumps({
            "type": "message",
            "message": user_msg,
        }, ensure_ascii=False))

        # === Генерация ответа системы (как в main.py) ===
        if text == "стоп игра":
            reply_text = "Игра остановлена. Обнови страницу, чтобы начать заново."
        else:
            data_for_solver = problem_solver.classify_message(text)
            reply_text = problem_solver.ask_message(data_for_solver)
            user.history.append(reply_text)

        reply_time = now_time()
        system_msg = {
            "role": "system",
            "text": reply_text,
            "time": reply_time,
        }
        history.append(system_msg)

        # Отправляем ответ системы
        ws.send(json.dumps({
            "type": "message",
            "message": system_msg,
        }, ensure_ascii=False))


if __name__ == "__main__":
    # Обычный dev-сервер Flask, WebSocket работает через flask-sock + simple-websocket
    app.run(host="127.0.0.1", port=8000, debug=True)
