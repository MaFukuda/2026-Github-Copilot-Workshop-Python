"""
Pytest 設定ファイル - フィクスチャの定義
"""

import pytest
import sys
from pathlib import Path

# プロジェクトルートをパスに追加（相対インポート対応）
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app import app as flask_app


@pytest.fixture
def app():
    """Flask アプリケーションのフィクスチャ"""
    flask_app.config['TESTING'] = True
    return flask_app


@pytest.fixture
def client(app):
    """Flask テスト用クライアント"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Flask CLI テスト用ランナー"""
    return app.test_cli_runner()
