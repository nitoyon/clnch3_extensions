#coding:utf-8

"""
ウインドウを処理するコマンド群

定義例：
    # config.py の configure() 関数に次のように記載します

    import window_command
    window.cmd_keymap[ "C-L" ] = window_command.command_ForegroundWindow
    window.cmd_keymap[ "C-Minus" ] = window_command.command_CloseWindow
    window.launcher.command_list += [
        ( u"foreground", window_command.command_ForegroundWindow ),
        ( u"close",      window_command.command_CloseWindow ),
        ( u"minimize",   window_command.command_MinimizeWindow ),
        ( u"maximize",   window_command.command_MaximizeWindow ),
        ( u"restore",    window_command.command_RestoreWindow ),
    ]

使用例：
    ・"foreground;notepad" + Enter
      メモ帳(notepad.exe)を全て最前面に表示する。

    ・"foreground:memochou" + Enter
      メモ帳をドラッグ＆ドロップで memochou として登録していれば、
      このように指定することも可能。

    ・"close;notepad" + Enter
      メモ帳を全て閉じる（編集中の場合は閉じるかどうか確認される）。

    ・"notepad" + Ctrl + [-]
      同上。

    ※foreground, close などで操作するウインドウは、プロセス名、または、ドラッグ＆ドロップで
      登録したコマンド名で指定します。
"""

import os
from clnch import *

def loadCommandListFromIniFile():
    i=0
    while True:
        try:
            command_string = clnch_ini.get( "COMMANDLIST", "command_%d"%(i,) )
        except:
            break

        yield eval( command_string )
        i += 1


# --------------------------------------------------------------------
# generator
def command_WindowGenerator(f):

    def commandHandler(args):
        # nonlocal...
        count = [0]

        def callback( wnd, fn ):
            if wnd.getProcessName().lower() == fn and wnd.isVisible():
                count[0] += 1
                f(wnd)
            return True

        if len(args) == 0:
            print( u"対象が指定されていません." )
            return

        command_name = args[0].lower()
        for command in loadCommandListFromIniFile():
            # ini のコマンド名から exe を探す
            if command_name == command[0].lower():
                pyauto.Window.enum( callback, os.path.basename(command[1]).lower() )
                break
        else:
            # プロセス名として解釈する
            if command_name[-4:].lower() != ".exe":
                command_name += ".exe"
            pyauto.Window.enum( callback, command_name )

        if count[0] == 0:
            print( "No window found: %s" % args[0] )

    return commandHandler

def foregroundHandler(wnd):
    wnd = wnd.getLastActivePopup()
    wnd.setForeground(False)
    wnd.setActive()

WM_CLOSE = 16

# --------------------------------------------------------------------
# ウインドウを最前面にするコマンド
command_ForegroundWindow = command_WindowGenerator( foregroundHandler )

# --------------------------------------------------------------------
# ウインドウを閉じるコマンド
command_CloseWindow = command_WindowGenerator( lambda wnd: wnd.sendMessage( WM_CLOSE, 0, 0 ) )

# --------------------------------------------------------------------
# ウインドウを最小化するコマンド
command_MinimizeWindow = command_WindowGenerator( lambda wnd: wnd.minimize() )

# --------------------------------------------------------------------
# ウインドウを最大化するコマンド
command_MaximizeWindow = command_WindowGenerator( lambda wnd: wnd.maximize() )

# --------------------------------------------------------------------
# ウインドウを元に戻すコマンド
command_RestoreWindow = command_WindowGenerator( lambda wnd: wnd.restore() )
