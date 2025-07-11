# Transcript Minutes API

トランスクリプトから議事録を自動生成するAPIシステム

## 概要

このAPIは音声トランスクリプトファイルをアップロードし、OpenAI APIを使用して自動的に議事録を生成する機能を提供します。

## 主要機能

- **ユーザー認証**: JWT認証によるセキュアなユーザー管理
- **トランスクリプト処理**: txt/jsonファイルのアップロードと前処理
- **議事録自動生成**: OpenAI GPT-4を使用した高品質な議事録作成
- **構造化ログ**: 詳細な操作履歴とエラー追跡
- **RESTful API**: 標準的なHTTP APIエンドポイント

## 技術スタック

- **フレームワーク**: FastAPI
- **データベース**: PostgreSQL (開発時はSQLite)
- **認証**: JWT (PyJWT)
- **AI**: OpenAI API (GPT-4)
- **ログ**: structlog
- **環境管理**: python-dotenv

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

```bash
cp .env.example .env
```

`.env`ファイルを編集して必要な設定を行ってください：

```env
# データベース
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# JWT設定
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30

# OpenAI API
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4

# ログ設定
LOG_LEVEL=INFO
LOG_FILE_PATH=./logs/app.log

# アプリケーション設定
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=False
```

### 3. データベースの初期化

アプリケーション起動時に自動的にテーブルが作成されます。

### 4. アプリケーションの起動

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
Content-Type: application/json

{
  "user_id": "string",
  "password": "string"
}
```

#### ログイン
```
POST /auth/login
Content-Type: application/json

{
  "user_id": "string",
  "password": "string"
}
```

### トランスクリプト

#### ファイルアップロード
```
POST /transcript/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <transcript_file>
```

#### トランスクリプト一覧取得
```
GET /transcript/list
Authorization: Bearer <token>
```

#### トランスクリプト詳細取得
```
GET /transcript/{transcript_id}
Authorization: Bearer <token>
```

### 議事録

#### 議事録生成
```
POST /minutes/generate
Authorization: Bearer <token>
Content-Type: application/json

{
  "transcript_id": 1
}
```

#### 議事録一覧取得
```
GET /minutes/list
Authorization: Bearer <token>
```

#### 議事録詳細取得
```
GET /minutes/{minutes_id}
Authorization: Bearer <token>
```

## ファイル形式

### サポートされるトランスクリプトファイル

- **テキストファイル (.txt)**: プレーンテキスト形式
- **JSONファイル (.json)**: 以下のキーをサポート
  - `transcript`
  - `text`
  - `content`

### ファイルサイズ制限

- 最大ファイルサイズ: 10MB

## ログ

アプリケーションは構造化ログ（JSON形式）を出力します：

- ファイル出力: `./logs/app.log`
- コンソール出力: 標準出力
- ログレベル: DEBUG, INFO, WARNING, ERROR

## セキュリティ

- パスワードはbcryptでハッシュ化
- JWTトークンによる認証
- CORS設定済み
- ファイルアップロードサイズ制限

## 開発

### テスト実行

```bash
pytest
```

### ログレベル変更

`.env`ファイルの`LOG_LEVEL`を変更してください。

## トラブルシューティング

### よくある問題

1. **OpenAI API エラー**
   - API キーが正しく設定されているか確認
   - API使用量制限を確認

2. **データベース接続エラー**
   - DATABASE_URLが正しく設定されているか確認
   - データベースサーバーが起動しているか確認

3. **ファイルアップロードエラー**
   - ファイル形式がサポートされているか確認
   - ファイルサイズが制限内か確認

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
