import pickle
import os
from pathlib import Path
import wx


class Frame(wx.Frame):
    def __init__(self, *args, **kw):
        if not os.path.exists('.storage/'):
            os.makedirs('.storage/')
        Path('.storage/var_storage.pk').touch(exist_ok=True)
        self.varStorage = ".storage/var_storage.pk"
        try:
            self.saveLocation = pickle.load(open(self.varStorage, "rb"))
        except EOFError:
            self.saveLocation = ".storage/"
        self.fileLocation = self.saveLocation + "brew-list.txt"
        super(Frame, self).__init__(*args, **kw)
        pnl = wx.Panel(self)
        st = wx.StaticText(pnl, label="What would you like to do today?")
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)
        save = wx.Button(pnl, label="Save", id=1)
        install = wx.Button(pnl, label="Install", id=2)
        modify = wx.Button(pnl, label="Modify", id=3)
        quitProgram = wx.Button(pnl, label="Quit", id=4)
        self.Bind(wx.EVT_BUTTON, self.OnSave, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnInstall, id=2)
        self.Bind(wx.EVT_BUTTON, self.OnModify, id=3)
        self.Bind(wx.EVT_BUTTON, self.OnExit, id=4)
        wrapper = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.GridBagSizer(3, 4)
        sizer.Add(st, flag=wx.ALIGN_CENTER | wx.EXPAND, pos=(0, 0), span=(0, 4))
        sizer.Add(save, flag=wx.EXPAND, pos=(1, 0))
        sizer.Add(install, flag=wx.EXPAND, pos=(1, 1))
        sizer.Add(modify, flag=wx.EXPAND, pos=(1, 2))
        sizer.Add(quitProgram, flag=wx.EXPAND, pos=(1, 3))
        sizer.AddGrowableRow(1)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableCol(2)
        wrapper.Add(sizer, 1, wx.EXPAND | wx.ALL, 10)
        pnl.SetSizer(wrapper)
        self.makeMenuBar()
        self.CreateStatusBar()
        self.SetStatusText("Welcome to Homebrew Backup!")

    def makeMenuBar(self):
        fileMenu = wx.Menu()
        saveItem = fileMenu.Append(101, "&Save...\tCtrl-S", "Save the package list.")
        installItem = fileMenu.Append(102, "&Install...\tCtrl-I", "Install from the package list.")
        modifyItem = fileMenu.Append(103, "&Modify...\tCtrl-M", "Modify the save directory.")

        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT)
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnSave, saveItem)
        self.Bind(wx.EVT_MENU, self.OnInstall, installItem)
        self.Bind(wx.EVT_MENU, self.OnModify, modifyItem)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        self.Close(True)

    def OnInstall(self, event):
        self.SetStatusText("Installing...")
        try:
            installList = open(self.fileLocation, "r").read().replace("\n", " ")
            os.system("brew install " + installList)
            self.SetStatusText("Installation was successful!")
            wx.MessageBox("Installation was successful!")
        except:
            wx.MessageBox("Installation failed! Try running the terminal version of the application.")

    def OnModify(self, event):
        self.SetStatusText("Modifying...")
        try:
            dlg = wx.DirDialog(None, "Choose your save directory...", "",
                               wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
            if dlg.ShowModal() == wx.ID_OK:
                self.saveLocation = dlg.GetPath() + "/"
            with open(self.varStorage, "wb") as file:
                pickle.dump(self.saveLocation, file)
            self.fileLocation = self.saveLocation + "brew-list.txt"
            self.SetStatusText("Modification of save directory was successful!")
            wx.MessageBox("Modification of save directory was successful!")
        except:
            wx.MessageBox("Modification of save directory failed!")

    def OnSave(self, event):
        if not os.path.exists(self.saveLocation):
            self.SetStatusText("Initializing...")
            os.makedirs(self.saveLocation)
        try:
            self.SetStatusText("Saving...")
            os.system("brew leaves > " + self.fileLocation)
            self.SetStatusText("Package list successfully saved!")
            wx.MessageBox("Package list successfully saved!")
        except:
            print("Package list failed to save!")

    def OnAbout(self, event):
        wx.MessageBox("Created by Alexander Leitzke\ngithub.com/ajleitzke",
                      "Homebrew Backup",
                      wx.OK | wx.ICON_INFORMATION)


if __name__ == '__main__':
    app = wx.App()
    frm = Frame(None, title="Homebrew Backup")
    frm.Show()
    app.MainLoop()
