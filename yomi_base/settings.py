# -*- coding: utf-8 -*-

# Copyright (C) 2013  Alex Yatskov
# Copyright (C) 2015  Christian Lott
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from PySide import QtGui, QtCore
import pickle, os

class cSettings(QtGui.QWidget):
    def __init__(self, session): # parent, preferences):
        QtGui.QWidget.__init__(self)

        if session.ThemeDir == "":
            self.ThemeDir = QtCore.QDir.currentPath() + "/theme/"
            self.ThemeFile = session.ThemeFile
        else:
            self.ThemeDir = session.ThemeDir
            self.ThemeFile = session.ThemeFile

        print "starting with: : " + self.ThemeFile
        self.transcriptlist = ""
        self.lookupline = ""
        self.vocab = ""
        self.linedefs = ""

        self.lookuplinedock = ""
        self.vocabdock = ""
        self.linedefsdock = ""
        self.statusbar = ""

        self.panel = ["Transcript List","Transcript Line Lookup",
                        "Vocabulary:Expression", "Vocabulary:Reading", "Vocabulary:Glossary",
                        "Definition:Expression", "Definition:Reading", "Definition:Glossary"]

        self.fonttype = list()
        self.fontsize = list()
        self.fgcolor = list()
        self.bgcolor = list()
        self.maxwinht = list()
        self.lineht = list()
        self.bgcolor_set = "white"
        self.bg_set = False

        self.setupUI()

    def settheme(self):
        print "#### set theme from: ####"
        print self.ThemeDir
        print self.ThemeFile
        print "#################### to:"
        # if self.ThemeFile == "Default" or self.ThemeFile == "":
        #     self.setdefaults()
        # else:
        #     self.loadfile()
        #if self.init == False:
        #print self.ThemeFile
        #print self.comboTheme.currentText()
        print "-----------------"
        self.ThemeFile = self.comboTheme.currentText()
        print self.ThemeFile
        if self.ThemeFile != "Default":
            self.loadfile()
            #self.comboTheme.setCurrentIndex(self.comboTheme.findText(self.ThemeFile))
            self.onPanelChanged()
            #self.comboTheme.addItem(self.ThemeFile + ".theme") # hacky, avoids re-query of dir
            #index = self.comboTheme.findText(self.ThemeFile + ".theme")
            #self.comboTheme.setCurrentIndex(index)
        else:
            self.setdefaults()
            print "defaulted"

    def showDialogThemeFolder(self):
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        dirNames = QtGui.QFileDialog.getOpenFileName
        if dialog.exec_():
            dirNames = dialog.selectedFiles()
            self.populatecombo("theme", self.comboTheme, dirNames[0], "Theme")
            self.basedir = dirNames[0]
            self.buttonThemeCreate.setDisabled(False)

    def populatecombo(self, filter, combo, dir, text):
        onlyfiles = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
        files = list()
        for x in onlyfiles:
            if x.split(".")[-1] in filter :
                files.append(x)

        combo.clear()
        combo.addItem("Default")
        combo.addItems(files)
        print "populatecombo"
        #self.statusbar.showMessage(text + " Folder set to: " + dir)

    def createtheme(self):
        # get new filename from input dialog
        # set as current filename(.theme), create new empty file
        # add new file to combobox and set it as current
        text, ok = QtGui.QInputDialog.getText(self, "Create Theme File", "File name:", QtGui.QLineEdit.Normal, "")
        if ok and text != '':
            self.ThemeFile = text + ".theme"
            file = open(self.ThemeDir + self.ThemeFile, 'w')
            #self.setdefaults()
            data = {'Panel':self.panel, 'FontFamily': self.fonttype, 'FontSize': self.fontsize, 'FgColor': self.fgcolor, 'BgColor': self.bgcolor, 'MaxWinHt': self.maxwinht, 'LineHt': self.lineht}
            pickle.dump(data, file)
            file.close()

            self.comboTheme.addItem(text + ".theme") # hacky, avoids re-query of dir
            index = self.comboTheme.findText(text + ".theme")
            self.comboTheme.setCurrentIndex(index)
            self.statusbar.showMessage("New Theme File Created: " + self.ThemeFile)

    def loadtheme(self):
        print "load theme"
        # if self.ThemeDir == "":
        #     self.ThemeDir = QtCore.QDir.currentPath() + "/theme/"
        #
        # print self.ThemeDir

        if self.ThemeFile == "Default" or self.ThemeFile == "":
            self.setdefaults()
            print "defaulted"
        else:
            self.loadfile()
            print self.ThemeFile + " loaded ..."


        #self.onPanelChanged()

    def loadfile(self):
        try:
            file = open(self.ThemeDir + self.ThemeFile, 'r')
            data = pickle.load(file)
            file.close()
            #print "file closed"
            self.panel = data['Panel'] # not needed
            self.fonttype = data['FontFamily']
            self.fontsize = data['FontSize']
            self.fgcolor = data['FgColor']
            self.bgcolor = data['BgColor']
            self.maxwinht = data['MaxWinHt']
            self.lineht = data['LineHt']
            # update #
            self.setall()

            self.statusbar.showMessage("Theme File Loaded: " + self.ThemeFile)

        finally:
            # create default file
            #print "no file"
            #self.setdefaults()
            return None

    def setall(self):
        print "SET ALL "
        i = self.comboPanel.currentIndex()
        ft = self.fonttype[i]
        fs = self.fontsize[i]
        lh = self.lineht[i]
        self.comboFontFamily.setCurrentFont(ft)
        self.spinFontSize.setValue(fs)
        self.spinLineHt.setValue(lh)

        i = 0
        ft = self.fonttype[i]
        fs = self.fontsize[i]
        cfg = self.fgcolor[i]
        cbg = self.bgcolor[i]
        lh = self.lineht[i]
        self.transcriptlist.settingsupdate(ft, fs, cfg, cbg)

        i = 1
        self.lookuplinedock.setMaximumHeight(self.maxwinht[i])
        self.spinMaxWinHt.setValue(self.maxwinht[i])
        ft = self.fonttype[i]
        fs = self.fontsize[i]
        cfg = self.fgcolor[i]
        cbg = self.bgcolor[i]
        lh = self.lineht[i]
        self.lookupline.settingsupdate(ft, fs, cfg, cbg)

        i = 2
        ft = self.fonttype[i]
        fs = self.fontsize[i]
        cfg = self.fgcolor[i]
        cbg = self.bgcolor[i]
        lh = self.lineht[i]
        self.vocabdock.settingsupdateEx(ft,fs,cfg,cbg,lh)

        i = 3
        ft = self.fonttype[i]
        fs = self.fontsize[i]
        cfg = self.fgcolor[i]
        cbg = self.bgcolor[i]
        lh = self.lineht[i]
        self.vocabdock.settingsupdateRe(ft,fs,cfg,cbg,lh)

        i = 4
        ft = self.fonttype[i]
        fs = self.fontsize[i]
        cfg = self.fgcolor[i]
        cbg = self.bgcolor[i]
        lh = self.lineht[i]
        self.vocabdock.settingsupdateGl(ft,fs,cfg,cbg,lh)

        i = 5
        ft = self.fonttype[i]
        fs = self.fontsize[i]
        cfg = self.fgcolor[i]
        cbg = self.bgcolor[i]
        lh = self.lineht[i]
        self.linedefs.settingsupdateEx(ft,fs,cfg,cbg,lh)

        i = 6
        ft = self.fonttype[i]
        fs = self.fontsize[i]
        cfg = self.fgcolor[i]
        cbg = self.bgcolor[i]
        lh = self.lineht[i]
        self.linedefs.settingsupdateRe(ft,fs,cfg,cbg,lh)

        i = 7
        ft = self.fonttype[i]
        fs = self.fontsize[i]
        cfg = self.fgcolor[i]
        cbg = self.bgcolor[i]
        lh = self.lineht[i]
        self.linedefs.settingsupdateGl(ft,fs,cfg,cbg,lh)

    def savetheme(self):
        print "save theme: " + self.ThemeFile
        if self.ThemeFile != "" or self.ThemeFile != "Default":
            file = open(self.ThemeDir + self.ThemeFile, 'w')
            data = {'Panel':self.panel, 'FontFamily': self.fonttype, 'FontSize': self.fontsize, 'FgColor': self.fgcolor, 'BgColor': self.bgcolor, 'MaxWinHt': self.maxwinht, 'LineHt': self.lineht}
            pickle.dump(data, file)
            file.close()
            self.statusbar.showMessage("Theme File Saved: " + self.ThemeFile)

    def setdefaults(self):
        # "Transcript List"
        # "Transcript Line Lookup"
        # "Vocabulary:Expression", "Vocabulary:Reading", "Vocabulary:Glossary"
        # "Definition:Expression", "Definition:Reading", "Definition:Glossary"

        self.fonttype = ['Meiryo','Meiryo','Meiryo','Meiryo','Meiryo','Meiryo','Meiryo','Meiryo','Meiryo','Meiryo','Meiryo']
        self.fontsize = [16,16,10,10,10,10,10,10]
        self.fgcolor = ['black','black','black','black','black','black','black','black']
        self.bgcolor = ['white','white','white','white','white','white','white','white']
        self.maxwinht = [0,90,500,500,500,500,500,500]
        self.lineht = [0,0,0,0,0,0,0,0]
        self.ThemeFile = "Default"
        self.setall()

    def onButtonColorFgClicked(self):
        color = self.fgcolor[self.comboPanel.currentIndex()]    # current color
        #color = QtGui.QColorDialog.getColor(color, self)
        color = QtGui.QColorDialog.getColor(color, self)
        self.fgcolor[self.comboPanel.currentIndex()] = color.name()   # new color
        self.onPanelChanged()

    def onButtonColorBgClicked(self):
        color = self.bgcolor[self.comboPanel.currentIndex()]    # current color
        #color = QtGui.QColorDialog.getColor(color, self)
        color = QtGui.QColorDialog.getColor(color, self)
        self.bgcolor_set = color.name()
        self.bg_set = True
        #self.bgcolor[self.comboPanel.currentIndex()] = color.name()    # new color
        self.onPanelChanged()

        #self.bgcolor[self.comboPanel.currentIndex()] = self.bgcolor_set

    def onFontFamilyChanged(self, font):
        print self.comboPanel.currentIndex()
        print str(font.family())
        self.fonttype[self.comboPanel.currentIndex()] = str(font.family())
        self.onPanelChanged()

    def onFontSizeChanged(self, size):
        self.fontsize[self.comboPanel.currentIndex()] = size
        self.onPanelChanged()

    def onPanelChanged(self):
        i = self.comboPanel.currentIndex()
        print "panel changed: " + str(i) + " " + self.comboPanel.currentText()
        if self.comboPanel.currentText() == "Transcript List":
            if self.bg_set:
                self.bgcolor[i] = self.bgcolor_set
                self.bg_set = False

            #self.comboFontFamily.setWritingSystem(QtGui.QFontDatabase.Japanese)
            #self.comboFontFamily.setWritingSystem(QtGui.QFontDatabase.TraditionalChinese)
            #self.comboFontFamily.setWritingSystem(QtGui.QFontDatabase.SimplifiedChinese)
            self.spinMaxWinHt.setDisabled(True) #visible
            #self.spinMaxWinHt.setValue(0)
            ft = self.fonttype[i]
            fs = self.fontsize[i]
            cfg = self.fgcolor[i]
            cbg = self.bgcolor[i]
            lh = self.lineht[i]
            self.spinLineHt.setValue(lh)
            self.transcriptlist.settingsupdate(ft, fs, cfg, cbg)
            print self.comboFontFamily.currentText()
            self.comboFontFamily.setCurrentFont(ft) # why isnt this Meiryo?
            self.spinFontSize.setValue(fs)


        if self.comboPanel.currentText() == "Transcript Line Lookup":
            if self.bg_set:
                self.bgcolor[i] = self.bgcolor_set
                self.bg_set = False

            #self.comboFontFamily.setWritingSystem(QtGui.QFontDatabase.Japanese)
            self.spinMaxWinHt.setDisabled(False) #visible
            self.lookuplinedock.setMaximumHeight(self.maxwinht[i])
            #self.lookuplinedock.setMinimumHeight(self.maxwinht[1]) # why doesn't this work?
            self.spinMaxWinHt.setValue(self.maxwinht[i])
            ft = self.fonttype[i]
            fs = self.fontsize[i]
            cfg = self.fgcolor[i]
            cbg = self.bgcolor[i]
            lh = self.lineht[i]
            self.spinLineHt.setValue(lh)
            self.lookupline.settingsupdate(ft, fs, cfg, cbg)

            self.comboFontFamily.setCurrentFont(ft)
            self.spinFontSize.setValue(fs)


        if self.comboPanel.currentText() == "Vocabulary:Expression":
            self.spinMaxWinHt.setDisabled(True)
            if self.bg_set:
                self.bgcolor[i] = self.bgcolor_set
                self.bgcolor[i+1] = self.bgcolor_set
                self.bgcolor[i+2] = self.bgcolor_set
                self.bg_set = False

            ft = self.fonttype[i]
            fs = self.fontsize[i]
            cfg = self.fgcolor[i]
            cbg = self.bgcolor[i]
            lh = self.lineht[i]
            self.spinLineHt.setValue(lh)
            self.vocabdock.settingsupdateEx(ft,fs,cfg,cbg,lh)
            self.comboFontFamily.setCurrentFont(ft)
            self.spinFontSize.setValue(fs)

        if self.comboPanel.currentText() == "Vocabulary:Reading":
            self.spinMaxWinHt.setDisabled(True)
            if self.bg_set:
                self.bgcolor[i] = self.bgcolor_set
                self.bgcolor[i-1] = self.bgcolor_set
                self.bgcolor[i+1] = self.bgcolor_set
                self.bg_set = False

            ft = self.fonttype[i]
            fs = self.fontsize[i]
            cfg = self.fgcolor[i]
            cbg = self.bgcolor[i]
            lh = self.lineht[i]
            self.spinLineHt.setValue(lh)
            self.vocabdock.settingsupdateRe(ft,fs,cfg,cbg,lh)
            self.comboFontFamily.setCurrentFont(ft)
            self.spinFontSize.setValue(fs)


        if self.comboPanel.currentText() == "Vocabulary:Glossary":
            self.spinMaxWinHt.setDisabled(True)
            if self.bg_set:
                self.bgcolor[i] = self.bgcolor_set
                self.bgcolor[i-1] = self.bgcolor_set
                self.bgcolor[i-2] = self.bgcolor_set
                self.bg_set = False

            ft = self.fonttype[i]
            fs = self.fontsize[i]
            cfg = self.fgcolor[i]
            cbg = self.bgcolor[i]
            lh = self.lineht[i]
            self.spinLineHt.setValue(lh)
            self.vocabdock.settingsupdateGl(ft,fs,cfg,cbg,lh)
            self.comboFontFamily.setCurrentFont(ft)
            self.spinFontSize.setValue(fs)


        if self.comboPanel.currentText() == "Definition:Expression":
            self.spinMaxWinHt.setDisabled(True)
            if self.bg_set:
                self.bgcolor[i] = self.bgcolor_set
                self.bgcolor[i+1] = self.bgcolor_set
                self.bgcolor[i+2] = self.bgcolor_set
                self.bg_set = False

            ft = self.fonttype[i]
            fs = self.fontsize[i]
            cfg = self.fgcolor[i]
            cbg = self.bgcolor[i]
            lh = self.lineht[i]
            self.spinLineHt.setValue(lh)
            self.linedefs.settingsupdateEx(ft,fs,cfg,cbg,lh)
            self.comboFontFamily.setCurrentFont(ft)
            self.spinFontSize.setValue(fs)


        if self.comboPanel.currentText() == "Definition:Reading":
            self.spinMaxWinHt.setDisabled(True)
            if self.bg_set:
                self.bgcolor[i] = self.bgcolor_set
                self.bgcolor[i-1] = self.bgcolor_set
                self.bgcolor[i+1] = self.bgcolor_set
                self.bg_set = False

            ft = self.fonttype[i]
            fs = self.fontsize[i]
            cfg = self.fgcolor[i]
            cbg = self.bgcolor[i]
            lh = self.lineht[i]
            self.spinLineHt.setValue(lh)
            self.linedefs.settingsupdateRe(ft,fs,cfg,cbg,lh)
            self.comboFontFamily.setCurrentFont(ft)
            self.spinFontSize.setValue(fs)


        if self.comboPanel.currentText() == "Definition:Glossary":
            self.spinMaxWinHt.setDisabled(True)
            if self.bg_set:
                self.bgcolor[i] = self.bgcolor_set
                self.bgcolor[i-1] = self.bgcolor_set
                self.bgcolor[i-2] = self.bgcolor_set
                self.bg_set = False

            ft = self.fonttype[i]
            fs = self.fontsize[i]
            cfg = self.fgcolor[i]
            cbg = self.bgcolor[i]
            lh = self.lineht[i]
            self.spinLineHt.setValue(lh)
            self.linedefs.settingsupdateGl(ft,fs,cfg,cbg,lh)
            self.comboFontFamily.setCurrentFont(ft)
            self.spinFontSize.setValue(fs)

    def onWinHtChanged(self):
        self.maxwinht[1] = self.spinMaxWinHt.value()
        self.lookuplinedock.setMaximumHeight(self.maxwinht[1])

    def onLineHtChanged(self):
        self.lineht[self.comboPanel.currentIndex()] = self.spinLineHt.value()
        self.onPanelChanged()

    def setupUI(self):
        vlayout = QtGui.QVBoxLayout()

        hlayoutTheme = QtGui.QHBoxLayout()        #  theme
        hlayoutPanel = QtGui.QHBoxLayout()        # panel
        hlayoutWinHt = QtGui.QHBoxLayout()        # WinHt
        hlayoutSaveReset = QtGui.QHBoxLayout()    # save reset

        # settings profile (load)
        self.labelTheme = QtGui.QLabel()
        self.labelTheme.setText(" Theme: ")
        self.labelTheme.setSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)

        hlayoutTheme.addWidget(self.labelTheme)

        self.comboTheme = QtGui.QComboBox()
        #self.comboTheme.addItem("Default")
        self.populatecombo("theme", self.comboTheme, self.ThemeDir, "Theme")
        self.comboTheme.setCurrentIndex(self.comboTheme.findText(self.ThemeFile))
        self.comboTheme.currentIndexChanged.connect(self.settheme)

        hlayoutTheme.addWidget(self.comboTheme)

        self.buttonThemeFolder = QtGui.QPushButton()
        self.buttonThemeFolder.setText("+")
        self.buttonThemeFolder.setMaximumWidth(50)
        hlayoutTheme.addWidget(self.buttonThemeFolder)
        self.buttonThemeFolder.clicked.connect(self.showDialogThemeFolder)

        self.buttonThemeCreate = QtGui.QPushButton()
        self.buttonThemeCreate.setText("Create")
        self.buttonThemeCreate.setMaximumWidth(50)
        hlayoutTheme.addWidget(self.buttonThemeCreate)
        self.buttonThemeCreate.clicked.connect(self.createtheme)
        #self.buttonThemeCreate.setDisabled(True)

        self.buttonThemeDelete = QtGui.QPushButton()
        self.buttonThemeDelete.setText("Delete")
        self.buttonThemeDelete.setMaximumWidth(50)
        hlayoutTheme.addWidget(self.buttonThemeDelete)
        #self.buttonThemeDelete.clicked.connect(self.showDialogTheme)

        vlayout.addLayout(hlayoutTheme)

        # combo set panel
        self.comboPanel = QtGui.QComboBox()
        self.comboPanel.addItems(self.panel)
        self.comboPanel.currentIndexChanged.connect(self.onPanelChanged)
        hlayoutPanel.addWidget(self.comboPanel)

        # combo set font
        self.comboFontFamily = QtGui.QFontComboBox()
        self.comboFontFamily.currentFontChanged.connect(self.onFontFamilyChanged)
        hlayoutPanel.addWidget(self.comboFontFamily)

        # spin font-size
        self.spinFontSize = QtGui.QSpinBox()
        self.spinFontSize.valueChanged.connect(self.onFontSizeChanged)
        hlayoutPanel.addWidget(self.spinFontSize)

        # button fg
        self.buttonColorFg = QtGui.QPushButton()
        self.buttonColorFg.clicked.connect(self.onButtonColorFgClicked)
        self.buttonColorFg.setText("Fg Color")
        self.buttonColorFg.setMaximumWidth(50)
        hlayoutPanel.addWidget(self.buttonColorFg)

        vlayout.addLayout(hlayoutPanel)

        # (max win ht, bg color) spacer label spin button
        self.spacerMaxWinHt = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        hlayoutWinHt.addItem(self.spacerMaxWinHt) #, QtCore.Qt.Horizontal)

        self.labelLineHt = QtGui.QLabel()
        self.labelLineHt.setText("Line Height: ")
        self.labelLineHt.setSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        hlayoutWinHt.addWidget(self.labelLineHt)
        self.labelLineHt.setVisible(False)

        self.spinLineHt = QtGui.QSpinBox()
        self.spinLineHt.setMaximum(20)
        self.spinLineHt.setMinimum(0)
        #self.spinLineHt.setDisabled(True)
        self.spinLineHt.setValue(0)
        self.spinLineHt.valueChanged.connect(self.onLineHtChanged)
        hlayoutWinHt.addWidget(self.spinLineHt)
        self.spinLineHt.setVisible(False)

        self.labelMaxWinHt = QtGui.QLabel()
        self.labelMaxWinHt.setText("Max Win Height: ")
        self.labelMaxWinHt.setSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        hlayoutWinHt.addWidget(self.labelMaxWinHt)

        self.spinMaxWinHt = QtGui.QSpinBox()
        self.spinMaxWinHt.setMaximum(500)
        self.spinMaxWinHt.setMinimum(80)
        self.spinMaxWinHt.setDisabled(True)
        self.spinMaxWinHt.setValue(0)
        self.spinMaxWinHt.valueChanged.connect(self.onWinHtChanged)
        hlayoutWinHt.addWidget(self.spinMaxWinHt)

        self.buttonColorBg = QtGui.QPushButton()
        self.buttonColorBg.clicked.connect(self.onButtonColorBgClicked)
        self.buttonColorBg.setText("Bg Color")
        self.buttonColorBg.setMaximumWidth(50)
        hlayoutWinHt.addWidget(self.buttonColorBg)

        vlayout.addLayout(hlayoutWinHt)

        # button ok cancel
        self.spacerSaveCancel = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        hlayoutSaveReset.addItem(self.spacerSaveCancel)

        self.buttonSave = QtGui.QPushButton()
        self.buttonReset = QtGui.QPushButton()
        self.buttonSave.clicked.connect(self.savetheme)
        self.buttonReset.clicked.connect(self.loadtheme)
        self.buttonSave.setText("Save")
        self.buttonReset.setText("Reset")

        #QtGui.QDialogButtonBox()

        hlayoutSaveReset.addWidget(self.buttonSave)
        hlayoutSaveReset.addWidget(self.buttonReset)
        vlayout.addLayout(hlayoutSaveReset)


        self.spacerPushUp = QtGui.QSpacerItem(1, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        vlayout.addItem(self.spacerPushUp)

        self.setLayout(vlayout)


#######################################################################################################

        # hlayoutSessionFile = QtGui.QHBoxLayout()
        # hlayoutVideoFolder = QtGui.QHBoxLayout()
        # hlayoutTranscrFolder = QtGui.QHBoxLayout()
        # hlayoutDefFolder = QtGui.QHBoxLayout()

        #### OVER ENGINEERING TIME ####
        # # session file: label combo button
        # self.labelSessionFile = QtGui.QLabel()
        # self.labelSessionFile.setText("Session File: ")
        # self.labelSessionFile.setSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        #
        # hlayoutSessionFile.addWidget(self.labelSessionFile)
        #
        # self.comboSessionFile = QtGui.QComboBox()
        # self.comboSessionFile.addItem("Default")
        # hlayoutSessionFile.addWidget(self.comboSessionFile)
        #
        # self.buttonSessionFileFolder = QtGui.QPushButton()
        # self.buttonSessionFileFolder.setText("+")
        # self.buttonSessionFileFolder.setMaximumWidth(50)
        # hlayoutSessionFile.addWidget(self.buttonSessionFileFolder)
        # #self.buttonSessionFileFolder.clicked.connect(self.showDialogSessionFile)
        #
        # vlayout.addLayout(hlayoutSessionFile)
        #
        # #horizLine1 = QtGui.QLin
        #
        # # video folder
        # self.spacerVideoFolder1 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        # hlayoutVideoFolder.addItem(self.spacerVideoFolder1) #, QtCore.Qt.Horizontal)
        #
        # self.labelVideoFolder = QtGui.QLabel()
        # self.labelVideoFolder.setText("Video Folder: ")
        # #self.labelVideoFolder.setSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        # self.labelVideoFolder.setMinimumWidth(700)
        # self.labelVideoFolder.setSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        # hlayoutVideoFolder.addWidget(self.labelVideoFolder)
        #
        # #self.spacerVideoFolder2 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        # #hlayoutVideoFolder.addItem(self.spacerVideoFolder2) #, QtCore.Qt.Horizontal)
        #
        # self.comboVideoFolder = QtGui.QComboBox()
        # self.comboVideoFolder.addItem("Default")
        # #self.comboVideoFolder.setMinimumWidth(300)
        # self.comboVideoFolder.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        # hlayoutVideoFolder.addWidget(self.comboVideoFolder)
        #
        # self.buttonVideoFolder = QtGui.QPushButton()
        # self.buttonVideoFolder.setText("+")
        # self.buttonVideoFolder.setMaximumWidth(50)
        # hlayoutVideoFolder.addWidget(self.buttonVideoFolder)
        # #self.buttonVideoFolder.clicked.connect(self.showDialogVideoFolder)
        #
        # vlayout.addLayout(hlayoutVideoFolder)
        #
        # # transcr folder
        # self.spacerTranscrFolder1 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        # hlayoutTranscrFolder.addItem(self.spacerTranscrFolder1) #, QtCore.Qt.Horizontal)
        #
        # self.labelTranscrFolder = QtGui.QLabel()
        # self.labelTranscrFolder.setText("Transcript Folder: ")
        # self.labelTranscrFolder.setSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        # self.labelVideoFolder.setMinimumWidth(80)
        # hlayoutTranscrFolder.addWidget(self.labelTranscrFolder)
        #
        # #self.spacerTranscrFolder2 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        # #hlayoutTranscrFolder.addItem(self.spacerTranscrFolder2) #, QtCore.Qt.Horizontal)
        #
        # self.comboTranscrFolder = QtGui.QComboBox()
        # self.comboTranscrFolder.addItem("Default")
        # #self.comboVideoFolder.setMinimumWidth(80)
        # self.comboTranscrFolder.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        # hlayoutTranscrFolder.addWidget(self.comboTranscrFolder)
        #
        # self.buttonTranscrFolder = QtGui.QPushButton()
        # self.buttonTranscrFolder.setText("+")
        # self.buttonTranscrFolder.setMaximumWidth(50)
        # hlayoutTranscrFolder.addWidget(self.buttonTranscrFolder)
        # #self.buttonVideoFolder.clicked.connect(self.showDialogVideoFolder)
        #
        # vlayout.addLayout(hlayoutTranscrFolder)
        #
        # # def folder
        # self.spacerDefFolder1 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        # hlayoutDefFolder.addItem(self.spacerDefFolder1) #, QtCore.Qt.Horizontal)
        #
        # self.labelDefFolder = QtGui.QLabel()
        # self.labelDefFolder.setText("Definition Folder: ")
        # self.labelDefFolder.setSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        # self.labelDefFolder.setMinimumWidth(80)
        # hlayoutDefFolder.addWidget(self.labelDefFolder)
        #
        # #self.spacerDefFolder2 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        # #hlayoutDefFolder.addItem(self.spacerDefFolder2) #, QtCore.Qt.Horizontal)
        #
        # self.comboDefFolder = QtGui.QComboBox()
        # self.comboDefFolder.addItem("Default")
        # #self.comboVideoFolder.setMinimumWidth(300)
        # self.comboDefFolder.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        # hlayoutDefFolder.addWidget(self.comboDefFolder)
        #
        # self.buttonDefFolder = QtGui.QPushButton()
        # self.buttonDefFolder.setText("+")
        # self.buttonDefFolder.setMaximumWidth(50)
        # hlayoutDefFolder.addWidget(self.buttonDefFolder)
        # #self.buttonVideoFolder.clicked.connect(self.showDialogVideoFolder)
        #
        # vlayout.addLayout(hlayoutDefFolder)
        #

#######################################################################################################
