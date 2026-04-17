# API リファレンス

> 最終更新: 2026-04-17  
> 対象バージョン: Phase 1（静的UI）

## 現在の実装状態

**Phase 1 では REST API は実装されていない。**  
実装済みのエンドポイントは以下の1件のみ。

---

## 実装済みエンドポイント

### `GET /`

メインページ（ポモドーロタイマーUI）を返す。

| 項目 | 値 |
|---|---|
| メソッド | `GET` |
| パス | `/` |
| 認証 | 不要 |
| レスポンス形式 | `text/html; charset=utf-8` |

#### レスポンス

| ステータスコード | 説明 |
|---|---|
| `200 OK` | HTMLページを返す |

#### HTMLレスポンスに含まれる要素

| 要素 | CSS クラス / 内容 |
|---|---|
| タイトル | `class="title"` / ポモドーロタイマー |
| ステータス表示 | `class="status"` / 作業中 |
| タイマー表示 | `class="time-display"` / `25:00` |
| 円形プログレスバー | `<svg class="circular-progress">` |
| 開始ボタン | `class="btn btn-primary"` / 開始 |
| リセットボタン | `class="btn btn-secondary"` / リセット |
| 進捗カード | `class="progress-card"` |
| 完了数 | `class="progress-number"` / `4` （ダミーデータ） |
| 集中時間 | `class="progress-time"` / `1時間40分` （ダミーデータ） |
| ウィンドウコントロール | `class="window-controls"` |

---

## 静的ファイルエンドポイント

Flask の静的ファイル配信機能により以下が利用可能。

| パス | 内容 | Content-Type |
|---|---|---|
| `/static/css/styles.css` | UIスタイルシート | `text/css; charset=utf-8` |
| `/static/js/app.js` | フロントエンドスクリプト | `application/javascript` |

---

## 存在しないパスへのアクセス

定義されていないルートへのアクセスは `404 Not Found` を返す。

---

## 将来実装予定のエンドポイント（Phase 3）

以下のAPIは `architecture.md` の設計に基づき Phase 3 で実装予定。

| メソッド | パス | 説明 |
|---|---|---|
| `GET` | `/api/today-summary` | 本日の進捗取得（完了数・累計集中時間） |
| `POST` | `/api/sessions/complete` | セッション完了を記録 |
| `GET` | `/api/settings` | タイマー設定値を取得 |
| `PUT` | `/api/settings` | タイマー設定値を更新 |
