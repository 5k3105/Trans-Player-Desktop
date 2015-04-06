#!/usr/bin/env python2
# -*- coding: utf-8 -*-

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

import yomi_base.reader_util
import sys, pysrt, pickle, os, ass
from PySide import QtCore
from PySide.QtGui import *
from yomi_base.settings import cSettings
from yomi_base.minireader import MiniReader
from PySide.phonon import Phonon

class cSubsList(QListWidget):
    def __init__(self, settings):
        super(cSubsList, self).__init__()
        self.ext = ""
        self.bgColor = "white" #QColor('white')

    def settingsupdate(self, ft, fs, cfg, cbg):
        # palette = self.palette()
        # palette.setColor(QPalette.Base, QColor(cbg))
        # palette.setColor(QPalette.Text, QColor(cfg))
        # self.setPalette(palette)
        self.bgColor = cbg

        font = QFont()
        font.setPointSize(fs)
        font.setFamily(ft)
        #self.setFont(font)

        for i in xrange(self.count()):
            self.item(i).setFont(font)
            self.item(i).setForeground(QColor(cfg))
            self.item(i).setBackground(QColor(cbg))


    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            if qp.player.state() == Phonon.PausedState:
                qp.player.play()
            else:
                qp.player.pause()

        if event.key() == QtCore.Qt.Key_Right:
            time = qp.player.currentTime()
            time += 5000
            qp.player.seek(time)

        if event.key() == QtCore.Qt.Key_Left:
            time = qp.player.currentTime()
            time -= 5000
            qp.player.seek(time)

    def loadSubsSrt(self, file):
        self.subs = pysrt.open(file, encoding='utf-8')

        self.clear()
        g = 0
        for i in self.subs:
            self.insertItem(g, i.text)
            g = g + 1

        for i in xrange(self.count()):
            self.item(i).setFont(QFont('Meiryo', 16))  # MS Mincho

        # back up 1:33
        # self.subs.shift(seconds=-30) # Move all subs 2 seconds earlier
        #self.subs.shift(minutes=-1)  # Move all subs 1 minutes later
        #self.subs.shift(milliseconds=-500 )

        i = self.subs[0]
        self.currentSubStart = i.start.ordinal
        self.currentSubEnd = i.end.ordinal
        self.currentRow = 0
        i = self.subs[1]
        self.nextSubStart = i.start.ordinal
        self.nextSubEnd = i.end.ordinal

    def gotoLineSrt(self):
        self.item(self.currentRow).setBackground(QColor(self.bgColor))#QColor('white'))

        g = self.currentIndex()
        self.currentRow = g.row()
        i = self.subs[g.row()]
        self.currentSubStart = i.start.ordinal
        self.currentSubEnd = i.end.ordinal
        qp.player.seek(self.currentSubStart)
        i = self.subs[g.row() + 1]
        self.nextSubStart = i.start.ordinal
        self.nextSubEnd = i.end.ordinal

        lookupLine.setPlainText(self.subs[g.row()].text)
        LineDefs.lookup(self.currentRow)


    def loadSubsAss(self, file):
        with open(file, "r") as f:
             self.subs = ass.parse(f).events

        self.clear()
        g = 0
        # for i in self.subs:
        #     if i.style not in "ED,OP,staff": #*Default": #
        #         self.insertItem(g, i.text.decode('utf_8'))
        #         g = g + 1
        for i in self.subs:
            self.insertItem(g, i.text.decode('utf_8'))
            g = g + 1

        for i in xrange(self.count()):
            self.item(i).setFont(QFont('Meiryo', 16))  # MS Mincho

        i = self.subs[0]
        self.currentSubStart = i.start.total_seconds() * 1000# + i.start.microseconds
        self.currentSubEnd = i.end.total_seconds() * 1000# + i.end.microseconds
        self.currentRow = 0
        i = self.subs[1]
        self.nextSubStart = i.start.total_seconds() * 1000# + i.start.microseconds
        self.nextSubEnd = i.end.total_seconds() * 1000# + i.end.microseconds

    def gotoLineAss(self):
        self.item(self.currentRow).setBackground(self.bgColor)#QColor('white'))

        g = self.currentIndex()
        self.currentRow = g.row()
        i = self.subs[g.row()]
        self.currentSubStart = i.start.total_seconds() * 1000# + i.start.microseconds
        self.currentSubEnd = i.end.total_seconds() * 1000# + i.end.microseconds
        qp.player.seek(self.currentSubStart)
        i = self.subs[g.row() + 1]
        self.nextSubStart = i.start.total_seconds() * 1000# + i.start.microseconds
        self.nextSubEnd = i.end.total_seconds() * 1000# + i.end.microseconds

        lookupLine.setPlainText(self.subs[g.row()].text.decode('utf_8'))

        LineDefs.lookup(self.currentRow)

    def loadSubs(self, file):
        _, fileExtension = os.path.splitext(file)
        #print fileExtension -- loaded twice?
        if fileExtension == ".srt":
            self.loadSubsSrt(file)
            self.ext = ".srt"
        if fileExtension == ".ass":
            self.loadSubsAss(file)
            self.ext = ".ass"

    def gotoLine(self):
        if self.ext == ".srt":
            self.gotoLineSrt()
        if self.ext == ".ass":
            self.gotoLineAss()

