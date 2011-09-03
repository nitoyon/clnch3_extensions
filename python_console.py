#coding:utf-8

"""
Python インタラクティブ シェルを可能にする

定義例：
    # config.py に次のように記載します

    import python_console
    #reload(python_console)
    python_console.register()

実行例：
    >>> a = [1,3,5]

    >>> a
    [1, 3, 5]

    >>> for i in a:
    ...     print i
    1
    3
    5
"""

import os
from clnch import *

# --------------------------------------------------------------------
# python console を有効にします
#
# 引数:
# - window:
#     メインウインドウ オブジェクト。
# - append_history: 
#     入力した文字列を履歴に追加するかどうか(bool)。デフォルト False。
# - ps1:
#     開始するときの先頭文字列。デフォルト ">>> "。
# - ps2:
#     継続行の先頭文字列。デフォルト "... "。
def register(window, append_history=False, ps1=">>> ", ps2="... "):

    console = commandline_PythonConsole(window, append_history, ps1, ps2)
    window.commandline_list.insert(0, console)


# --------------------------------------------------------------------
# "PythonConsole" コマンドライン
# code.InteractiveInterpreter を参照して実装しています
class commandline_PythonConsole:

    def __init__( self, main_window, append_history, ps1=">>> ", ps2="... " ):
        self.main_window = main_window
        self.append_history = append_history
        self.ps1 = ps1
        self.ps2 = ps2
        self.locals = {"__name__": "__console__", "__doc__": None}
        self.compile = CommandCompiler()
        self.buffer = []
        self.filename = "<console>"
        self.resetbuffer()
        self.more = False

    def onCandidate( self, update_info ):
        text = update_info.text
        if text == "":
            # startswith で True を返さないように影響のない文字に変更
            text = "_______"

        # console 入力中にスペースを入力するためのハック
        vk_complete = self.main_window.commandline_edit.vk_complete
        contains_space = VK_SPACE in vk_complete
        if text.startswith(self.ps1) or self.ps1.startswith(text) or \
           text.startswith(self.ps2) or self.ps2.startswith(text):
            if contains_space:
                vk_complete.remove(VK_SPACE)
        else:
            if not contains_space:
                vk_complete.append(VK_SPACE)

        # ps1, ps2 を候補として返す
        if self.ps1.startswith(text):
            return [self.ps1]
        elif self.ps2.startswith(text):
            return [self.ps2]

        return []
    
    def onEnter( self, commandline, text, mod ):

        # 今回の ps を判定
        if text.startswith(self.ps2) and self.more:
            ps = self.ps2
        elif text.startswith(self.ps1):
            ps = self.ps1
            self.resetbuffer()
        else:
            return False

        # 実行
        print text
        self.more = self.push(text[len(ps):])

        # 履歴に追加
        if self.append_history:
            commandline.appendHistory(text)

        # エディットの文字列を変更
        display_text = self.ps2 if self.more else self.ps1
        commandline.setText(display_text)
        commandline.updateWindowWidth(display_text)
        commandline.setSelection( [ len(display_text), len(display_text) ] )
        commandline.paint()

        return True

    def onStatusString( self, text ):
        return None

    def resetbuffer(self):
        self.buffer = []

    def push(self, line):
        self.buffer.append(line)
        source = "\n".join(self.buffer)
        more = self.runsource(source, self.filename)
        if not more:
            self.resetbuffer()
        return more

    def runsource(self, source, filename="<input>", symbol="single"):
        """Compile and run some source in the interpreter.

        Arguments are as for compile_command().

        One several things can happen:

        1) The input is incorrect; compile_command() raised an
        exception (SyntaxError or OverflowError).  A syntax traceback
        will be printed by calling the showsyntaxerror() method.

        2) The input is incomplete, and more input is required;
        compile_command() returned None.  Nothing happens.

        3) The input is complete; compile_command() returned a code
        object.  The code is executed by calling self.runcode() (which
        also handles run-time exceptions, except for SystemExit).

        The return value is True in case 2, False in the other cases (unless
        an exception is raised).  The return value can be used to
        decide whether to use sys.ps1 or sys.ps2 to prompt the next
        line.

        """
        try:
            code = self.compile(source, filename, symbol)
        except (OverflowError, SyntaxError, ValueError):
            # Case 1
            self.showsyntaxerror(filename)
            return False

        if code is None:
            # Case 2
            return True

        # Case 3
        self.runcode(code)
        return False

    def runcode(self, code):
        """Execute a code object.

        When an exception occurs, self.showtraceback() is called to
        display a traceback.  All exceptions are caught except
        SystemExit, which is reraised.

        A note about KeyboardInterrupt: this exception may occur
        elsewhere in this code, and may not always be caught.  The
        caller should be prepared to deal with it.

        """
        try:
            exec code in self.locals
        except SystemExit:
            raise
        except:
            self.showtraceback()
        else:
            print

    def showsyntaxerror(self, filename=None):
        """Display the syntax error that just occurred.

        This doesn't display a stack trace because there isn't one.

        If a filename is given, it is stuffed in the exception instead
        of what was there before (because Python's parser always uses
        "<string>" when reading from a string).

        The output is written by self.write(), below.

        """
        type, value, sys.last_traceback = sys.exc_info()
        sys.last_type = type
        sys.last_value = value
        if filename and type is SyntaxError:
            # Work hard to stuff the correct filename in the exception
            try:
                msg, (dummy_filename, lineno, offset, line) = value
            except:
                # Not the format we expect; leave it alone
                pass
            else:
                # Stuff in the right filename
                value = SyntaxError(msg, (filename, lineno, offset, line))
                sys.last_value = value
        list = traceback.format_exception_only(type, value)
        print "".join(list)

    def showtraceback(self):
        """Display the exception that just occurred.

        We remove the first stack item because it is our own code.

        The output is written by self.write(), below.

        """
        try:
            type, value, tb = sys.exc_info()
            sys.last_type = type
            sys.last_value = value
            sys.last_traceback = tb
            tblist = traceback.extract_tb(tb)
            del tblist[:1]
            list = traceback.format_list(tblist)
            if list:
                list.insert(0, "Traceback (most recent call last):\n")
            list[len(list):] = traceback.format_exception_only(type, value)
        finally:
            tblist = tb = None
        print "".join(list)


