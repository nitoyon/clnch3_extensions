#coding:utf-8

"""
雑多なコマンドを定義します

コマンド：
  ・command_OpenExploer
    第一引数のフォルダをエクスプローラーで開きます。

関数：
  ・addAlias
    コマンドの別名を登録します。

定義例：
    # config.py に次のように記載します

    import misc
    #reload(misc)

    # cls コマンドを登録する
    window.launcher.command_list += [ ( u"cls", misc.command_ClearConsole ) ]

    # Google コマンドを g で使えるようにする
    misc.addAlias( window, u"Google", u"g" )

"""

import os
from clnch import *

# --------------------------------------------------------------------
# "clear" コマンド
#   コンソールを消去します。
def command_ClearConsole(window):
    def _command_ClearConsole(args):
        window.console_window.clearLog()
        print "Done"

    return _command_ClearConsole


# --------------------------------------------------------------------
# "addAlias" 関数
#   同じ処理を行う新しいコマンドを登録します。
#
# 引数:
# - window:
#     メインウインドウ オブジェクト。
# - originalName:
#      元の名前。
# - newName:
#      新しい名前
def addAlias(window, originalName, newName):
    cmd = filter(lambda x: x[0] == originalName, window.launcher.command_list)
    if len(cmd) == 0:
        raise Exception("Command not found: %s" % originalName)

    window.launcher.command_list += [( newName, cmd[0][1] )]