class QPlayer(QWidget):
    def __init__(self, settings):
        super(QPlayer, self).__init__()
        self.audioOuptut = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.player = Phonon.MediaObject(self)
        Phonon.createPath(self.player, self.audioOuptut)

        self.videoWidget = cVideoWidget()
        Phonon.createPath(self.player, self.videoWidget)

        self.player.setTickInterval(500)  #1000
        self.connect(self.player, QtCore.SIGNAL("tick(qint64)"), self.tick)

        self.seekSlider = Phonon.SeekSlider(self.player, self)
        self.volumeSlider = Phonon.VolumeSlider(self.audioOuptut, self)
        #self.volumeSlider.setMaximumVolume(0.35)

        self.buildGUI()
        self.setupConnections()
        self.init = True # used to test before loading file when PLAY is pushed

        # load a subtitle test
        #self.mediaobject = Phonon.MediaObject()
        #self.mediacontroller = Phonon.MediaController(self.mediaobject)

        #fn = "G:\Documents and Settings\\5k3105\Desktop\\anime\sidonia\\"
        #self.player.setCurrentSubtitle(fn + "timed for [Underwater] release Shidonia_No_Kishi_001.srt")

    def buildGUI(self):

        self.fileEdit = ""
        self.lcdTimer = QLCDNumber()
        self.lcdTimer.display("00:00")

        self.playButton = QPushButton("Play")
        self.playButton.setIcon(QIcon(":/images/play.png"))
        self.playButton.setEnabled(True)

        self.pauseButton = QPushButton("Pause")
        self.pauseButton.setIcon(QIcon(":/images/pause.png"))

        self.stopButton = QPushButton("Stop")
        self.stopButton.setIcon(QIcon(":/images/stop.png"))

        midLayout = QHBoxLayout()
        midLayout.addWidget(self.seekSlider)
        midLayout.addWidget(self.lcdTimer)

        lowerLayout = QHBoxLayout()
        lowerLayout.addWidget(self.playButton)
        lowerLayout.addWidget(self.pauseButton)
        lowerLayout.addWidget(self.stopButton)
        lowerLayout.addWidget(self.volumeSlider)

        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)
        layout.addLayout(midLayout)
        layout.addLayout(lowerLayout)

        self.setLayout(layout)
        self.lcdTimer.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.seekSlider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.volumeSlider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)


    def setupConnections(self):
        self.playButton.clicked.connect(self.playClicked)
        self.pauseButton.clicked.connect(self.pauseClicked)
        self.stopButton.clicked.connect(self.stopClicked)

        #self.videoWidget.keyPressed.connect(self.fullScreenButton)
        #self.mController.availableSubtitlesChanged.connect(self.subsChanged)
        #self.videoWidget.stateChanged.connect(self.vidStateChanged)

    def tick(self, time):  # transcript list hi-lite following
        displayTime = QtCore.QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        self.lcdTimer.display(displayTime.toString('mm:ss'))
        """
        print "time             : ", time
        print
        print ">current row     : ", w.currentRow
        print " currentSubStart : ", w.currentSubStart
        print " currentSubEnd   : ", w.currentSubEnd
        print " nextSubStart    : ", w.nextSubStart
        print " nextSubEnd      : ", w.nextSubEnd
        print "***************"
        """

        if time > subsList.currentSubEnd:
            subsList.item(subsList.currentRow).setBackground(QColor('grey'))

        if time > subsList.nextSubStart:

            if subsList.ext == ".srt":
                subsList.currentRow = subsList.currentRow + 1
                i = subsList.subs[subsList.currentRow]
                subsList.currentSubStart = i.start.ordinal
                subsList.currentSubEnd = i.end.ordinal
                n = subsList.subs[subsList.currentRow + 1]
                subsList.nextSubStart = n.start.ordinal
                subsList.nextSubEnd = n.end.ordinal

            if subsList.ext == ".ass":
                subsList.currentRow = subsList.currentRow + 1
                i = subsList.subs[subsList.currentRow]
                subsList.currentSubStart = i.start.total_seconds() * 1000# + i.start.microseconds
                subsList.currentSubEnd = i.end.total_seconds() * 1000# + i.end.microseconds
                n = subsList.subs[subsList.currentRow + 1]
                subsList.nextSubStart = n.start.total_seconds() * 1000# + n.start.microseconds
                subsList.nextSubEnd = n.end.total_seconds() * 1000# + n.end.microseconds
                #print str(n.end.total_seconds()) + " : " + str(n.end.microseconds)

            subsList.item(subsList.currentRow - 1).setBackground(QColor('white'))
            subsList.item(subsList.currentRow).setBackground(QColor('red'))

            # browser text
            # w.body.appendInside("<span>" + w.subs[w.currentRow].text + "</span>")
            #w.span.setPlainText( w.subs[w.currentRow].text)

            #scroll to option. should center current item in list though.
            subsList.ScrollHint = QAbstractItemView.EnsureVisible
            subsList.scrollToItem(subsList.item(subsList.currentRow), subsList.ScrollHint)

            # Update LineDefs panel
            LineDefs.lookup(subsList.currentRow)


    def playClicked(self):  # Set video file at first play click
        if self.init:
            self.player.setCurrentSource(Phonon.MediaSource(self.fileEdit))
            self.init = False
        self.player.play()

    def pauseClicked(self):
        self.player.pause()

    def stopClicked(self):
        self.player.stop()
        self.lcdTimer.display("00:00")

    def browseClicked(self): #$
        f, _ = QFileDialog.getOpenFileName(self)
        if f != "":
            self.fileEdit.setText(f)

    def checkFileName(self, s): #$
        if s != "":
            self.playButton.setEnabled(True)
        else:
            self.playButton.setEnabled(False)

