#coding:utf-8

"""
Ctrl-Shift-Enter で管理者として実行する

スタート メニューの [プログラムとファイルの検索] で Ctrl-Shift-Enter を
押すと [管理者として実行] の効果が得られる挙動を CraftLaunch 3 で
可能にします。
(Windows Vista 以降で UAC が有効の場合)

定義例：
    # config.py の configure() 関数に次のように記載します

    import run_as_administrator
    run_as_administrator.register(window)

"""

from clnch import *
import pyauto
import ctypes

# --------------------------------------------------------------------
# コマンドラインを登録する
def register(window):

    # オリジナルの ShellExecuteW をバックアップする
    if not 'ShellExecuteW__' in ctypes.windll.shell32.__dict__:
        ctypes.windll.shell32.ShellExecuteW__ = ctypes.windll.shell32.ShellExecuteW

    # ラップ用 ShellExecute
    # 各種コマンドや各種コマンドラインで ckit.shellExecute 
    def _ShellExecuteW( hwnd, verb, filename, param, directory, swmode ):
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
            verb = unicode('runas', 'mbcs')

        # オリジナルの ShellExecute を実行
        return ctypes.windll.shell32.ShellExecuteW__( hwnd, verb, filename, param, directory, swmode)

    ctypes.windll.shell32.ShellExecuteW = _ShellExecuteW
