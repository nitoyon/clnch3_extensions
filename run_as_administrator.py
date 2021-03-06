#coding:utf-8

"""
Ctrl-Shift-Enter で管理者として実行する

スタート メニューの [プログラムとファイルの検索] で Ctrl-Shift-Enter を
押すと [管理者として実行] の効果が得られる挙動を CraftLaunch 3 で
可能にします。
(Windows Vista 以降で UAC が有効の場合)

フォルダーを開くときに Ctrl-Shift-Enter を押しているときには
管理者のコマンド プロンプトでフォルダーを開きます。

定義例：
    # config.py の configure() 関数に次のように記載します

    import run_as_administrator
    run_as_administrator.register(window)

"""

from ckit.ckit_const import *
import os
import pyauto
import types

shell = "cmd.exe"

# --------------------------------------------------------------------
# コマンドラインを登録する
def register(window):

    # オリジナルの shellExecute をバックアップする
    if isinstance(pyauto.shellExecute, types.BuiltinFunctionType):
        pyauto.shellExecute__ = pyauto.shellExecute

    # ラップ用 ShellExecute
    # 各種コマンドや各種コマンドラインで ckit.shellExecute 
    def _shellExecute( verb,file,param=None,directory=None,swmode=None ):
        # キー状態を確認
        is_ctrl_down  = pyauto.Input.getAsyncKeyState(VK_CONTROL) & 0x8000
        is_shift_down = pyauto.Input.getAsyncKeyState(VK_SHIFT) & 0x8000
        is_alt_down   = pyauto.Input.getAsyncKeyState(VK_MENU) & 0x8000
        is_win_down   = pyauto.Input.getAsyncKeyState(VK_LWIN) & 0x8000 or pyauto.Input.getAsyncKeyState(VK_RWIN) & 0x8000
        is_enter_down = pyauto.Input.getAsyncKeyState(VK_RETURN) & 0x8000

        # Ctrl-Shift-Enter が押されていて verb が指定されていない場合は runas に変更
        if is_ctrl_down and \
           is_shift_down and \
           is_enter_down and \
           not is_alt_down and \
           not is_win_down and \
           verb is None:
            verb = 'runas'

            # ディレクトリを開くときにはコマンド プロンプトで開く
            if os.path.isdir(file):
                # 絶対パス化
                if not os.path.isabs(file):
                    file = os.path.abspath(file)

                # 管理者のコマンドプロンプトには directory が引き継がれないので
                # cd コマンドで移動させる
                # (例) D:\test → cmd.exe /k "D: & cd D:\test"
                param = '/k "%s & cd %s"' % (os.path.splitdrive(file)[0], file)
                file = "cmd.exe"

        # オリジナルの ShellExecute を実行
        return pyauto.shellExecute__( verb, file, param, directory, swmode )

    pyauto.shellExecute = _shellExecute