class cVideoWidget(Phonon.VideoWidget):
    def __init__(self):
        super(cVideoWidget, self).__init__()
        self.FS = False

    def mouseDoubleClickEvent(self, event):  # Fullscreen toggle
        if self.FS == True:
            self.exitFullScreen()
            self.FS = False
        else:
            self.enterFullScreen()
            self.FS = True

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:  # Exit fullscreen
            if self.FS == True:
                self.exitFullScreen()
                self.FS = False
            else:
                self.enterFullScreen()
                self.FS = True

        if event.key() == QtCore.Qt.Key_Space:  # Pause with space
            if qp.player.state() == Phonon.PausedState:
                qp.player.play()
            else:
                qp.player.pause()

        if event.key() == QtCore.Qt.Key_Right:
            time = qp.player.currentTime()
            time += 5000
            qp.player.seek(time)

        if event.key() == QtCore.Qt.Key_Left:
            time = qp.player.currentTime()
            time -= 5000
            qp.player.seek(time)

class cDockKanji(QDockWidget):
    def __init__(self):
        super(cDockKanji, self).__init__()

        self.dockWidgetContents = QWidget()

        self.verticalLayout = QVBoxLayout(self.dockWidgetContents)

        self.textKanjiDefs = QTextBrowser(self.dockWidgetContents)
        self.textKanjiDefs.setAcceptDrops(False)
        self.textKanjiDefs.setOpenLinks(False)

        self.verticalLayout.addWidget(self.textKanjiDefs)
        self.horizontalLayout = QHBoxLayout()

        self.label = QLabel(self.dockWidgetContents)

        self.horizontalLayout.addWidget(self.label)
        self.textKanjiSearch = QLineEdit(self.dockWidgetContents)

        self.horizontalLayout.addWidget(self.textKanjiSearch)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.setWidget(self.dockWidgetContents)
        self.setWindowTitle("Kanji")

