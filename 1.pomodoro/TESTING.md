# ポモドーロタイマー - ユニットテストガイド

## 概要

このプロジェクトのユニットテストは **pytest** フレームワークで実装されています。

## テスト構造

```
tests/
├── conftest.py              # pytest フィクスチャ定義
├── unit/
│   ├── backend/
│   │   └── test_routes.py   # Flask ルート・HTML レスポンステスト（20個）
│   └── frontend/
│       └── test_ui.py       # UIコンポーネント・CSSテスト（17個）
```

## テスト分類

### バックエンド (tests/unit/backend/test_routes.py)

#### TestIndexRoute (10個のテスト)
- GET / が 200 を返すか
- HTML が正しく返されるか
- ページタイトル、ステータス、タイマー表示の確認
- ボタンと進捗カードの要素確認

#### TestStaticFiles (4個のテスト)
- CSS ファイルが正常にロードされるか
- JavaScript ファイルが正常にロードされるか
- CSS に紫系カラー (#6B5B95) が含まれているか
- JavaScript ファイルがコンテンツを持つか

#### TestHTMLStructure (5個のテスト)
- HTML が正しい DOCTYPE と lang 属性を持つか
- UTF-8 charset が指定されているか
- viewport メタタグがあるか
- CSS・JS ファイルが正しくリンクされているか

#### TestNotFound (1個のテスト)
- 存在しないルートが 404 を返すか

### フロントエンド (tests/unit/frontend/test_ui.py)

#### TestUIElements (8個のテスト)
- カードコンテナ、ヘッダー、タイマーセクションの存在確認
- ボタングループ、プライマリ/セカンダリボタンの存在確認
- 進捗カードの数値と時間要素の確認

#### TestCSSStyles (6個のテスト)
- Flexbox の使用確認
- グラデーション背景の確認
- ボーダーラディウス、トランジション効果の確認
- レスポンシブデザイン（メディアクエリ）の確認
- 円形プログレスバースタイルの確認

#### TestJavaScript (1個のテスト)
- JavaScript ファイルが有効な基本構造を持つか

#### TestResponsiveness (2個のテスト)
- viewport が正しく設定されているか
- カードが最大幅を持つか（レスポンシブ対応）

## テスト実行方法

### すべてのテストを実行

```bash
cd /workspaces/2026-Github-Copilot-Workshop-Python/1.pomodoro
/workspaces/2026-Github-Copilot-Workshop-Python/.venv/bin/python -m pytest tests -v
```

### 特定のテストクラスを実行

```bash
# バックエンドテストのみ
/workspaces/2026-Github-Copilot-Workshop-Python/.venv/bin/python -m pytest tests/unit/backend/ -v

# フロントエンドテストのみ
/workspaces/2026-Github-Copilot-Workshop-Python/.venv/bin/python -m pytest tests/unit/frontend/ -v
```

### 特定のテスト関数を実行

```bash
/workspaces/2026-Github-Copilot-Workshop-Python/.venv/bin/python -m pytest tests/unit/backend/test_routes.py::TestIndexRoute::test_index_returns_200 -v
```

### カバレッジレポート付きで実行

```bash
/workspaces/2026-Github-Copilot-Workshop-Python/.venv/bin/python -m pytest tests -v --cov=pomodoro --cov-report=html
```

HTML レポートが `htmlcov/index.html` に生成されます。

## テスト設定 (pytest.ini)

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v                          # 詳細出力
    --strict-markers            # マーカー厳密チェック
    --tb=short                  # 短いトレースバック
    --cov=pomodoro              # カバレッジ計測
    --cov-report=html           # HTML レポート生成
    --cov-report=term-missing   # ターミナルに未カバー行表示
```

## フィクスチャ (conftest.py)

Flask アプリケーション用のフィクスチャが定義されています：

- `app`: Flask テスト設定済みアプリケーション
- `client`: Flask テスト用クライアント（HTTP リクエスト送信用）
- `runner`: Flask CLI テスト用ランナー

```python
@pytest.fixture
def client(app):
    """Flask テスト用クライアント"""
    return app.test_client()
```

## テスト戦略（Phase 1 時点）

### 実装済み
- ✅ ルートとテンプレートレンダリングテスト
- ✅ 静的ファイル（CSS・JS）ロードテスト
- ✅ HTML 構造・メタタグテスト
- ✅ UI エレメント存在確認テスト
- ✅ CSS スタイル内容テスト

### 今後の追加（Phase 2 以降）
- タイマー FSM の状態遷移テスト
- 残り時間計算ロジックのテスト
- API エンドポイントテスト
- セッション記録・進捗計算のテスト

## テスト実行結果例

```
================================ test session starts ================================
collected 37 items

tests/unit/backend/test_routes.py::TestIndexRoute::test_index_returns_200 PASSED
tests/unit/backend/test_routes.py::TestIndexRoute::test_index_returns_html PASSED
...
tests/unit/frontend/test_ui.py::TestResponsiveness::test_card_has_max_width PASSED

================================ 37 passed in 0.28s ================================
```

## トラブルシューティング

### テスト実行で Flask アプリが見つからない場合
- `conftest.py` のパス設定を確認
- `app.py` が `/workspaces/2026-Github-Copilot-Workshop-Python/1.pomodoro/` に存在することを確認

### カバレッジレポートが生成されない場合
- `pytest-cov` パッケージがインストールされているか確認
- `pytest.ini` の `addopts` セクションを確認
