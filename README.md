# Pythonのロギング検証環境

## 実行方法

まずはこのリポジトリをクローンする。

```bash
git clone https://github.com/temp493/python-logging.git
cd python-logging/
```

`/app/.env`を用意する。
メール送信用のハンドラで用いるデータを定義する。

```ini:/app/.env
from_gmail="example@gmail.com"
google_app_pw="google_top_secret_password"
to_email="example@example.com"
```

次に、下のコマンドを実行する。

```bash
docker-compose up -d
docker-compose exec app bash
python /app/main.py
```

## 実現したいこと

`/app/module.py`で共通のロガーのモデルを作り、`/app/source/script1.py`, `/app/source/script2.py`から利用する。

その際、

* コンソールにはINFO以上
* ログファイルにはDEBUG以上
* メールにはWARNING以上

の出力をしたい。

ただし、グローバルな名前空間を汚さないような方法が望ましい。

## 試したこと

ハンドラの設定でbasicConfigを上書きできないので、仕方なく、`module.py`78行目あたりで`logging.basicConfig(level=logging.NOTSET)`とした。
これで、より高レベルの設定を上書きできるらしく、上記の出力を得られた。

## 問題点

### 1.コンソールでの出力

コンソールでは次のような出力となった。

```log
DEBUG:source.script1:debug
2021-05-22 03:23:37,253 [INFO] (script1.py | main | 8) info
INFO:source.script1:info
2021-05-22 03:23:37,254 [WARNING] (script1.py | main | 9) warning
WARNING:source.script1:warning
DEBUG:source.script2:debug
2021-05-22 03:23:39,832 [INFO] (script2.py | main | 8) info
INFO:source.script2:info
2021-05-22 03:23:39,832 [WARNING] (script2.py | main | 9) warning
WARNING:source.script2:warning
```

欲しかった出力は下記。

```log
2021-05-22 03:23:37,253 [INFO] (script1.py | main | 8) info
2021-05-22 03:23:37,254 [WARNING] (script1.py | main | 9) warning
2021-05-22 03:23:39,832 [INFO] (script2.py | main | 8) info
2021-05-22 03:23:39,832 [WARNING] (script2.py | main | 9) warning
```

loggingのもとの設定でなぜか出力されてしまう。

### 2.ライブラリからのログ出力

いい例が見つからず、今回は再現できなかったが、実際にはライブラリから出力されてくるログも一緒に表示されてしまう。
(`logging.basicConfig`を触ってしまったからか？)