class cDockVocab(QDockWidget):
    def __init__(self, settings):
        super(cDockVocab, self).__init__()

        #self.dockWidgetContents = QWidget()
        #self.verticalLayout = QVBoxLayout(self.dockWidgetContents)
        self.textVocabDefs = QTextBrowser()#self.dockWidgetContents)
        self.textVocabDefs.setAcceptDrops(False)
        self.textVocabDefs.setOpenLinks(False)
        self.setWidget(self.textVocabDefs)
        #self.verticalLayout.addWidget(self.textVocabDefs)

        # self.horizontalLayout = QHBoxLayout()
        # self.label = QLabel(self.dockWidgetContents)
        # self.horizontalLayout.addWidget(self.label)
        # self.textVocabSearch = QLineEdit(self.dockWidgetContents)
        # self.horizontalLayout.addWidget(self.textVocabSearch)
        # self.verticalLayout.addLayout(self.horizontalLayout)

        #self.setWidget(self.dockWidgetContents)
        self.setWindowTitle("Vocabulary")
        self.bg = "black"
        self.eft = 12
        self.efs = "black"
        self.efg = "black"
        self.rft = "black"
        self.rfs = 12
        self.rfg = "black"
        self.gft = "black"
        self.gfs = 12
        self.gfg = "black"
        self.elh = 0
        self.rlh = 0
        self.glh = 0

    def settingsupdateEx(self, eft, efs, efg, bg, elh):
        self.eft = eft
        self.efs = efs
        self.efg = efg
        self.bg = bg
        self.elh = elh
        lookupLine.updateVocabDefs()

    def settingsupdateRe(self, rft, rfs, rfg, bg, rlh):
        self.rft = rft
        self.rfs = rfs
        self.rfg = rfg
        self.bg = bg
        self.rlh = rlh
        lookupLine.updateVocabDefs()

    def settingsupdateGl(self, gft, gfs, gfg, bg, glh):
        self.gft = gft
        self.gfs = gfs
        self.gfg = gfg
        self.bg = bg
        self.glh = glh
        lookupLine.updateVocabDefs()

    def buildDefHeader(self):

        return u"""
                <html><head><style>
                body {{ background-color: {0} }}
                span.expression {{ font-size: {1}px; font-family: '{2}'; color: {3}; line-height: {10}px }}
                span.reading {{ font-size: {4}px; font-family: '{5}'; color: {6}; line-height: {11}px }}
                span.glossary {{ font-size: {7}px; font-family: '{8}'; color: {9}; line-height: {12}px }}
                </style></head><body>""".format(self.bg, self.efs, self.eft, self.efg, self.rfs, self.rft, self.rfg, self.gfs, self.gft, self.gfg, self.elh, self.rlh, self.glh) #+ html + "</body></html>"

    def buildDefFooter(self):
        return '</body></html>'


    def buildEmpty(self):
        return u"""
            <p>No definitions to display.</p>
            <p>Mouse over text with the <em>middle mouse button</em> or <em>shift key</em> pressed to search.</p>
            <p>You can also also input terms in the search box below."""


    def buildVocabDef(self, definition, index, query):
        reading = unicode()
        if definition['reading']:
            reading = u'<span class = "reading">[{0}]<br/></span>'.format(definition['reading'])

        rules = unicode()
        if len(definition['rules']) > 0:
            rules = ' &lt; '.join(definition['rules'])
            rules = '<span class = "rules">({0})<br/></span>'.format(rules)

        links = '<a href = "copyVocabDef:{0}"><img src = "img/icon_add_expression.png" align = "right"/></a>'.format(index)
        if query is not None:
            if query('vocab', yomi_base.reader_util.markupVocabExp(definition)):
                links += '<a href = "addVocabExp:{0}"><img src = "://img/img/icon_add_expression.png" align = "right"/></a>'.format(index)
            if query('vocab', yomi_base.reader_util.markupVocabReading(definition)):
                links += '<a href = "addVocabReading:{0}"><img src = "://img/img/icon_add_reading.png" align = "right"/></a>'.format(index)

        html = u"""
            <span class = "links">{0}</span>
            <span class = "expression">{1}<br/></span>
            {2}
            <span class = "glossary">{3}<br/></span>
            {4}
            <br clear = "all"/>""".format(links, definition['expression'], reading, definition['glossary'], rules)
        #print html
        return html


    def buildVocabDefs(self, definitions, query):
        html = self.buildDefHeader()
        if len(definitions) > 0:
            for i, definition in enumerate(definitions):
                html += self.buildVocabDef(definition, i, query)
        else:
            html += self.buildEmpty()

        return html + self.buildDefFooter()


    def buildKanjiDef(self, definition, index, query):
        links = '<a href = "copyKanjiDef:{0}"><img src = "://img/img/icon_copy_definition.png" align = "right"/></a>'.format(index)
        if query is not None and query('kanji', yomi_base.reader_util.markupKanji(definition)):
            links += '<a href = "addKanji:{0}"><img src = "://img/img/icon_add_expression.png" align = "right"/></a>'.format(index)

        readings = ', '.join([definition['kunyomi'], definition['onyomi']])
        html = u"""
            <span class = "links">{0}</span>
            <span class = "expression">{1}<br/></span>
            <span class = "reading">[{2}]<br/></span>
            <span class = "glossary">{3}<br/></span>
            <br clear = "all"/>""".format(links, definition['character'], readings, definition['glossary'])

        return html


    def buildKanjiDefs(self, definitions, query):
        html = self.buildDefHeader()

        if len(definitions) > 0:
            for i, definition in enumerate(definitions):
                html += self.buildKanjiDef(definition, i, query)
        else:
            html += self.buildEmpty()

        return html + self.buildDefFooter()

