#coding:utf-8

"""
コントロール パネルを開くためのコマンド群

定義例：
    # config.py に次のように記載します

    import control_panel
    #reload(control_panel)
    control_panel.register(window)

利用例：

    cpl
    → コントロール パネルを開く

    cpl:Network
    → ネットワークを開く

    cpl:UserAccount
    → ユーザー アカウントを開く

    cpl:ComputerManagement
    → コンピューターの管理を開く

    cpl:EventViewer
    → イベント ビューワーを開く

    ※ control_panel.register() の prefix 引数で cpl の部分を変更できます。

"""

import os
from clnch import *

# --------------------------------------------------------------------
# コマンド登録
def register(window, prefix="cpl"):
    commands = ControlCommandList(window, prefix)
    window.launcher.command_list += commands.getCommandList()


class ControlCommandList:
    def __init__( self, main_window, prefix='cpl' ):
        self.main_window = main_window
        self.prefix = prefix
        self.systemPath = getSystemPath()
        self.params = {}

        self.addControl('',                                     u'')
        self.addControl('Accessibility Options',                u"access.cpl")
        self.addControl('Add Remove Programs',                  u"appwiz.cpl")
        self.addControl('ProgramAnd Features',                  u"appwiz.cpl")
        self.addControl('Date/Time',                            u"timedate.cpl")
        self.addControl('Display Properties',                   u"desktop")
        self.addControl('Desktop Properties',                   u"desktop")
        self.addControl('Desktop Appearance',                   u"color")
        self.addControl('Fonts',                                u"fonts")
        self.addControl('Folder Options',                       u"folders")
        self.addControl('Internet Properties',                  u"inetcpl.cpl")
        self.addControl('Joystick',                             u"joy.cpl")
        self.addControl('Game Controllers',                     u"joy.cpl")
        self.addControl('Keyboard',                             u"keyboard")
        self.addControl('Mouse',                                u"mouse")
        self.addControl('Regional and Languages',               u"international")
        self.addControl('Sound Property',                       u"mmsys.cpl")
        self.addControl('Multimedia Properties',                u"mmsys.cpl")
        self.addControl('Power Option',                         u"powercfg.cpl")
        self.addControl('Modem',                                u"telephony")
        self.addControl('Phone and Modem',                      u"telephony")
        self.addControl('Network',                              u"netconnections")
        self.addControl('Scaner and Camera',                    u"scannercamera")
        self.addControl('User Account',                         u"userpasswords")
        self.addControl('User Account2',                        u"userpasswords2")
        self.addControl("Printers",                             u"printers")
        self.addControl("System Properties",                    u"sysdm.cpl")
        self.addControl("Text Service and Input Language",      u"input.dll")
        self.addControl("Administrative Tools",                 u"admintools")
        self.addControl("Scheduled Tasks",                      u"schedtasks")
        self.addControl("ODBC",                                 u"odbccp32.cpl")
        self.addControl("Data Source",                          u"odbccp32.cpl")
        self.addControl("Firewall",                             u"firewall.cpl")
        self.addControl("Windows Update",                       u"wuaucpl.cpl")
        self.addControl("Security Center",                      u"wscui.cpl")
        self.addControl("License",                              u"liccpa.cpl")
        self.addControl("Network Setup",                        u"netsetup.cpl")

        self.addMmc("ADSI Edit",                                u"adsiedit.msc")
        self.addMmc("Authorization Manager",                    u"azman.msc")
        self.addMmc("Certificates",                             u"certmgr.msc")
        self.addMmc("Indexing Service",                         u"ciadv.msc")
        self.addMmc("Component Services",                       u"comexp.msc")
        self.addMmc("Computer Management",                      u"compmgmt.msc")
        self.addMmc("Device Manager",                           u"devmgmt.msc")
        self.addMmc("Disk Defragmenter",                        u"dfrg.msc")
        self.addMmc("Defragmenter",                             u"dfrg.msc")
        self.addMmc("DHCP",                                     u"dhcpmgmt.msc")
        self.addMmc("Disk Management",                          u"diskmgmt.msc")
        self.addMmc("DNS",                                      u"dnsmgmt.msc")
        self.addMmc("Active Directory Domains and Trusts",      u"domain.msc")
        self.addMmc("Active Directory Users and Computers",     u"dsa.msc")
        self.addMmc("Active Directory Sites and Services",      u"dssite.msc")
        self.addMmc("Event Viewer",                             u"eventvwr.msc")
        self.addMmc("Shared Folders",                           u"fsmgmt.msc")
        self.addMmc("Local Group Policy Editor",                u"gpedit.msc")
        self.addMmc("Group Policy Editor",                      u"gpedit.msc")
        self.addMmc("Group Policy Management",                  u"gpmc.msc")
        self.addMmc("Group Policy Management Editor",           u"gpme.msc")
        self.addMmc("Group Policy Starter GPO Editor",          u"gptedit")
        self.addMmc("IIS",                                      u"inetsrv\\iis.msc")
        self.addMmc("Internet Information Services",            u"inetsrv\\iis.msc")
        self.addMmc("Internet Authentication Service",          u"ias.msc")
        self.addMmc("IAS",                                      u"ias.msc")
        self.addMmc("Local Users and Groups",                   u"lusrmgr.msc")
        self.addMmc("Removable Storage Manager ",               u"ntmsmgr.msc")
        self.addMmc("Removable Storage Operator Requests",      u"ntmsoprq.msc")
        self.addMmc("Performance Monitor",                      u"perfmon.msc")
        self.addMmc("Print Management",                         u"printmanagement.msc")
        self.addMmc("Resultant Set of Policy",                  u"rsop.msc")
        self.addMmc("Local Security Policy",                    u"secpol.msc") 
        self.addMmc("Security Policy",                          u"secpol.msc")
        self.addMmc("Server Manager",                           u"ServerManager.msc")
        self.addMmc("Services",                                 u"services.msc")
        self.addMmc("Share and Storage Management",             u"StorageMgmt.msc")
        self.addMmc("Storage Explorer",                         u"StorExpl.msc")
        self.addMmc("Telephony",                                u"tapimgmt.msc")
        self.addMmc("Task Scheduler",                           u"taskschd.msc")
        self.addMmc("Trusted Platform Module Management",       u"tpm.msc")
        self.addMmc("TPM Management",                           u"tpm.msc")
        self.addMmc("Terminal Services Manager",                u"tsadmin.msc")
        self.addMmc("Terminal Services Configuration",          u"tsconfig.msc")
        self.addMmc("Remote Desktops",                          u"tsmmc.msc")
        self.addMmc("Windows Server Backup",                    u"wbadmin.msc")
        self.addMmc("Windows Firewall with Advanced Security",  u"WF.msc")
        self.addMmc("Firewall with Advanced Security",          u"WF.msc")
        self.addMmc("WMI Control",                              u"wmimgmt.msc")
        self.addMmc("Windows Management Instrumentation",       u"wmimgmt.msc")

    def addControl(self, name, param):
        # 拡張子がある場合はファイル
        if param:
            if ckit.splitExt(param)[1]:
                param = ckit.joinPath(self.systemPath, param)

                # ファイルが存在しない場合は追加しない
                if not os.path.isfile(param):
                    return

        # 追加する
        name = self.addPrefix(self.capitalize(name))
        if not name:
            return
        self.params[name] = self.main_window.command_ShellExecute(None, u"control.exe", param, '')

    def addMmc(self, name, param):
        param = ckit.joinPath(self.systemPath, param)

        # ファイルが存在しない場合は追加しない
        if not os.path.isfile(param):
            return

        # 追加する
        name = self.addPrefix(self.capitalize(name))
        self.params[name] = self.main_window.command_ShellExecute(None, u"mmc.exe", param, '')

    def addPrefix(self, name):
        if not self.prefix:
            return name
        if name:
            return "%s:%s" % (self.prefix, name)
        else:
            return self.prefix

    def capitalize(self, s):
        return ''.join(map(lambda x: x[0].upper() + x[1:] if len(x) > 1 else x, s.split(' ')))

    def getCommandList(self):
        return [(k, self.params[k]) for k in sorted(self.params.keys())]

def getSystemPath():

    MAX_PATH = 260
    CSIDL_SYSTEM = 0x25

    buf = ctypes.create_unicode_buffer(MAX_PATH)
    ctypes.windll.shell32.SHGetSpecialFolderPathW( None, buf, CSIDL_SYSTEM, 0 )

    return buf.value
