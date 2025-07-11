# Transcript Minutes API

トランスクリプトから議事録を自動生成するAPIシステム

## 概要

このAPIは音声トランスクリプトファイルをアップロードし、OpenAI GPT-4を使用して自動的に議事録を生成する機能を提供します。

## 主要機能

- **ユーザー認証**: JWT認証によるセキュアなユーザー管理
- **トランスクリプト処理**: テキストファイル・JSONファイルのアップロードと処理
- **議事録生成**: OpenAI GPT-4による自動議事録生成
- **ログ機能**: 構造化ログによる操作履歴管理

## 技術スタック

- **フレームワーク**: FastAPI
- **データベース**: SQLite (開発用) / PostgreSQL (本番用)
- **認証**: JWT (PyJWT)
- **AI**: OpenAI API (GPT-4)
- **ログ**: Python logging + structlog

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env.example`を`.env`にコピーして、必要な値を設定してください：

```bash
cp .env.example .env
```

重要な環境変数：
- `OPENAI_API_KEY`: OpenAI APIキー
- `JWT_SECRET_KEY`: JWT署名用の秘密鍵
- `DATABASE_URL`: データベース接続URL

### 3. アプリケーションの起動

```bash
python main.py
```

または

```bash
uvicorn main:app --reload
```

## API エンドポイント

### 認証

#### ユーザー登録
```
POST /auth/register
```

#### ログイン
```
POST /auth/login
```

### トランスクリプト

#### ファイルアップロード
```
POST /transcript/upload
Authorization: Bearer <token>
```

#### トランスクリプト一覧
```
GET /transcript/list
Authorization: Bearer <token>
```

#### トランスクリプト取得
```
GET /transcript/{transcript_id}
Authorization: Bearer <token>
```

### 議事録

#### 議事録生成
```
POST /minutes/generate
Authorization: Bearer <token>
```

#### 議事録一覧
```
GET /minutes/list
Authorization: Bearer <token>
```

#### 議事録取得
```
GET /minutes/{minutes_id}
Authorization: Bearer <token>
```

## 使用方法

1. **ユーザー登録**: `/auth/register`でアカウントを作成
2. **ログイン**: `/auth/login`でJWTトークンを取得
3. **トランスクリプトアップロード**: `/transcript/upload`でファイルをアップロード
4. **議事録生成**: `/minutes/generate`で議事録を自動生成

## サポートファイル形式

- **テキストファイル** (`.txt`): プレーンテキスト形式
- **JSONファイル** (`.json`): `transcript`, `text`, `content`キーを含むJSON形式

## セキュリティ

- パスワードはbcryptでハッシュ化
- JWT認証による保護されたエンドポイント
- ファイルサイズ制限 (10MB)
- 構造化ログによる監査証跡

## ログ

アプリケーションは構造化ログ（JSON形式）を出力し、以下の情報を記録します：

- API呼び出し履歴
- 認証イベント
- エラー情報
- 処理時間

## 開発

### テスト実行

```bash
pytest
```

### ログ確認

```bash
tail -f logs/app.log
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