class cDockDirSelect(QDockWidget):
    def __init__(self, session):
        super(cDockDirSelect, self).__init__()

        self.dockWidgetContents = QWidget()
        self.horizontalLayout = QHBoxLayout(self.dockWidgetContents)
        self.dockWidgetContents.setLayout(self.horizontalLayout)

        self.comboVideo = QComboBox(self.dockWidgetContents)
        self.horizontalLayout.addWidget(self.comboVideo)
        self.btnVideo = QPushButton(self.dockWidgetContents)
        #self.btnVideo.setIcon(QIcon(QtCore.QDir.currentPath() + "/img/icon_action_open.png"))
        self.btnVideo.setText("+")
        self.horizontalLayout.addWidget(self.btnVideo)
        self.btnVideo.clicked.connect(self.showDialogV)

        self.comboTranscr = QComboBox(self.dockWidgetContents)
        self.horizontalLayout.addWidget(self.comboTranscr)
        self.btnTranscr = QPushButton(self.dockWidgetContents)
        self.btnTranscr.setText("+")
        self.horizontalLayout.addWidget(self.btnTranscr)
        self.btnTranscr.clicked.connect(self.showDialogT)

        self.comboDefs = QComboBox(self.dockWidgetContents)
        self.horizontalLayout.addWidget(self.comboDefs)
        self.btnDefs = QPushButton(self.dockWidgetContents)
        self.btnDefs.setText("+")
        self.horizontalLayout.addWidget(self.btnDefs)
        self.btnDefs.clicked.connect(self.showDialogD)

        # enable Load/Save when file selected, set linedefs.filename
        self.comboDefs.editTextChanged.connect(self.setdefsfile)

        self.btnVideo.setMaximumWidth(35)
        self.btnTranscr.setMaximumWidth(35)
        self.btnDefs.setMaximumWidth(35)

        # load save create ... SETTINGS
        #self.btnLoad = QPushButton(self.dockWidgetContents)
        #self.btnLoad.setText("Load")
        #self.horizontalLayout.addWidget(self.btnLoad)
        #self.btnLoad.clicked.connect(LineDefs.loaddefs)
        #self.btnLoad.setDisabled(True)

        self.btnSave = QPushButton(self.dockWidgetContents)
        self.btnSave.setText("Save Def")
        self.horizontalLayout.addWidget(self.btnSave)
        self.btnSave.clicked.connect(LineDefs.savedefs)
        self.btnSave.setDisabled(True)

        self.btnCreate = QPushButton(self.dockWidgetContents)
        self.btnCreate.setText("Create Def")
        self.horizontalLayout.addWidget(self.btnCreate)
        self.btnCreate.clicked.connect(LineDefs.createdefs)
        self.btnCreate.setDisabled(True)

        self.btnSettings = QPushButton(self.dockWidgetContents)
        self.btnSettings.setText("Settings")
        self.horizontalLayout.addWidget(self.btnSettings)
        self.btnSettings.clicked.connect(self.settingsPanel)
        self.btnSettings.setDisabled(False)

        self.btnSettings.setMaximumWidth(90)
        self.btnSave.setMaximumWidth(90)
        self.btnCreate.setMaximumWidth(90)

        self.setWidget(self.dockWidgetContents)
        self.setWindowTitle("Directory Select")
        self.setMinimumHeight(50)

        self.comboVideoDir = session.VideoDir
        self.comboVideo.currentIndexChanged.connect(self.setvideofile)

        self.comboTranscrDir = session.TranscrDir
        self.comboTranscr.currentIndexChanged.connect(self.settranscrfile)

        self.comboDefsDir = session.DefsDir
        self.comboDefs.currentIndexChanged.connect(self.setdefsfile)

        if self.comboDefsDir <> "":
            self.populatecombo("tdef", self.comboDefs, self.comboDefsDir, "Definitions")
        if self.comboTranscrDir <> "":
            self.populatecombo("srt,ass", self.comboTranscr, self.comboTranscrDir, "Transcript")
        if self.comboVideoDir <> "":
            self.populatecombo("mp4,mkv", self.comboVideo, self.comboVideoDir, "Video")

        self.comboDefs.setCurrentIndex(self.comboDefs.findText(session.DefsFile))
        self.comboTranscr.setCurrentIndex(self.comboTranscr.findText(session.TranscrFile))
        self.comboVideo.setCurrentIndex(self.comboVideo.findText(session.VideoFile))

        self.settranscrfile()
        self.setvideofile()
        self.setdefsfile()


    def settingsPanel(self):
        if dockSettings.isVisible():
            dockSettings.setVisible(False)
        else:
            dockSettings.setVisible(True)
            #w.tabifyDockWidget(dockSettings, dockVideo)
            # setfocus

    def setvideofile(self):
        if self.comboVideo.currentText() != "":
            qp.init = True  # reset video source
            qp.fileEdit = self.comboVideoDir + "/" + self.comboVideo.currentText()
            statusbar.showMessage("Video File Loaded: " + qp.fileEdit)

    def settranscrfile(self):
        if self.comboTranscr.currentText() != "":
            fn = self.comboTranscrDir + "/" + self.comboTranscr.currentText()
            subsList.loadSubs(fn)
            statusbar.showMessage("Transcript File Loaded: " + fn)

    def setdefsfile(self):
        if self.comboDefs.currentText() != "":
            LineDefs.filename = self.comboDefsDir + "/" + self.comboDefs.currentText()
            #self.btnLoad.setDisabled(False)
            self.btnSave.setDisabled(False)
            LineDefs.loaddefs()

    def showDialogV(self):
        self.showdialog("mp4,mkv", self.comboVideo,"Video")

    def showDialogT(self):
        self.showdialog("ass,srt",self.comboTranscr, "Transcript")

    def showDialogD(self): # Definitions
        self.showdialog("tdef", self.comboDefs, "Definitions")

    def showdialog(self, filter, combo, text):
        # open file dialog, get folder, add folder files to combobox
        # set basedir, enable Create button
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        dirNames = QFileDialog.getOpenFileName
        if dialog.exec_():
            dirNames = dialog.selectedFiles()
            self.populatecombo(filter, combo, dirNames[0], text)

            if text == "Video":
               self.comboVideoDir = dirNames[0]
            if text == "Transcript":
                self.comboTranscrDir = dirNames[0]
            if text == "Definitions":
                self.comboDefsDir = dirNames[0]

    def populatecombo(self, filter, combo, dir, text):
        onlyfiles = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
        files = list()
        for x in onlyfiles:
            if x.split(".")[-1] in filter :
                files.append(x)

        combo.clear()
        combo.addItem("")
        combo.addItems(files)

        if text == "Definitions":
            LineDefs.basedir = dir
            self.btnCreate.setDisabled(False)

        statusbar.showMessage(text + " Folder set to: " + dir)

