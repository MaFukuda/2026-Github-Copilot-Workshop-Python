"""
ポモドーロタイマー Flask アプリケーション
"""

import os

from flask import Flask, render_template

# Flask アプリの初期化
app = Flask(__name__)


@app.route('/')
def index():
    """ポモドーロタイマーのメインページを返す"""
    return render_template('index.html')


if __name__ == '__main__':
    # 開発サーバーの起動
    debug_mode = os.getenv('FLASK_DEBUG', '').lower() in ('1', 'true', 'yes', 'on')
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
