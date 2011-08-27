#coding:utf-8

"""
�E�C���h�E����������R�}���h�Q

��`��F
    # config.py �Ɏ��̂悤�ɋL�ڂ��܂�

    import window_command
    #reload(window_command)
    window.cmd_keymap[ KeyEvent( VK_L, MODKEY_CTRL ) ] = window_command.command_ForegroundWindow
    window.cmd_keymap[ KeyEvent( VK_OEM_MINUS, MODKEY_CTRL ) ] = window_command.command_CloseWindow
    window.launcher.command_list += [
        ( u"foreground", window_command.command_ForegroundWindow ),
        ( u"close",      window_command.command_CloseWindow ),
        ( u"minimize",   window_command.command_MinimizeWindow ),
        ( u"maximize",   window_command.command_MaximizeWindow ),
        ( u"restore",    window_command.command_RestoreWindow ),
    ]

�g�p��F
    �E"foreground;notepad" + Enter
      ������(notepad.exe)��S�čőO�ʂɕ\������B

    �E"foreground:memochou" + Enter
      ���������h���b�O���h���b�v�� memochou �Ƃ��ēo�^���Ă���΁A
      ���̂悤�Ɏw�肷�邱�Ƃ��\�B

    �E"close;notepad" + Enter
      ��������S�ĕ���i�ҏW���̏ꍇ�͕��邩�ǂ����m�F�����j�B

    �E"notepad" + Ctrl + [-]
      ����B

    ��foreground, close �Ȃǂő��삷��E�C���h�E�́A�v���Z�X���A�܂��́A�h���b�O���h���b�v��
      �o�^�����R�}���h���Ŏw�肵�܂��B
"""

import os
from clnch import *

def loadCommandListFromIniFile():
    i=0
    while True:
        try:
            command_string = unicode( clnch_ini.get( "COMMANDLIST", "command_%d"%(i,) ), "utf8" )
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
            print "�Ώۂ��w�肳��Ă��܂���."
            return

        command_name = args[0].lower()
        for command in loadCommandListFromIniFile():
            # ini �̃R�}���h������ exe ��T��
            if command_name == command[0].lower():
                pyauto.Window.enum( callback, os.path.basename(command[1]).lower() )
                break
        else:
            # �v���Z�X���Ƃ��ĉ��߂���
            if command_name[-4:].lower() != ".exe":
                command_name += ".exe"
            pyauto.Window.enum( callback, command_name )

        if count[0] == 0:
            print "No window found: %s" % args[0]

    return commandHandler

def foregroundHandler(wnd):
    wnd = wnd.getLastActivePopup()
    wnd.setForeground(False)
    wnd.setActive()

WM_CLOSE = 16

# --------------------------------------------------------------------
# �E�C���h�E���őO�ʂɂ���R�}���h
command_ForegroundWindow = command_WindowGenerator( foregroundHandler )

# --------------------------------------------------------------------
# �E�C���h�E�����R�}���h
command_CloseWindow = command_WindowGenerator( lambda wnd: wnd.sendMessage( WM_CLOSE, 0, 0 ) )

# --------------------------------------------------------------------
# �E�C���h�E���ŏ�������R�}���h
command_MinimizeWindow = command_WindowGenerator( lambda wnd: wnd.minimize() )

# --------------------------------------------------------------------
# �E�C���h�E���ő剻����R�}���h
command_MaximizeWindow = command_WindowGenerator( lambda wnd: wnd.maximize() )

# --------------------------------------------------------------------
# �E�C���h�E�����ɖ߂��R�}���h
command_RestoreWindow = command_WindowGenerator( lambda wnd: wnd.restore() )