class cLineDefs(QTextBrowser):
    def __init__(self, settings):
        super(cLineDefs, self).__init__()
        self.TranscriptLine = list()
        self.Expression = list()
        self.Reading = list()
        self.Glossary = list()
        self.Result = ""
        self.filename = ""
        self.basedir = ""
        # font = QFont()
        # font.setPointSize(16)
        # self.setFont(font)

        self.setAcceptDrops(False)
        self.setOpenLinks(False)
        self.anchorClicked.connect(self.onDefsAnchorClicked)
        self.bg = "white"
        self.eft = "Meiryo"
        self.efs = 10
        self.efg = "black"
        self.rft = "Meiryo"
        self.rfs = 15
        self.rfg = "black"
        self.gft = "courier"
        self.gfs = 20
        self.gfg = "green"
        self.elh = 0
        self.rlh = 0
        self.glh = 0

    def settingsupdateEx(self, eft, efs, efg, bg, elh):
        self.eft = eft
        self.efs = efs
        self.efg = efg
        self.bg = bg
        self.elh = elh
        self.lookup(subsList.currentRow)

    def settingsupdateRe(self, rft, rfs, rfg, bg, rlh):
        self.rft = rft
        self.rfs = rfs
        self.rfg = rfg
        self.bg = bg
        self.rlh = rlh
        self.lookup(subsList.currentRow)

    def settingsupdateGl(self, gft, gfs, gfg, bg, glh):
        self.gft = gft
        self.gfs = gfs
        self.gfg = gfg
        self.bg = bg
        self.glh = glh
        self.lookup(subsList.currentRow)

    def onDefsAnchorClicked(self, url):
        #print "here: " + url.toString()
        command, index = unicode(url.toString()).split(':')
        self.executeDefsCommand(command, int(index))

    def executeDefsCommand(self, command, index):
        if command == 'deleteDef':
            #print "removing: <" + str(index) + "> " + str(self.TranscriptLine[index]) + " " + self.Expression[index]
            del self.TranscriptLine[index]
            del self.Expression[index]
            del self.Reading[index]
            del self.Glossary[index]
            self.lookup(subsList.currentRow)

        if command == 'editDef':
            #print "editing: <" + str(index) + "> " + str(self.TranscriptLine[index]) + " " + self.Expression[index]
            editDialog(self.Glossary[index], index).exec_()
            #print text

    def createdefs(self):
        # get new filename from input dialog
        # set as current filename(.tdef), create new empty file
        # add new file to combobox and set it as current
        text, ok = QInputDialog.getText(self, "Create Definitions File", "File name:", QLineEdit.Normal, "")
        if ok and text != '':
            self.filename = self.basedir + "/" + text + ".tdef"
            file = open(self.filename, 'w')
            data = {'TranscriptLine': self.TranscriptLine, 'Expression': self.Expression, 'Reading': self.Reading, 'Glossary': self.Glossary}
            pickle.dump(data, file)
            file.close()

            dockDirSelect.comboDefs.addItem(text + ".tdef") # hacky, avoids re-query of dir
            index = dockDirSelect.comboDefs.findText(text + ".tdef")
            dockDirSelect.comboDefs.setCurrentIndex(index)
            statusbar.showMessage("New Definitions File Created: " + self.filename)

    def loaddefs(self):
        file = open(self.filename, 'r')
        data = pickle.load(file)
        file.close()
        #print "file closed"
        self.TranscriptLine = data['TranscriptLine']
        self.Expression = data['Expression']
        self.Reading = data['Reading']
        self.Glossary = data['Glossary']
        statusbar.showMessage("Definitions File Loaded: " + self.filename)

    def savedefs(self):
        if self.filename != "":
            file = open(self.filename, 'w')
            data = {'TranscriptLine': self.TranscriptLine, 'Expression': self.Expression, 'Reading': self.Reading, 'Glossary': self.Glossary}
            pickle.dump(data, file)
            file.close()
            statusbar.showMessage("Definitions File Saved: " + self.filename)

    def add(self, expression, reading, glossary):
        line = subsList.currentRow
        self.TranscriptLine.append(line)
        self.Expression.append(expression)
        self.Reading.append(reading)
        self.Glossary.append(glossary)

        self.lookup(line)

    def lookup(self, line):
        #self.clear() # clear linedefs and append matching defs for transcript line
        LineDefs.setHtml(u"""<html><head><style>body {{ background-color: {0} }})
                                        </style></head><body></body></html>""".format(self.bg))

        if line in self.TranscriptLine:
            index = list()
            for z in range(len(self.TranscriptLine)):
                if line == self.TranscriptLine[z]:
                    index.append(z)

            html = unicode()
            for z in range(len(index)):
                html += self.buildDef(self.Expression[index[z]], self.Reading[index[z]], self.Glossary[index[z]], index[z])

            LineDefs.setHtml(self.wrapDefs(html))
            #LineDefs.append(self.wrapDefs(html))
            print self.wrapDefs(html)

    def buildDef(self, expression, reading, glossary, index):
        reading = u'<span class = "reading">[{0}]</span>'.format(reading)
        links = '<a href = "deleteDef:{0}"><img src = "img/icon_action_quit.png" align = "right"/></a>'.format(index)
        links += '<a><img src = "img/empty.png" align = "right"/></a>'
        links += '<a href = "editDef:{0}"><img src = "img/icon_action_zoom_reset.png" align = "right"/></a>'.format(index)

        html = u"""
            <span class = "links">{0}</span>
            <span class = "expression">{1}</span>
            {2}
            <span class = "glossary"><br/>{3}</span>
            <br clear = "all"/><br/>""".format(links, expression, reading, glossary)
        return html

    def wrapDefs(self, html):
        # ; color: {0}; font-size: 16pt;
        return u"""
            <html><head><style>
            body {{ background-color: {0} }}
            span.expression {{ font-size: {1}px; font-family: '{2}'; color: {3}; letter-spacing: {10}px }}
            span.reading {{ font-size: {4}px; font-family: '{5}'; color: {6}; letter-spacing: {11}px }}
            span.glossary {{ font-size: {7}px; font-family: '{8}'; color: {9}; letter-spacing: {12}px }}
            </style></head><body>""".format(self.bg, self.efs, self.eft, self.efg, self.rfs, self.rft, self.rfg, self.gfs, self.gft, self.gfg,self.elh,self.rlh,self.glh) + html + "</body></html>"

            #.format('green', 15, 'serif', 'green', 12, 'serif', 'blue', 10, 'serif','gray') + html + "</body></html>"
            #body {{ background-color: {0} }}

