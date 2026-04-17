# データモデル仕様

> 最終更新: 2026-04-17  
> 対象バージョン: Phase 1（静的UI）

## 現在の実装状態

**Phase 1 ではデータモデル・データベースは実装されていない。**  
進捗カードに表示されているデータ（完了数: `4`、集中時間: `1時間40分`）は HTML にハードコードされたダミーデータである。

---

## 将来実装予定のデータモデル（Phase 3）

以下のデータモデルは `architecture.md` の設計に基づき Phase 3 で SQLite に実装予定。

### sessions テーブル

ポモドーロセッションの完了記録を保持する。

| カラム名 | 型 | 説明 |
|---|---|---|
| `id` | INTEGER PRIMARY KEY | 自動採番ID |
| `started_at` | DATETIME | セッション開始時刻 |
| `ended_at` | DATETIME | セッション終了時刻 |
| `session_type` | TEXT | セッション種別: `work` / `short_break` / `long_break` |
| `completed` | BOOLEAN | 完了フラグ（中断は `false`） |
| `created_at` | DATETIME | レコード作成時刻 |

### settings テーブル

タイマー設定値を保持する（単一ユーザー想定、レコードは1件）。

| カラム名 | 型 | デフォルト値 | 説明 |
|---|---|---|---|
| `id` | INTEGER PRIMARY KEY | `1`（固定） | 単一ユーザー用固定ID |
| `work_minutes` | INTEGER | `25` | 作業セッション時間（分） |
| `short_break_minutes` | INTEGER | `5` | 短い休憩時間（分） |
| `long_break_minutes` | INTEGER | `15` | 長い休憩時間（分） |
| `long_break_interval` | INTEGER | `4` | 長休憩までの作業セッション数 |
| `auto_start_break` | BOOLEAN | `false` | 休憩を自動開始するか |
| `auto_start_work` | BOOLEAN | `false` | 作業セッションを自動開始するか |
| `updated_at` | DATETIME | — | 最終更新時刻 |

---

## リポジトリパターン（Phase 3 設計）

データアクセスはリポジトリパターンで抽象化する予定。

| リポジトリ | 役割 |
|---|---|
| `SessionRepository` | セッション記録の保存・集計クエリ |
| `SettingsRepository` | 設定値の取得・更新 |

各リポジトリはインターフェース（抽象クラス）を持ち、以下の2実装を提供する予定:

- **SQLiteRepository**: 本番用 SQLite 実装
- **InMemoryRepository**: テスト用インメモリ実装
