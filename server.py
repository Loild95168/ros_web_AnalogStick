import eventlet
eventlet.monkey_patch()  # ✅ 必須放在最上面！

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from datetime import datetime, timezone

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")  # ✅ 明確指定 async_mode

@app.route("/")
def index():
    return render_template("index.html")  # 提供前端頁面

# 👉 網頁控制按鈕：前進、後退、停止等
@socketio.on("control")
def handle_control(data):
    print("📲 手機送出指令：", data)
    socketio.emit("control", data, namespace="/ros")  # 廣播給 ROS 主機

# 👉 類比搖桿控制事件
@socketio.on("analog_control")
def handle_analog_control(data):
    print("🎮 類比搖桿控制：", data)
    socketio.emit("analog_control", data, namespace="/ros")  # 廣播給 ROS 主機

# 👉 ROS 主機連線確認
@socketio.on("connect", namespace="/ros")
def on_ros_connect():
    print("✅ ROS 主機已連線")

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)