class editDialog(QDialog):
    def __init__(self, text, index):
        super(editDialog, self).__init__()
        self.index = index
        self.texteditor = QTextEdit()
        font = QFont()
        font.setPointSize(12)
        self.texteditor.setFont(font)

        self.texteditor.setText(text)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.texteditor)

        btnOK = QPushButton()
        btnCancel = QPushButton()
        btnOK.setText("Save")
        btnCancel.setText("Cancel")
        vlayout.addWidget(btnOK)
        vlayout.addWidget(btnCancel)
        self.setLayout(vlayout)

        btnOK.clicked.connect(self.btnOKclicked)
        btnCancel.clicked.connect(self.btnCancelclicked)
        self.setWindowTitle("Edit Definition")
        self.show()

    def btnOKclicked(self):
        LineDefs.Glossary[self.index] = self.texteditor.toPlainText()
        LineDefs.lookup(subsList.currentRow)
        self.close()

    def btnCancelclicked(self):
        self.close()

class cSession():
    def __init__(self):
        self.TranscrDir = ""
        self.DefsDir = ""
        self.VideoDir = ""
        self.ThemeDir = ""
        self.TranscrFile = ""
        self.DefsFile = ""
        self.VideoFile = ""
        self.ThemeFile = ""

    def save(self):
        file = open((QtCore.QDir.currentPath() + "/session"), 'w')
        data = {'comboTranscrDir': dockDirSelect.comboTranscrDir,
                'comboDefsDir': dockDirSelect.comboDefsDir,
                'comboVideoDir': dockDirSelect.comboVideoDir,
                'ThemeDir': Settings.ThemeDir,
                'defsfile': dockDirSelect.comboDefs.currentText(),    # .currentIndex(),
                'transcrfile': dockDirSelect.comboTranscr.currentText(),
                'videofile': dockDirSelect.comboVideo.currentText(),
                'themefile': Settings.comboTheme.currentText()}

        pickle.dump(data, file)
        file.close()

        # automatic save defs on close. not sure about this ....
        LineDefs.savedefs()

        #statusbar.showMessage("Session File Saved: " + (QtCore.QDir.currentPath() + "/session"), 2000)
        print "Session File Saved: " + (QtCore.QDir.currentPath() + "/session")
        # subsList.currentRow
        # video position

    def load(self):
        try:
            file = open((QtCore.QDir.currentPath() + "/session"), 'r')
            data = pickle.load(file)
            file.close()

            self.TranscrDir = data['comboTranscrDir']
            self.DefsDir = data['comboDefsDir']
            self.VideoDir = data['comboVideoDir']
            self.ThemeDir = data['ThemeDir']
            self.TranscrFile = data['transcrfile']
            self.DefsFile = data['defsfile']
            self.VideoFile = data['videofile']
            self.ThemeFile = data['themefile']

            statusbar.showMessage("Session Restored: " + (QtCore.QDir.currentPath() + "/session"))
            statusbar.showMessage("ThemeFile Restored: " + self.ThemeFile)
        finally: # in case no session file yet
            return None

