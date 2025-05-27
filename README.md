[![test](https://github.com/ks6088ts-labs/template-streamlit/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/ks6088ts-labs/template-streamlit/actions/workflows/test.yaml?query=branch%3Amain)
[![docker](https://github.com/ks6088ts-labs/template-streamlit/actions/workflows/docker.yaml/badge.svg?branch=main)](https://github.com/ks6088ts-labs/template-streamlit/actions/workflows/docker.yaml?query=branch%3Amain)
[![docker-release](https://github.com/ks6088ts-labs/template-streamlit/actions/workflows/docker-release.yaml/badge.svg)](https://github.com/ks6088ts-labs/template-streamlit/actions/workflows/docker-release.yaml)
[![ghcr-release](https://github.com/ks6088ts-labs/template-streamlit/actions/workflows/ghcr-release.yaml/badge.svg)](https://github.com/ks6088ts-labs/template-streamlit/actions/workflows/ghcr-release.yaml)
[![docs](https://github.com/ks6088ts-labs/template-streamlit/actions/workflows/github-pages.yaml/badge.svg)](https://github.com/ks6088ts-labs/template-streamlit/actions/workflows/github-pages.yaml)

# template-streamlit

## 概要 (Overview)

`template-streamlit`は、[Streamlit](https://streamlit.io/)アプリケーションの開発に必要な基本構造とツールを提供するテンプレートリポジトリです。このテンプレートを使用することで、AI機能を持つWebアプリケーションを迅速に開発・デプロイすることができます。

This template repository provides the basic structure and tools needed for developing [Streamlit](https://streamlit.io/) applications. By using this template, you can quickly develop and deploy web applications with AI capabilities.

## 特徴と利点 (Features and Benefits)

### 主な特徴 (Key Features)

- **Streamlitフレームワーク**: インタラクティブなWebアプリケーションを短時間で構築
- **LangChainサポート**: AIモデル（Azure OpenAI、Ollama）との連携機能
- **Dockerサポート**: コンテナベースの開発・デプロイが可能
- **テキスト分割プレイグラウンド**: 異なるテキスト分割方法の視覚化
- **環境変数管理**: APIキーなどの機密情報を安全に管理
- **MkDocs統合**: プロジェクトドキュメントの自動生成

### 利点 (Benefits)

- **開発時間の短縮**: 必要なコンポーネントが事前構成済み
- **Makefileによる標準化**: 一貫した開発ワークフロー
- **コンテナ対応**: 環境依存性の問題を削減
- **モジュール構造**: 拡張や機能追加が容易
- **CIパイプライン**: ビルドとテスト自動化の設定済み

## 前提条件 (Prerequisites)

- [Python 3.10+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [GNU Make](https://www.gnu.org/software/make/)
- Docker（Dockerを使用する場合）

## 開発手順 (Development Instructions)

当プロジェクトは`Makefile`を中心とした開発ワークフローを採用しています。主な操作はすべてMakeコマンドから実行できます。

### ヘルプ表示 (View Help)

`Makefile`で定義されているすべてのコマンドを表示するには：

```shell
make
# または
make help
```

### ローカル開発 (Local Development)

#### 依存関係のインストール (Install Dependencies)

```shell
# 開発用依存関係をインストール
make install-deps-dev

# 本番用依存関係のみをインストール
make install-deps
```

#### コードフォーマットとリント (Code Formatting and Linting)

```shell
# コードフォーマットを適用
make format

# 自動修正を適用
make fix

# リントチェック
make lint
```

#### テスト実行 (Run Tests)

```shell
# テストを実行
make test

# CIテストを実行（フォーマットチェック、リント、テスト）
make ci-test
```

#### Streamlitアプリの実行 (Run Streamlit App)

```shell
# Streamlitアプリを起動（ポート8000）
make streamlit
```

実行後、ブラウザで http://localhost:8000 を開くとStreamlitアプリケーションにアクセスできます。

#### その他の開発ツール (Other Development Tools)

```shell
# JupyterLabを起動
make jupyterlab

# ドキュメントをローカルで表示
make docs-serve
```

### Docker開発 (Docker Development)

Dockerを使用して開発環境を構築することもできます。

```shell
# Dockerイメージをビルド
make docker-build

# Dockerコンテナを実行
make docker-run

# DockerでCIテストを実行
make ci-test-docker
```

## Docker使用方法 (Docker Usage)

### 簡単な実行方法 (Quick Start)

Dockerを使ってワンライナーでアプリを実行する：

```shell
docker run --rm -p 8000:8000 ks6088ts/template-streamlit:latest streamlit run main.py --server.port 8000 --server.address 0.0.0.0
```

### 環境変数の設定 (Environment Variables)

環境変数を使用する場合（例：Azure OpenAI APIキー）：

```shell
# .envファイルをコンテナにマウント
docker run --rm \
  -v $(pwd)/.env:/app/.env \
  -p 8000:8000 \
  ks6088ts/template-streamlit:latest
```

`.env`ファイルの例（`.env.template`をコピーして作成）：

```
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2023-07-01-preview
AZURE_OPENAI_GPT_MODEL=your-gpt-deployment
```

### ポート設定 (Port Configuration)

デフォルトでポート8000を使用しますが、ホスト側のポートは変更可能です：

```shell
# ホスト側ポート3000をコンテナの8000にマッピング
docker run --rm \
  -p 3000:8000 \
  ks6088ts/template-streamlit:latest
```

この場合、ブラウザで http://localhost:3000 にアクセスします。

### トラブルシューティング (Troubleshooting)

- **コンテナが起動しない場合**: ポートが既に使用されていないか確認してください
- **環境変数が読み込まれない場合**: `.env`ファイルのパスが正しいか確認してください
- **APIエラー**: `.env`ファイル内のAPIキーや設定を確認してください

## デプロイ手順 (Deployment Instructions)

### Docker Hub

Docker Hubにイメージを公開するには、[アクセストークンを作成](https://app.docker.com/settings/personal-access-tokens/create)し、リポジトリの設定に以下のシークレットを設定する必要があります。

```shell
gh secret set DOCKERHUB_USERNAME --body $DOCKERHUB_USERNAME
gh secret set DOCKERHUB_TOKEN --body $DOCKERHUB_TOKEN
```
