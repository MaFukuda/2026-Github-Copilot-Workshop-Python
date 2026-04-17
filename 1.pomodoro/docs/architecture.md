# アーキテクチャ概要

> 最終更新: 2026-04-17  
> 対象バージョン: Phase 1（静的UI）

## 1. 現在の実装状態

本ドキュメントは **Phase 1（静的UI）** の実際の実装を反映している。  
タイマーロジック・バックエンドAPI・データベースはまだ実装されていない。

## 2. 全体構成

```
1.pomodoro/
  app.py                  # Flask アプリケーションエントリーポイント
  pomodoro/
    __init__.py           # パッケージ初期化（空）
  templates/
    index.html            # メインページテンプレート
  static/
    css/
      styles.css          # UIスタイルシート
    js/
      app.js              # フロントエンドエントリーポイント（スケルトンのみ）
  tests/
    conftest.py           # Pytest フィクスチャ定義
    unit/
      backend/
        test_routes.py    # Flaskルート・HTMLレスポンステスト
      frontend/
        test_ui.py        # UIコンポーネント・CSSテスト
```

## 3. レイヤー構成

### 3.1 サーバー層（Flask）

- `app.py` がアプリケーションのエントリーポイント
- `GET /` の1ルートのみ実装済み
- `render_template('index.html')` で静的HTMLを返却

```python
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
```

### 3.2 プレゼンテーション層（HTML/CSS）

- `templates/index.html`: タイマーUI・ボタン・進捗カードの静的レイアウト
- `static/css/styles.css`: 紫系カラースキーム・フレックスボックス・レスポンシブデザイン

### 3.3 フロントエンド層（JavaScript）

- `static/js/app.js`: Phase 1ではスケルトン（コメントのみ）
- タイマーロジックは **Phase 2** で実装予定

## 4. 未実装の層（将来実装予定）

| 層 | 内容 | フェーズ |
|---|---|---|
| バックエンドAPI | REST APIエンドポイント群 | Phase 3 |
| アプリケーション層 | ユースケース（UseCase） | Phase 3 |
| ドメイン層 | エンティティ定義 | Phase 3 |
| インフラ層 | SQLite・リポジトリ実装 | Phase 3 |
| フロントタイマー | FSM・残り時間計算 | Phase 2 |
| API連携 | fetch による進捗取得・セッション記録 | Phase 4 |

## 5. 技術スタック

| 種別 | 技術 |
|---|---|
| Webフレームワーク | Flask |
| テンプレートエンジン | Jinja2 |
| スタイリング | CSS3（Flexbox・SVG・メディアクエリ） |
| JavaScript | Vanilla JS（Phase 1はスケルトン） |
| テスト | pytest |

## 6. 設定

| 設定項目 | 値 | 設定方法 |
|---|---|---|
| デバッグモード | 環境変数 `FLASK_DEBUG` が `1/true/yes/on` のとき有効 | 環境変数 |
| ホスト | `0.0.0.0` | コード固定 |
| ポート | `5000` | コード固定 |

## 7. テスト実行

```bash
cd 1.pomodoro
pytest
```

pytest 設定は `pytest.ini` を参照。
