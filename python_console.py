#coding:utf-8

"""
CraftLaunch で Python インタラクティブ シェルを使う拡張

  - CraftLaunch ver 3.27 で動作検証済。
  - CraftLaunch ver 3.26 では動きません。

実行例：
    ※ ">>> " も含めて CraftLaunch に入力してください

    >>> a = [1,3,5]
    >>> a
    [1, 3, 5]
    >>> for i in a:
    ...     print(i)
    ... 
    1
    3
    5

定義例：
    # config.py の configure() 関数に次のように記載します

    import python_console
    python_console.register(window)

"""

import os
from clnch import *
import code

# --------------------------------------------------------------------
# python console を有効にします
#
# 引数:
# - window:
#     メインウインドウ オブジェクト。
# - append_history: 
#     入力した文字列を履歴に追加するかどうか(bool)。デフォルト True。
# - ps1:
#     開始するときの先頭文字列。デフォルト ">>> "。
# - ps2:
#     継続行の先頭文字列。デフォルト "... "。
def register(window, append_history=True, ps1=">>> ", ps2="... "):

    console = commandline_PythonConsole(window, append_history, ps1, ps2)
    window.commandline_list.insert(0, console)


# --------------------------------------------------------------------
# "PythonConsole" コマンドライン
class commandline_PythonConsole(code.InteractiveConsole):

    def __init__( self, main_window, append_history, ps1, ps2 ):
        code.InteractiveConsole.__init__(self)
        self.main_window = main_window
        self.append_history = append_history
        self.more = False

        sys.ps1 = ps1
        sys.ps2 = ps2

    def onCandidate( self, update_info ):
        text = update_info.text
        if text == "":
            # startswith で True を返さないように影響のない文字に変更
            text = "_______"

        # console 入力中にスペースを入力可能にするためのハック
        vk_complete = self.main_window.commandline_edit.vk_complete
        contains_space = VK_SPACE in vk_complete
        if text.startswith(sys.ps1) or sys.ps1.startswith(text) or \
           text.startswith(sys.ps2) or sys.ps2.startswith(text):
            if contains_space:
                vk_complete.remove(VK_SPACE)
        else:
            if not contains_space:
                vk_complete.append(VK_SPACE)

        # ps1, ps2 を候補として返す
        if sys.ps1.startswith(text):
            return [sys.ps1]
        elif sys.ps2.startswith(text) and self.more:
            return [sys.ps2]

        return []
    
    def onEnter( self, commandline, text, mod ):

        # 今回の ps を判定
        if text.startswith(sys.ps2) and self.more:
            ps = sys.ps2
        elif text.startswith(sys.ps1):
            ps = sys.ps1
            self.resetbuffer()
        else:
            return False

        # 実行
        print(text)
        self.more = self.push(text[len(ps):])

        # 履歴に追加
        if self.append_history:
            commandline.appendHistory(text)

        # エディットの文字列を変更
        display_text = sys.ps2 if self.more else sys.ps1
        commandline.setText(display_text)
        commandline.updateWindowWidth(display_text)
        commandline.setSelection( [ len(display_text), len(display_text) ] )
        commandline.paint()

        return True

    def onStatusString( self, text ):
        return None
