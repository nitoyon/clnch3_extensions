#coding:utf-8

r"""
フォルダを開くコマンド群

コマンド：
  ・command_OpenExplorer
    第一引数のフォルダをエクスプローラーで開きます。

  ・command_OpenCommandPrompt
    第一引数のフォルダをコマンド プロンプトで開きます。

  ・command_EditCommand
    第一引数のコマンドを編集します。


定義例：
    # config.py の configure() 関数に次のように記載します

    import open_folder
    window.cmd_keymap[ "S-Return" ] = open_folder.command_OpenExplorer
    window.cmd_keymap[ "C-Return" ] = open_folder.command_OpenCommandPrompt
    window.cmd_keymap[ "A-Return" ] = open_folder.command_EditCommand(window)


使用例：
    ・"memochou" + Shift - Enter
      メモ帳をドラッグ＆ドロップで memochou として登録していれば、
      メモ帳がインストールされたフォルダをエクスプローラーで開く。

    ・"memochou" + Ctrl - Enter
      メモ帳をドラッグ＆ドロップで memochou として登録していれば、
      メモ帳がインストールされたフォルダをコマンド プロンプトで開く。

    ・"memochou" + Alt - Enter
      メモ帳をドラッグ＆ドロップで memochou として登録していれば、
      memochou コマンドを編集する。

    ・"~" + Ctrl - Enter
      マイドキュメントをドラッグ＆ドロップで ~ として登録していれば、
      コマンド プロンプトでマイドキュメント フォルダを開く。

    ・"~" + Alt - Enter
      マイドキュメントをドラッグ＆ドロップで ~ として登録していれば、
      ~ コマンドを編集する。

    ・"C:\Users" + Ctrl - Enter
      C:\Users をコマンド プロンプトを開く。

"""

import os
from clnch import *

# --------------------------------------------------------------------
# コマンドのフォルダーをエクスプローラーで表示する
def command_OpenExplorer(args):
    path = getCommandPath(args[0])
    if path:
        if os.path.isfile(path):
            pyauto.shellExecute( None, "explorer.exe", '/select,"%s"' % path, "", None )
        elif os.path.isdir(path):
            pyauto.shellExecute( None, path, "", "", None )
        else:
            pyauto.shellExecute( None, os.path.split(path)[0], "", "", None )

# --------------------------------------------------------------------
# コマンドのフォルダーをコマンド プロンプトで表示する
def command_OpenCommandPrompt(args):
    path = getCommandPath(args[0])
    if path:
        if os.path.isdir(path):
            pyauto.shellExecute( None, "cmd.exe", "", path, None )
        else:
            pyauto.shellExecute( None, "cmd.exe", "", os.path.split(path)[0], None )

# --------------------------------------------------------------------
# コマンドを編集する
def command_EditCommand(window):
    def _command_EditCommand(args):
        command_name = args[0].lower()

        items = loadCommandListFromIniFile()
        i = 0
        for i in range(len(items)):
            if command_name == items[i][0].lower():
                # 編集ウインドウを表示する
                edit_result = clnch_commandwindow.popCommandWindow( window, *items[i] )

                # 編集した場合
                if edit_result:
                    items[i] = edit_result

                    # iniファイルに反映させる
                    clnch_ini.remove_section("COMMANDLIST")
                    for i in range(len(items)):
                        clnch_ini.set( "COMMANDLIST", "command_%d"%(i,), str(tuple(items[i])) )

                    # 設定を再読み込みする
                    window.configure()
                break
            i += 1

    return _command_EditCommand


# 処理対象のフォルダを取得する
def getCommandPath( text ):

    # ファイルやディレクトリ パスならそのまま返す
    if os.path.isfile(text) or os.path.isdir(text):
        return text

    # ini から取得
    text = text.lower()
    command_list = loadCommandListFromIniFile()
    for command in command_list:
        if text.lower() == command[0].lower():
            return command[1]

# ini に保存されたコマンドを読み込む
def loadCommandListFromIniFile():
    i=0
    ret = []
    while True:
        try:
            command_string = clnch_ini.get( "COMMANDLIST", "command_%d"%(i,) )
        except:
            break

        ret.append(eval( command_string ))
        i += 1
    return ret
