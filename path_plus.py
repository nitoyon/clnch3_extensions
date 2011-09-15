#coding:utf-8

"""
相対パス・フォルダエイリアス対応化

定義例：
    # config.py の configure() 関数の末尾に次のように記載します

    import path_plus
    #reload(path_plus)
    window.launcher.command_list += [( u"cd", path_plus.command_ChangeDirectory )]
    path_plus.register(window)


使用例：
    ・"~\memo.txt"
      マイドキュメントを ~ として登録しておくと、「~\」でマイドキュメント
      配下のファイル・フォルダーへアクセスできます。

    ・".\"
      カレントフォルダー配下のファイル・フォルダーへアクセスできます。
      ※ 標準でもサポートされていますが、深い階層のファイルを開くと
         エラーになる問題を修正しています

    ・"cd;..\"
      カレントフォルダーを１つ上の階層に移動します。
"""

import os
import sys
from clnch import *

class IniCommandList:
    def __init__( self ):
        self.mtime = 0
        self.updateCommandList()

    def updateCommandList(self):

        # check modified
        mtime = os.path.getmtime( clnch_ini.ini_filename )
        if self.mtime >= mtime:
            return
        self.mtime = mtime

        self.command_list = []
        i=0
        while True:
            try:
                command_string = unicode( clnch_ini.get( "COMMANDLIST", "command_%d"%(i,) ), "utf8" )
            except:
                break
        
            command_tuple = eval( command_string )
            self.command_list.append(command_tuple[0:2])
            i += 1

    def convertArg( self, arg ):
        for item in self.command_list:
            item_lower = item[0].lower()
            if arg.lower().startswith(item_lower + u"\\") or arg.lower().startswith(item_lower + u"/"):
                path = item[1]
                if os.path.isfile(path):
                    path, tmp = os.path.split(path)
                return path +  arg[ len(item_lower): ]
        return arg

def fixHistory( main_window, orig_text, text):
    history = main_window.commandline_history
    if history[0] == text and orig_text != text:
        history.pop(0)
        history.insert(0, orig_text)

# --------------------------------------------------------------------
# "MyLauncher" コマンドライン
#   commandline_Launcher をカスタマイズします。
class commandline_MyLauncher(clnch_commandline.commandline_Launcher):
    def __init__( self, window, ini_commands ):
        clnch_commandline.commandline_Launcher.__init__( self, window )
        self.ini_commands = ini_commands
        self.command_list = window.launcher.command_list

    def create_new_update_info(self, update_info, new_text_left):
        text = update_info.text
        sel1 = update_info.selectionLeft()
        sel2 = update_info.selectionRight()
        text_left = text[ : sel1 ]
        text_sel = text[ sel1 : sel2 ]
        text_right = text[ sel2 : ]
        text_diff = len(new_text_left) - len(text_left)
        return update_info.__class__("%s%s%s" % (new_text_left, text_sel, text_right),
                                     [sel1 + text_diff, sel2 + text_diff])

    def onCandidate( self, update_info ):
        self.ini_commands.updateCommandList()

        left = update_info.text[ : update_info.selectionLeft() ]
        left_lower = left.lower()
        pos_arg = left.rfind(";")+1
        arg = left[ pos_arg : ]

        new_arg = self.ini_commands.convertArg(arg)
        if new_arg != arg:
            update_info = self.create_new_update_info(update_info, new_arg)

        return clnch_commandline.commandline_Launcher.onCandidate( self, update_info )

    def onEnter( self, commandline, text, mod ):
        orig_text = text
        args = map( self.ini_commands.convertArg, text.split(';') )

        # 元々の処理に委譲
        text = ";".join(args)
        ret = clnch_commandline.commandline_Launcher.onEnter( self, commandline, text, mod )

        # history を調整
        if ret:
            fixHistory(self.main_window, orig_text, text)
        return ret

# --------------------------------------------------------------------
# "MyLauncher" コマンドライン
#   commandline_Launcher をカスタマイズします。
class commandline_MyExecuteFile(clnch_commandline.commandline_ExecuteFile):
    def __init__( self, window, ini_commands ):
        clnch_commandline.commandline_ExecuteFile.__init__( self, window )
        self.ini_commands = ini_commands

    def onEnter( self, commandline, text, mod ):
        orig_text = text
        args = map( self.ini_commands.convertArg, text.split(';') )

        # ファイルを確認
        file = args[0]
        if not os.path.exists(file):
            return False

        # 絶対パス化
        if not os.path.isabs(file):
            file = os.path.abspath(file)
        args[0] = file

        # 元々の処理に委譲
        text = ";".join(args)
        ret = clnch_commandline.commandline_ExecuteFile.onEnter( self, commandline, text, mod )

        # history を調整
        if ret:
            fixHistory(self.main_window, orig_text, text)
        return ret


def fixCommand(func, window, ini_commands):
    def _newCommand(args):
        orig_text = ";".join(args)
        args = map( ini_commands.convertArg, args )

        # 元々の処理に委譲
        text = ";".join(args)
        ret = func(args)

        # history を調整
        if ret:
            fixHistory(window, orig_text, text)

    argspec = inspect.getargspec(func)
    if inspect.ismethod(func):
        num_args = len(argspec[0])-1
    else:
        num_args = len(argspec[0])

    if num_args == 1:
        return _newCommand
    else:
        return func

# --------------------------------------------------------------------
# "ChangeDirectory" コマンド
#   カレントフォルダを変更します。
#    cd;c:\users :   カレントフォルダを c:\users に変更します。
#    cd;L        :   カレントフォルダを表示します。
def command_ChangeDirectory(args):
    
    if len(args)>=1:
        dir = args[0]
        os.chdir(dir)
    else:
        print os.getcwd()

# --------------------------------------------------------------------
# コマンドラインを登録する
def register(window):
    ini_commands = IniCommandList()

    # commandline 置き換え
    my_launcher = commandline_MyLauncher(window, ini_commands)
    my_file = commandline_MyExecuteFile(window, ini_commands)
    window.launcher = my_launcher
    window.commandline_list = map(lambda commandline:
        my_launcher if isinstance(commandline, clnch_commandline.commandline_Launcher) else 
        my_file     if isinstance(commandline, clnch_commandline.commandline_ExecuteFile) else commandline,
        window.commandline_list)

    # cmd_keymap の command 置き換え
    for k,cmd in window.cmd_keymap.items():
        window.cmd_keymap[k] = fixCommand(cmd, window, ini_commands)
