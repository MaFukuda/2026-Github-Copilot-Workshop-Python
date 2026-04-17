# ポモドーロタイマー 段階的実装計画

## Phase 1 — 静的UI（土台）
**目標**: モック画像を忠実に再現した動かないHTML/CSS画面を作る

- ディレクトリ構成をリポジトリ直下の `architecture.md` に沿って作成
- `templates/index.html`: タイマー表示・ボタン・今日の進捗カードのレイアウト
- `static/css/styles.css`: 円形プログレス・ボタンデザイン・紫系カラースキーム
- `app.py`: Flaskで `/` を返すだけのルート

**完了基準**: ブラウザで開くとモックと同じ外観が表示される

---

## Phase 2 — フロントタイマーロジック（コアロジック）
**目標**: APIなしでタイマーが動く状態にする

- `static/js/core/timer_state_machine.js`: `idle / running_work / running_break / paused` のFSM（純粋関数）
- `static/js/core/progress_calculator.js`: 残り時間計算（終了予定時刻 − 現在時刻方式）
- `static/js/core/session_policy.js`: 作業→休憩遷移のルール
- `static/js/adapters/browser_clock.js` / `browser_scheduler.js`: 副作用の隔離
- `static/js/ui/renderer.js` / `controller.js`: DOM更新・イベントバインド
- `static/js/app.js`: 組み上げ

**完了基準**: 開始/一時停止/リセットが動き、円形プログレスが更新される

---

## Phase 3 — バックエンドAPI（最小）
**目標**: セッション記録と進捗取得がAPIで動く

- `pomodoro/infrastructure/db.py`: SQLiteセットアップ・マイグレーション
- `pomodoro/infrastructure/repositories/`: `SessionRepository` / `SettingsRepository`（+ InMemory版）
- `pomodoro/domain/entities.py`: `Session` / `Settings` エンティティ
- `pomodoro/application/usecases/`: `RecordSessionComplete` / `GetTodaySummary` / `GetSettings` / `UpdateSettings`
- `pomodoro/routes/api.py`: 4本のAPIエンドポイント実装

**完了基準**: `curl` でセッション記録・進捗取得・設定取得が動作する

---

## Phase 4 — UI と API の連携
**目標**: フロントがAPIを叩いて今日の進捗カードが実データで表示される

- `static/js/adapters/api_client.js`: Fetch APIラッパー
- セッション完了時に `POST /api/sessions/complete` を呼ぶ
- ページロード時に `GET /api/today-summary` と `GET /api/settings` を呼ぶ
- 設定画面（最小限）を追加して `PUT /api/settings` 連携

**完了基準**: 実際にポモドーロを完了すると「今日の進捗」カードの数字が増える

---

## Phase 5 — テストと品質
**目標**: 主要ロジックがテストで保護された状態にする

- `tests/unit/backend/`: UseCase単体テスト（InMemoryRepository使用）
- `tests/unit/frontend/`: FSM遷移・残り時間計算の境界値テスト（Jest等）
- `tests/integration/api/`: Flask test clientによるAPIテスト
- 音声通知・ブラウザタブ非アクティブ対策（既にPhase 2のタイマー方式で軽減済み）
- エラーハンドリング・ロギング追加

**完了基準**: `pytest` と `npm test` が全てパスする

---

## 実装粒度の考え方

| 判断基準 | 理由 |
|---------|------|
| **1フェーズ = 1つの動く成果物** | 途中でも動作確認できる状態を保つ |
| **フロントのコアロジックを先にAPIより実装** | 依存関係なしでテスト・UI検証が進む |
| **FSMと計算ロジックは純粋関数で閉じる** | フェイクClock注入でブラウザ不要のテストが可能 |
| **リポジトリ抽象化を最初から入れる** | Phase 3から差し替え可能なのでPhase 5のテストが楽になる |
