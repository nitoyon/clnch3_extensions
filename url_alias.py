#coding:utf-8

"""
特定のキーワードが入力されたときに URL を開くための拡張

実行例：
    rfc822
      → http://www.ietf.org/rfc/rfc822.txt を規定のブラウザで開く

    @nitoyon
      → http://twitter.com/nitoyon を規定のブラウザで開く

定義例：
    # config.py の configure() 関数に次のように記載します

    import url_alias
    #reload(url_alias)
    url_alias.register(window, 
                       { 'regex': re.compile('^rfc(\d+)$', re.IGNORECASE), 
                         'url': 'http://www.ietf.org/rfc/rfc%param%.txt' },
                       { 'regex': re.compile('^@(\w+)$'), 
                         'url': 'http://twitter.com/%param%' },
                      )

"""

from clnch import *

# --------------------------------------------------------------------
# url alias を有効にします
#
# 引数:
# - window:
#     メインウインドウ オブジェクト。
# - pattern1:
#      入力パターン。
# - pattern2:
#       :
#       :
def register(window, *args):

    url_alias = commandline_UrlAlias(window, args)
    window.commandline_list.insert(0, url_alias)


# --------------------------------------------------------------------
# "UrlAlias" コマンドライン
class commandline_UrlAlias:

    def __init__( self, main_window, patterns ):
        self.main_window = main_window
        self.patterns = patterns

    def onCandidate( self, update_info ):
        return []
    
    def onEnter( self, commandline, text, mod ):

        for pattern in self.patterns:
            m = pattern['regex'].search(text)
            if m:
                break
        else:
            return False

        # エディットの文字列を変更
        command = self.main_window.command_URL(pattern['url'])
        clnch_commandline.executeCommand(commandline, command, m.groups(), mod, text, True)
        return True

    def onStatusString( self, text ):
        return None
