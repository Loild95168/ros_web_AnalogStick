import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from datetime import datetime, timezone
import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return render_template("index.html")  # 提供前端頁面

# 👉 Web client 發送指令
@socketio.on("control")
def handle_control(data):
    print("📲 手機送出指令：", data)
    socketio.emit("control", data, namespace="/ros")  # 廣播給 ROS 主機

# 👉 提供 ROS 主機連線的 socket namespace
@socketio.on("connect", namespace="/ros")
def on_ros_connect():
    print("✅ ROS 主機已連線")

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)