if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    qapp.setStyle("cleanlooks")
    w = QMainWindow()

    w.setWindowTitle("Trans-Player-Desktop v0.3")
    statusbar = QStatusBar(w)
    w.setStatusBar(statusbar)

# Restore Session
    Session = cSession()
    #session.restore()
    Session.load()
    qapp.aboutToQuit.connect(Session.save)

# Settings
    dockSettings = QDockWidget("Settings")
    Settings =  cSettings(Session)
    dockSettings.setWidget(Settings)
    dockSettings.setVisible(False)
    w.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dockSettings)

# Video Player
    dockVideo = QDockWidget("Video Player")
    qp = QPlayer(Settings) # videodir/videofile
    dockVideo.setWidget(qp)
    dockVideo.setMinimumWidth(500)
    w.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dockVideo)
    ##w.tabifyDockWidget(dockSettings, dockVideo)
    #w.tabifyDockWidget(dockVideo, dockSettings)

# Transcript List
    subsList = cSubsList(Settings) # font, fgcolor, bgcolor
    subsList.itemDoubleClicked.connect(subsList.gotoLine)
    w.setCentralWidget(subsList)

# Vocab and Kanji
    dockVocab = cDockVocab(Settings) # font, fgcolor, bgcolor, maxwinht
    w.addDockWidget(QtCore.Qt.RightDockWidgetArea, dockVocab)
    dockKanji = cDockKanji()
    w.addDockWidget(QtCore.Qt.RightDockWidgetArea, dockKanji)
    dockKanji.hide()

# Line Defs -- add defs load/save
    LineDefs = cLineDefs(Settings) # font, fgcolor, bgcolor, maxwinht
    dockLineDefs = QDockWidget("Definitions")
    dockLineDefs.setWidget(LineDefs)
    LineDefs.setMinimumWidth(250) # sets the whole right side

# Lookup Line (Minireader)
    lookupLine = MiniReader(dockKanji, dockVocab, dockVocab.textVocabDefs, dockKanji.textKanjiDefs, LineDefs, Settings) # font, fgcolor, bgcolor, maxwinht
    dockLookupLine = QDockWidget("Transcript Line Lookup")
    dockLookupLine.setWidget(lookupLine)
    dockLookupLine.setMaximumHeight(90)
    w.addDockWidget(QtCore.Qt.RightDockWidgetArea, dockLookupLine)
    w.addDockWidget(QtCore.Qt.RightDockWidgetArea, dockLineDefs)

# Directory Select
    dockDirSelect = cDockDirSelect(Session)
    dockDirSelect.setMaximumHeight(70)
    #dockDirSelect.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    w.addDockWidget(QtCore.Qt.TopDockWidgetArea, dockDirSelect)

# Settings
    Settings.transcriptlist = subsList
    Settings.lookupline = lookupLine
    Settings.vocab = dockVocab.textVocabDefs
    Settings.linedefs = LineDefs
    Settings.lookuplinedock = dockLookupLine
    Settings.vocabdock = dockVocab
    Settings.linedefsdock = dockLineDefs
    Settings.statusbar = statusbar
    Settings.loadtheme()
    #statusbar.showMessage("Translation Player Started . . .")

    w.showMaximized()
    qapp.exec_()
