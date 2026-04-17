# Webアプリケーションアーキテクチャ案（Pomodoro Timer）

## 1. 目的と前提

本ドキュメントは、Flask + HTML/CSS/JavaScriptで実装するポモドーロタイマーのアーキテクチャ方針を定義する。

前提:
- 単一ユーザー利用を初期スコープとする。
- UIは添付モックをベースに実装する。
- 初期リリースはシンプルさを優先しつつ、将来拡張可能な構成にする。
- ユニットテスト容易性を重要要件とする。

## 2. 全体方針

- サーバー(Flask): 画面配信とデータAPIに責務を限定する。
- クライアント(JavaScript): タイマー進行・画面更新を担当する。
- 永続化(SQLite): 完了セッションと設定値を保存する。

狙い:
- UXに直結するタイマー更新をクライアントで高速に実現する。
- サーバーは集計と保存に集中し、構造を単純化する。
- 将来的に認証や同期機能を追加しやすくする。

## 3. レイヤー構成

### 3.1 プレゼンテーション層

- Flaskテンプレートで初期HTMLを返却
- CSSでUIモックを再現
- JavaScriptで以下を制御
  - 残り時間表示
  - 円形プログレス表示
  - ステータス文言
  - 開始/停止/リセット操作
  - 今日の進捗カード

### 3.2 アプリケーション層

- セッション完了記録
- 今日の進捗集計
- 設定値の取得/更新

### 3.3 永続化層

- SQLiteを使用
- リポジトリパターンでDBアクセスを隠蔽

## 4. 推奨ディレクトリ構成

```text
1.pomodoro/
  app.py
  pomodoro/
    __init__.py
    routes/
      web.py
      api.py
    application/
      usecases/
        get_today_summary.py
        record_session_complete.py
        get_settings.py
        update_settings.py
    domain/
      entities.py
      services.py
    infrastructure/
      db.py
      repositories/
        session_repository.py
        settings_repository.py
  templates/
    index.html
  static/
    css/
      styles.css
    js/
      core/
        timer_state_machine.js
        progress_calculator.js
        session_policy.js
      adapters/
        browser_clock.js
        browser_scheduler.js
        api_client.js
      ui/
        renderer.js
        controller.js
      app.js
  tests/
    unit/
      backend/
      frontend/
    integration/
      api/
```

補足:
- 既存の`1.pomodoro/app.py`はエントリーポイントとして残し、内部実装を分割する。
- 初期段階では必要最小限のファイルから開始し、段階的に分離する。

## 5. フロントエンド設計（テスト容易性重視）

### 5.1 重要原則

- タイマーのコアロジックは純粋関数に寄せる。
- 副作用(UI更新、通知、HTTP通信、setInterval)はアダプタ層へ隔離する。
- 状態管理は有限状態機械(FSM)で明示する。

状態例:
- idle
- running_work
- running_break
- paused

### 5.2 タイマー計算

残り時間は「1秒デクリメント」ではなく、以下で算出する。
- 終了予定時刻 - 現在時刻

これにより、タブ非アクティブ時や描画遅延時のドリフトを抑制できる。

### 5.3 依存性注入

以下を直接参照せず注入する。
- Clock（現在時刻提供）
- Scheduler（定期実行）
- ApiClient（通信）

効果:
- フェイクClock/フェイクSchedulerで安定したユニットテストが可能。

## 6. バックエンド設計（Flask）

### 6.1 ルートは薄く保つ

ルート層は以下のみ実施:
- 入力をDTOへ変換
- UseCase呼び出し
- レスポンス整形

業務ロジックはUseCase/Serviceへ委譲する。

### 6.2 リポジトリ境界

UseCaseは抽象リポジトリに依存し、実体は差し替え可能にする。
- 本番: SQLiteRepository
- テスト: InMemoryRepository

### 6.3 API契約（最小）

- GET /api/today-summary
  - 返却: 完了ポモドーロ数、合計集中時間(分)
- POST /api/sessions/complete
  - 入力: セッション種別、開始/終了時刻、完了フラグ
- GET /api/settings
  - 返却: 作業分、休憩分、長休憩分、長休憩までの回数、自動切替有無
- PUT /api/settings
  - 入力: 設定値一式

## 7. データモデル（初期案）

### 7.1 sessions

- id (PK)
- started_at (datetime)
- ended_at (datetime)
- session_type (text: work | short_break | long_break)
- completed (boolean)
- created_at (datetime)

### 7.2 settings

- id (PK, 単一ユーザーなら固定1)
- work_minutes (int)
- short_break_minutes (int)
- long_break_minutes (int)
- long_break_interval (int)
- auto_start_break (boolean)
- auto_start_work (boolean)
- updated_at (datetime)

## 8. テスト戦略

## 8.1 ユニットテスト（最優先）

フロントエンド:
- 状態遷移(FSM)のテスト
- 残り時間計算の境界値テスト
- 一時停止/再開/完了イベントのテスト

バックエンド:
- UseCase単体テスト（InMemoryRepository使用）
- 集計ロジック（日付跨ぎ、未完了除外）の境界値テスト
- 設定値バリデーションテスト

## 8.2 APIテスト

- Flask test clientで正常系/異常系を最小限カバー
- 契約破壊がないかを検証

## 8.3 最小E2E

- 開始 -> 完了 -> 今日の進捗反映 の1シナリオを自動化

## 9. 実装ステップ

1. 静的UI（HTML/CSS）をモック準拠で構築
2. フロント単体でタイマー挙動(FSM + 残り時間計算)を実装
3. Flask API（today-summary / sessions/complete / settings）実装
4. UIとAPI連携
5. テスト拡充（unit -> api -> e2e最小）

## 10. 将来拡張の見通し

- マルチユーザー化: 認証導入とsettings/sessionsのユーザー紐付け
- 複数端末同期: サーバー側で現在セッション状態を保持、必要に応じてWebSocket化
- 通知拡張: ブラウザ通知からデスクトップ通知連携へ発展

---

この構成により、初期実装は軽量に保ちながら、ロジックの単体テストを高密度で実施できる。特に「純粋なコアロジック」と「副作用の隔離」を守ることが、保守性と品質を両立する鍵となる。
