from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO
from datetime import datetime, timezone  # ✅ 修正這裡！

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
    print("📲 手機送出指令：", data, file=sys.stderr)

    # 推送指令給 WebSocket Client
    socketio.emit('control', data)

    return jsonify({
        'status': 'ok',
        'received_command': command,
        'server_time': datetime.now(timezone.utc).isoformat()
    })

@app.before_request
def log_request_info():
    print(f"Request: {request.method} {request.path}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # ✅ for Render
    socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)