# --------------------------------------------------------------------
# codeop.py
import __future__

_features = [getattr(__future__, fname)
             for fname in __future__.all_feature_names]

PyCF_DONT_IMPLY_DEDENT = 0x200          # Matches pythonrun.h

def _maybe_compile(compiler, source, filename, symbol):
    # Check for source consisting of only blank lines and comments
    for line in source.split("\n"):
        line = line.strip()
        if line and line[0] != '#':
            break               # Leave it alone
    else:
        if symbol != "eval":
            source = "pass"     # Replace it with a 'pass' statement

    err = err1 = err2 = None
    code = code1 = code2 = None

    try:
        code = compiler(source, filename, symbol)
    except SyntaxError, err:
        pass

    try:
        code1 = compiler(source + "\n", filename, symbol)
    except SyntaxError, err1:
        pass

    try:
        code2 = compiler(source + "\n\n", filename, symbol)
    except SyntaxError, err2:
        pass

    if code:
        return code
    if not code1 and repr(err1) == repr(err2):
        raise SyntaxError, err1

class Compile:
    """Instances of this class behave much like the built-in compile
    function, but if one is used to compile text containing a future
    statement, it "remembers" and compiles all subsequent program texts
    with the statement in force."""
    def __init__(self):
        self.flags = PyCF_DONT_IMPLY_DEDENT

    def __call__(self, source, filename, symbol):
        codeob = compile(source, filename, symbol, self.flags, 1)
        for feature in _features:
            if codeob.co_flags & feature.compiler_flag:
                self.flags |= feature.compiler_flag
        return codeob

class CommandCompiler:
    """Instances of this class have __call__ methods identical in
    signature to compile_command; the difference is that if the
    instance compiles program text containing a __future__ statement,
    the instance 'remembers' and compiles all subsequent program texts
    with the statement in force."""

    def __init__(self,):
        self.compiler = Compile()

    def __call__(self, source, filename="<input>", symbol="single"):
        r"""Compile a command and determine whether it is incomplete.

        Arguments:

        source -- the source string; may contain \n characters
        filename -- optional filename from which source was read;
                    default "<input>"
        symbol -- optional grammar start symbol; "single" (default) or
                  "eval"

        Return value / exceptions raised:

        - Return a code object if the command is complete and valid
        - Return None if the command is incomplete
        - Raise SyntaxError, ValueError or OverflowError if the command is a
          syntax error (OverflowError and ValueError can be produced by
          malformed literals).
        """
        return _maybe_compile(self.compiler, source, filename, symbol)
