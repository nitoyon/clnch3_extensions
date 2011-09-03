#coding:utf-8

"""
フォルダを開くコマンド群

コマンド：
  ・command_OpenExplorer
    第一引数のフォルダをエクスプローラーで開きます。

  ・command_OpenCommandPrompt
    第一引数のフォルダをコマンド プロンプトで開きます。

  ・command_EditCommand
    第一引数のコマンドを編集します。


定義例：
    # config.py に次のように記載します

    import open_folder
    #reload(open_folder)
    window.cmd_keymap[ KeyEvent( VK_RETURN, MODKEY_SHIFT ) ] = open_folder.command_OpenExplorer
    window.cmd_keymap[ KeyEvent( VK_RETURN, MODKEY_CTRL  ) ] = open_folder.command_OpenCommandPrompt
    window.cmd_keymap[ KeyEvent( VK_RETURN, MODKEY_ALT   ) ] = open_folder.command_EditCommand(window)


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
            shellExecute( None, None, u"explorer.exe", u'/select,"%s"' % path, u"" )
        elif os.path.isdir(path):
            shellExecute( None, None, path, u"", u"" )
        else:
            shellExecute( None, None, os.path.split(path)[0], u"", u"" )

# --------------------------------------------------------------------
# コマンドのフォルダーをコマンド プロンプトで表示する
def command_OpenCommandPrompt(args):
    path = getCommandPath(args[0])
    if path:
        if os.path.isdir(path):
            shellExecute( None, None, "cmd.exe", u"", path )
        else:
            shellExecute( None, None, u"cmd.exe", u"", os.path.split(path)[0] )

# --------------------------------------------------------------------
# コマンドを編集する
def command_EditCommand(window):
    def _command_EditCommand(args):
        command_name = args[0].lower()

        items = loadCommandListFromIniFile()
        i = 0
        for i in xrange(len(items)):
            if command_name == items[i][0].lower():
                # 編集ウインドウを表示する
                edit_result = clnch_commandwindow.popCommandWindow( window, *items[i] )

                # 編集した場合
                if edit_result:
                    items[i] = edit_result

                    # iniファイルに反映させる
                    clnch_ini.remove_section("COMMANDLIST")
                    for i in xrange(len(items)):
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
            command_string = unicode( clnch_ini.get( "COMMANDLIST", "command_%d"%(i,) ), "utf8" )
        except:
            break

        ret.append(eval( command_string ))
        i += 1
    return ret
