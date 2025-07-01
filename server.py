from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO
from datetime import datetime, timezone, timedelta  # ✅ 加入 timedelta

import sys
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')  # 控制介面

@app.route('/control', methods=['POST'])
def control():
    data = request.json
    command = data.get('command')
    client_time_str = data.get('client_time')  # ✅ 手機端送出的時間

    # 取得 server 端 UTC 時間
    server_time = datetime.now(timezone.utc)

    # 計算延遲
    delay_ms = None
    if client_time_str:
        try:
            # 將 Z 結尾轉成 timezone-aware datetime
            client_time = datetime.fromisoformat(client_time_str.replace('Z', '+00:00'))
            delay = server_time - client_time
            delay_ms = round(delay.total_seconds() * 1000, 3)  # 毫秒
        except Exception as e:
            print("⚠️ 無法解析 client_time:", e, file=sys.stderr)

    # 台灣時間（+08:00）
    taiwan_tz = timezone(timedelta(hours=8))
    taiwan_str = server_time.astimezone(taiwan_tz).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    # 印出 log
    print("📲 手機送出指令：", data, file=sys.stderr)
    if client_time_str:
        print("📡 client_time（手機）：", client_time_str, file=sys.stderr)
    print("🕒 server_time（接收）：", server_time.isoformat(), file=sys.stderr)
    print("🕒 台灣時間：", taiwan_str, file=sys.stderr)
    if delay_ms is not None:
        print(f"⏱ 指令延遲：{delay_ms} ms", file=sys.stderr)

    # 發送到 WebSocket client
    socketio.emit('control', data)

    return jsonify({
        'status': 'ok',
        'received_command': command,
        'client_time': client_time_str,
        'server_time_utc': server_time.isoformat(),
        'server_time_taiwan': taiwan_str,
        'delay_ms': delay_ms
    })

@app.before_request
def log_request_info():
    print(f"Request: {request.method} {request.path}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # ✅ for Render
    socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)

