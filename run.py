import sys
import subprocess
import _winreg

import wx
import win32serviceutil
import pywintypes


class WinFrame(wx.Frame):
    def __init__(self, parent, title):
        super(WinFrame, self).__init__(parent, title=title, size=[375, 115],
                                       style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        wxpanel = wx.Panel(self)

        self.telebox = wx.CheckBox(wxpanel, label="Enable Telemetry", pos=(10, 15))
        self.telebox.Set3StateValue(0)

        self.diagbox = wx.CheckBox(wxpanel, label="Enable DiagTrack log", pos=(10, 45))
        self.diagbox.Set3StateValue(0)

        self.hostbox = wx.CheckBox(wxpanel, label="Unblock tracking servers with HOSTS file", pos=(10, 60))
        self.hostbox.Set3StateValue(0)

        self.servicebox = wx.CheckBox(wxpanel, label="Enable Services", pos=(10, 30))
        self.servicebox.Set3StateValue(0)
        self.servicebox.Bind(wx.EVT_CHECKBOX, self.serviceradcheck)

        self.servicerad = wx.RadioBox(wxpanel, label="Service Method", pos=(135, 10), choices=["Enable"])
        self.servicerad.Disable()

        self.okbutton = wx.Button(wxpanel, -1, "Go Public!", (275, 25))
        self.Bind(wx.EVT_BUTTON, self.onok, self.okbutton)
        self.Centre()
        self.Show()

    def serviceradcheck(self, event):
        self.servicerad.Enable(self.servicebox.IsChecked())  # If Service box is ticked enable Service radio box

    def onok(self, event):
        if self.telebox.IsChecked():
            self.telekeypath = r'SOFTWARE\Policies\Microsoft\Windows\DataCollection'  # Path to Telemetry key

            try:
                self.telekey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, self.telekeypath, 0, _winreg.KEY_ALL_ACCESS)
                _winreg.SetValueEx(self.telekey, "AllowTelemetry", 0, _winreg.REG_SZ, "1")  # Enable Telemetry
                _winreg.CloseKey(self.telekey)
            except WindowsError:
                pass
        if self.diagbox.IsChecked():
            try:
                subprocess.Popen(
                    "echo y|cacls C:\ProgramData\Microsoft\Diagnosis\ETLLogs\AutoLogger\AutoLogger-Diagtrack-Listener.etl /e /g SYSTEM:F",
                    shell=True)  # Prevent modification to file
            except IOError:
                pass

        if self.hostbox.IsChecked():
            self.MSHosts = "# Copyright (c) 1993-2006 Microsoft Corp.\r\n\
                              #\r\n\
                              # This is a sample HOSTS file used by Microsoft TCP/IP for Windows.\r\n\
                              #\r\n\
                              # This file contains the mappings of IP addresses to host names. Each\r\n\
                              # entry should be kept on an individual line. The IP address should\r\n\
                              # be placed in the first column followed by the corresponding host name.\r\n\
                              # The IP address and the host name should be separated by at least one\r\n\
                              # space.\r\n\
                              #\r\n\
                              # Additionally, comments (such as these) may be inserted on individual\r\n\
                              # lines or following the machine name denoted by a '#' symbol.\r\n\
                              #\r\n\
                              # For example:\r\n\
                              #\r\n\
                              #      102.54.94.97     rhino.acme.com          # source server\r\n\
                              #       38.25.63.10     x.acme.com              # x client host\r\n\
                              # localhost name resolution is handle within DNS itself.\r\n\
                              #       127.0.0.1       localhost\r\n\
                              #       ::1             localhost\r\n"
            try:
                with open('C:\Windows\System32\drivers\etc\hosts', 'wb') as f:
                    f.write(self.MSHosts)
            except WindowsError:
                pass

        if self.servicebox.IsChecked():
            self.diagkeypath = r'SYSTEM\CurrentControlSet\Services\DiagTrack'
            self.dmwakeypath = r'SYSTEM\CurrentControlSet\Services\dmwappushsvc'

            try:
                self.diagkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, self.diagkeypath, 0, _winreg.KEY_ALL_ACCESS)
                _winreg.SetValueEx(self.diagkey, "Start", 0, _winreg.REG_DWORD, 0x0000002)
                _winreg.CloseKey(self.diagkey)
            except WindowsError:
                pass

            try:
                self.dmwakey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, self.dmwakeypath, 0, _winreg.KEY_ALL_ACCESS)
                _winreg.SetValueEx(self.dmwakey, "Start", 0, _winreg.REG_DWORD, 0x0000002)
                _winreg.CloseKey(self.dmwakey)
            except WindowsError:
                pass

            try:
                win32serviceutil.StartService('Diagnostics Tracking Service')  # Enable Diagnostics Tracking Service
            except pywintypes.error:
                print "Diagnostics Tracking Service unable to be started. Deleted, or is the program not elevated?"
                pass

            try:
                win32serviceutil.StartService('dmwappushsvc')  # Enable dmwappushsvc
            except pywintypes.error:
                print "dmwappushsvc unable to be started. Deleted, or is the program not elevated?"
                pass

            print "Services Enabled"
        sys.exit()


if __name__ == '__main__':
    wxwindow = wx.App(False)
    WinFrame(None, title='Enable Windows 10 Tracking')  # Create Window
    wxwindow.MainLoop()
