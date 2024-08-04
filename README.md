# gachit

作ってガチで理解するGit = gachit

# 環境構築

`Docker`と`rye`がインストールされている事が前提です。インストールされていない場合は事前にインストールして使えるようにしておいてください。

以下のコマンドを打つことで環境構築が可能です。

```sh
rye sync
```

# このリポジトリをクローンしたらやること

1. `mv .git/objects/pack/*.pack .`

2. `cat *.pack | git unpack-objects`

3. `rm *.pack`

# 動作確認方法

```sh
./.venv/bin/activate
rye sync
gachit
```
