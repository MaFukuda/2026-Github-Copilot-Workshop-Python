# フロントエンドドキュメント

> 最終更新: 2026-04-17  
> 対象バージョン: Phase 1（静的UI）

## 現在の実装状態

**Phase 1 ではフロントエンドは静的UIのみ実装済み。**  
JavaScript によるタイマーロジックは **Phase 2** で実装予定。

---

## ファイル構成

```
static/
  css/
    styles.css     # UIスタイルシート（実装済み）
  js/
    app.js         # フロントエンドエントリーポイント（スケルトン）
templates/
  index.html       # メインページテンプレート（実装済み）
```

---

## HTMLテンプレート（`templates/index.html`）

Jinja2 テンプレート。Flask の `render_template('index.html')` で配信される。

### 主要セクション

| セクション | CSSクラス | 説明 |
|---|---|---|
| コンテナ | `.container` | 画面全体のフレックスコンテナ |
| カード | `.card` | UIカード（最大幅 450px） |
| ヘッダー | `.header` | タイトル + ウィンドウコントロールボタン |
| ステータス | `.status` | 現在の状態テキスト（「作業中」）|
| タイマーセクション | `.timer-section` | 円形プログレスバー + 時間表示 |
| ボタングループ | `.button-group` | 開始・リセットボタン |
| 進捗カード | `.progress-card` | 今日の進捗（完了数・集中時間） |

### 静的ファイルの参照

Jinja2 の `url_for` を使って静的ファイルを参照している。

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
<script src="{{ url_for('static', filename='js/app.js') }}"></script>
```

---

## スタイルシート（`static/css/styles.css`）

### カラースキーム

| 用途 | カラーコード |
|---|---|
| プライマリカラー（紫） | `#6B5B95` |
| プライマリホバー | `#5A4A84` |
| 背景グラデーション | `linear-gradient(135deg, #6B5B95, #8B7BB8)` |
| カード背景 | `#FFFFFF` |
| テキスト（濃） | `#2C2C2C` |
| テキスト（薄） | `#999999` |
| 進捗カード背景 | `linear-gradient(135deg, #F0E8FF, #F5F0FF)` |

### 主要コンポーネント

#### 円形プログレスバー

SVG の `stroke-dasharray` / `stroke-dashoffset` を使用して円形プログレスを表現。

| CSSクラス | 役割 |
|---|---|
| `.circular-progress` | SVG要素、`rotate(-90deg)` で12時方向を起点に設定 |
| `.progress-bg` | 背景の円（`#E8E8E8`）|
| `.progress-bar` | プログレス円（`#6B5B95`）|

プログレスバーの計算値:
- 半径 `r=45`、円周 = `2π × 45 ≈ 282.7`（`stroke-dasharray: 282.7`）
- Phase 1 初期表示は `stroke-dashoffset: 70.67`（75% 進捗状態）

#### ボタン

| CSSクラス | 説明 |
|---|---|
| `.btn` | 共通ボタンスタイル（角丸 25px、最小幅 120px） |
| `.btn-primary` | 開始ボタン（紫背景・白テキスト） |
| `.btn-secondary` | リセットボタン（白背景・紫ボーダー） |

#### レスポンシブ対応

`@media (max-width: 480px)` ブレークポイントで以下を調整:

- カードパディングを縮小
- タイトルフォントサイズを 20px → 18px
- 時間表示を 56px → 48px
- タイマーセクションを 220px → 180px
- ボタン最小幅を 120px → 100px

---

## JavaScript（`static/js/app.js`）

**Phase 1 ではスケルトンのみ（コメントのみ記述）。**

```javascript
// Pomodoro Timer フロントエンドメイン
// Phase 1では静的UIのみ実装
```

### Phase 2 で実装予定のモジュール構成

`architecture.md` および `plan.md` に基づく予定構成:

| ファイル | 役割 |
|---|---|
| `core/timer_state_machine.js` | 有限状態機械（FSM）: `idle / running_work / running_break / paused` |
| `core/progress_calculator.js` | 残り時間計算（終了予定時刻 − 現在時刻方式） |
| `core/session_policy.js` | 作業→休憩遷移ルール |
| `adapters/browser_clock.js` | 現在時刻の取得（副作用隔離） |
| `adapters/browser_scheduler.js` | 定期実行スケジューリング（副作用隔離） |
| `adapters/api_client.js` | Fetch APIラッパー（Phase 4） |
| `ui/renderer.js` | DOM更新 |
| `ui/controller.js` | イベントバインド |
| `app.js` | モジュールの組み上げ |

---

## テスト

フロントエンド関連のテストは `tests/unit/frontend/test_ui.py` に記述されており、Python/pytest で実行される（HTMLレスポンスの検証）。

| テストクラス | 検証内容 |
|---|---|
| `TestUIElements` | UIセクション・CSS クラスの存在確認 |
| `TestCSSStyles` | CSS の特定プロパティ（Flexbox・グラデーション・メディアクエリ等）の存在確認 |
| `TestJavaScript` | `app.js` にコメントが含まれるかの確認 |
| `TestResponsiveness` | ビューポートメタタグ・`max-width` の存在確認 |
