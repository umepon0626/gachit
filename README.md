# gachit

作ってガチで理解するGit = gachit

# 環境構築

`Docker`と`rye`がインストールされている事が前提です。インストールされていない場合は事前にインストールして使えるようにしておいてください。
<!-- TODO: (@umepon0626) dev-containersでDockerだけで動くようにする。 -->

以下のコマンドを打つことで環境構築が可能です。

```sh
rye sync
```

# 動作確認方法

```sh
./.venv/bin/activate
rye sync
gachit
```

# テスト環境

`gachit`を作っている最中に動作確認をしたくなることがあるかもしれません。
しかし、これには注意が必要です。なぜならば`gachit`は`git`と同じで、作業中のファイルを誤って書き換えてしまう可能性があるからです。
そのため、本リポジトリではDockerでテスト環境を用意しています。

テスト環境では`playground`という[リポジトリ](https://github.com/umepon0626/gachit_practice)をcloneしてあり、
`gachit`のリポジトリから完全に分離された環境ですので安心して動作確認を行うことが可能です。
テストを行うためには以下のコマンドを実行します。

```sh
docker compose up
```

もしもテスト環境をもう一度作り直したい場合は以下のコマンドを実行してください。

```sh
docker compose up --build
```

## テスト環境の中のディレクトリ構成

テスト環境の中のディレクトリ構成は以下のようになっています。

```plain-text
workspace
├── gachit 
└── playground
```
