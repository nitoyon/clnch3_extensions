CraftLaunch3 便利プラグイン集

[CraftLaunch3](https://sites.google.com/site/craftware/clnch) v3.30 用の便利プラグイン集。3.30 に対応。


インストール方法
================

1. https://github.com/nitoyon/clnch3_extensions/releases からソースコードを取得します。
2. CraftLaunch のインストールフォルダーにある `extension` フォルダーの中に中身を突っ込みます。(`extension/control_panel.py` となるように設置してください)
3. 各プラグイン冒頭のコメントを参照して、`config.py` を修正します。(`config.py` の場所については CraftLanch のドキュメントを参照してください)


プラグイン一覧
==============

control_panel
-------------

コントロールパネルや管理ツールをコマンド化するプラグインです。


たとえば、次のようにできます。

  * [ネットワーク接続] を開くには `cpl:Network` と入力
  * [イベント ビューワー] を開くには `cpl:EventViewer` と入力

コントロールパネルや管理ツールの各アイテムは日本語版 Windows ではキーボードでアクセスしにくいので、キーボード派の人には便利じゃないでしょうか。

登録されるコマンド一覧は [`control_panel.py`](https://github.com/nitoyon/clnch3_extensions/blob/master/control_panel.py) の `ControlCommandList.__init__()` を参照してください。


misc
----

独立して作るほどではない雑多な機能を実装しています。

次の２つの機能が入っています。

  * `command_ClearConsole` コマンド
    コンソールをクリアします。python_console プラグインの出力を消したいときや、プラグイン開発していて例外メッセージに満ち溢れてきたときに便利。

  * `addAlias` 関数
    コマンドに別名を設定する関数です。control_panel プラグインで便利。


open_folder
-----------

コマンド名を入力して、Ctrl や Shfit と一緒に Enter を押すことで、フォルダーを便利に開けるようになります。また、Alt と一緒に押すと、コマンドの設定を変更できるようになります。

  * Ctrl-Enter: コマンドのインストール フォルダーをコマンドプロンプトで開く。
  * Shift-Enter: コマンドのインストール フォルダーをエクスプローラーで開く。
  * Alt-Enter: コマンドの設定を編集する。


path_plus
---------

登録したコマンドからサブフォルダに移動しやすくなります。

たとえば、マイ ドキュメントを `~` コマンドとして登録してあるときには、次のような利益があります。

  * `~\` でマイドキュメント以下のファイルが補完で現れる
  * `~\memo.txt` でマイドキュメント直下の `memo.txt` を開ける

コマンド名のあとに `\` をつけると、コマンドのフォルダー内のファイルにアクセスできます。

たとえば、CraftLaunch を `CraftLaunch` コマンドとして登録しておけば、`CraftLaunch\readme.txt` で CraftLaunch の readme を表示できます。


python_console
--------------

Python のインタラクティブシェルが使えるようになります。

`>>> ` (`>` を 3 つと、スペース 1 つ) を先頭に入力することで、Python のインタラクティブ シェルと同等の動作をしてくれます。

```python
>>> a = [1,3,5]
>>> a
[1, 3, 5]
>>> for i in a:
...     print i
... 
1
3
5
```

run_as_administrator
--------------------

管理者として実行させたいコマンドを Ctrl-Shift-Enter で実行すると、管理者権限で実行してくれます。Vista 以降で UAC を有効のまま使っている人には便利です。


url_alias
---------

特定の規則に従った URL を開くのが便利になります。

設定例：

  * `@nitoyon` と入力して Enter を押すと `http://twitter.com/nitoyon` を開く
  * `rfc822` と入力して Enter を押すと `http://www.ietf.org/rfc/rfc822.txt` を開く

登録は、`config.py` に次のようにして正規表現で定義します。

```python
# config.py の configure() 関数に次のように記載します

import url_alias
url_alias.register(window, 
                   { 'regex': re.compile('^rfc(\d+)$', re.IGNORECASE), 
                     'url': 'http://www.ietf.org/rfc/rfc%param%.txt' },
                   { 'regex': re.compile('^@(\w+)$'), 
                     'url': 'http://twitter.com/%param%' },
                  )
```


window_command
--------------

指定した exe のウインドウを「最前面・最大化・最小化・元のサイズに戻す・閉じる」といった処理をまとめて実行できます。

たとえば、メモ帳を `notepad` コマンドとして登録している場合、

  * `foreground;notepad` と入力すれば、メモ帳を最前面にできる。
  * `minimize;notepad` と入力すれば、メモ帳を全て最小化できる。
  * `close;notepad` の代わりに `notepad` と入力して Ctrl + [-] でもよい。

のような機能を実現できます。


開発について
============

pull request 大歓迎です。

Git レポジトリー上のファイルの改行コードが CRLF になるようにしています。これは、zip 形式で GitHub からダウンロードして利用することを想定しているためです。そのため、Git の設定で `core.autocrlf` を `false` に設定して作業してください。

