#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore  # PyQt4
from yomi_base import japanese
from yomi_base.preference_data import Preferences


from yomi_base.minireader import MiniReader
import sys, pysrt, subterms
from os import listdir
from os.path import isfile, join
from PySide.phonon import Phonon

class cSubsList(QtGui.QListWidget):
    def __init__(self):
        super(cSubsList, self).__init__()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            if qp.player.state() == Phonon.PausedState:
                qp.player.play()
            else:
                qp.player.pause()

    def loadSubs(self, file):
        self.subs = pysrt.open(file, encoding='utf-8')

        self.clear()
        g = 0
        for i in self.subs:
            self.insertItem(g, i.text)
            g = g + 1

        for i in xrange(self.count()):
            self.item(i).setFont(QtGui.QFont('Meiryo', 16))  # MS Mincho

        # back up 1:33
        #self.subs.shift(seconds=-30) # Move all subs 2 seconds earlier
        #self.subs.shift(minutes=-1)  # Move all subs 1 minutes later
        #self.subs.shift(milliseconds=-500 )

        i = self.subs[0]
        self.currentSubStart = i.start.ordinal
        self.currentSubEnd = i.end.ordinal
        self.currentRow = 0
        i = self.subs[1]
        self.nextSubStart = i.start.ordinal
        self.nextSubEnd = i.end.ordinal

    def gotoLine(self):
        self.item(self.currentRow).setBackground(QtGui.QColor('white'))

        g = self.currentIndex()
        self.currentRow = g.row()
        i = self.subs[g.row()]
        self.currentSubStart = i.start.ordinal
        self.currentSubEnd = i.end.ordinal
        qp.player.seek(self.currentSubStart)
        i = self.subs[g.row() + 1]
        self.nextSubStart = i.start.ordinal
        self.nextSubEnd = i.end.ordinal
        # self.lcdTimer.display("11:00")
        lookupLine.setPlainText(self.subs[g.row()].text)
        #lookupLine.appendPlainText(self.subs[g.row()].text)
        #self.textEditor.append(self.subs[g.row()].text)


class QPlayer(QtGui.QWidget):
    def __init__(self):
        # QtGui.QWidget.__init__(self)
        super(QPlayer, self).__init__()
        self.audioOuptut = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.player = Phonon.MediaObject(self)
        Phonon.createPath(self.player, self.audioOuptut)

        #subtitles not working..
        #self.mController = Phonon.MediaController(self.player)
        #self.mController.setAutoplayTitles(True)

        self.videoWidget = cVideoWidget()
        #self.videoWidget = Phonon.VideoWidget(self)
        Phonon.createPath(self.player, self.videoWidget)

        self.player.setTickInterval(500)  #1000
        self.connect(self.player, QtCore.SIGNAL("tick(qint64)"), self.tick)

        self.seekSlider = Phonon.SeekSlider(self.player, self)
        self.volumeSlider = Phonon.VolumeSlider(self.audioOuptut, self)
        #self.volumeSlider.setMaximumVolume(0.35)

        self.buildGUI()
        self.setupConnections()
        self.init = True

        self.stLineNumber = list()
        self.stTermEnd = list()
        self.stTermStart = list()
        self.stTermStart.append(4)


    def buildGUI(self):

        # self.fileLabel = QtGui.QLabel("File")
        #self.fileEdit = QtGui.QLineEdit()
        #self.fileLabel.setBuddy(self.fileEdit)
        self.fileEdit = ""
        self.lcdTimer = QtGui.QLCDNumber()
        self.lcdTimer.display("00:00")

        #self.browseButton = QtGui.QPushButton("Browse")
        #self.browseButton.setIcon(QtGui.QIcon(":/images/folder-music.png"))

        self.playButton = QtGui.QPushButton("Play")
        self.playButton.setIcon(QtGui.QIcon(":/images/play.png"))
        self.playButton.setEnabled(True)

        self.pauseButton = QtGui.QPushButton("Pause")
        self.pauseButton.setIcon(QtGui.QIcon(":/images/pause.png"))

        self.stopButton = QtGui.QPushButton("Stop")
        self.stopButton.setIcon(QtGui.QIcon(":/images/stop.png"))

        #self.fullScreenButton = QtGui.QPushButton("Full Screen")  ######

        #upperLayout = QtGui.QHBoxLayout()
        #upperLayout.addWidget(self.fileLabel)
        #upperLayout.addWidget(self.fileEdit)
        #upperLayout.addWidget(self.browseButton)

        midLayout = QtGui.QHBoxLayout()
        midLayout.addWidget(self.seekSlider)
        midLayout.addWidget(self.lcdTimer)

        lowerLayout = QtGui.QHBoxLayout()
        lowerLayout.addWidget(self.playButton)
        lowerLayout.addWidget(self.pauseButton)
        lowerLayout.addWidget(self.stopButton)
        #lowerLayout.addWidget(self.fullScreenButton)  #########
        lowerLayout.addWidget(self.volumeSlider)

        layout = QtGui.QVBoxLayout()
        #layout.addLayout(upperLayout)
        layout.addWidget(self.videoWidget)
        layout.addLayout(midLayout)
        layout.addLayout(lowerLayout)

        self.setLayout(layout)
        self.lcdTimer.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.seekSlider.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.volumeSlider.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)


    def setupConnections(self):
        # self.browseButton.clicked.connect(self.browseClicked)
        self.playButton.clicked.connect(self.playClicked)
        self.pauseButton.clicked.connect(self.pauseClicked)
        self.stopButton.clicked.connect(self.stopClicked)
        #self.fileEdit.textChanged.connect(self.checkFileName)
        #self.fullScreenButton.clicked.connect(self.fullScreenClicked)
        #self.videoWidget.keyPressed.connect(self.fullScreenButton)
        #self.mController.availableSubtitlesChanged.connect(self.subsChanged)
        #self.videoWidget.stateChanged.connect(self.vidStateChanged)

    def fullScreenClicked(self):  # Testing Subterm Saves
        self.stLineNumber.append(1)
        self.stTermEnd.append(1)
        self.stTermStart.append(2)
        subterms.save_data(self.stLineNumber, self.stTermStart, self.stTermEnd)

        print self.stTermStart
        self.stTermStart.append(5)
        print self.stTermStart
        print "zxc"
        self.stLineNumber, self.stTermStart, self.stTermEnd = subterms.restore_data()
        print self.stTermStart

    def subsChanged(self):
        pass

    def tick(self, time):  # transcript list hilight following
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
            subsList.item(subsList.currentRow).setBackground(QtGui.QColor('grey'))

        if time > subsList.nextSubStart:
            subsList.currentRow = subsList.currentRow + 1
            i = subsList.subs[subsList.currentRow]
            subsList.currentSubStart = i.start.ordinal
            subsList.currentSubEnd = i.end.ordinal
            n = subsList.subs[subsList.currentRow + 1]
            subsList.nextSubStart = n.start.ordinal
            subsList.nextSubEnd = n.end.ordinal

            subsList.item(subsList.currentRow - 1).setBackground(QtGui.QColor('white'))
            subsList.item(subsList.currentRow).setBackground(QtGui.QColor('red'))

            # browser text
            #w.body.appendInside("<span>" + w.subs[w.currentRow].text + "</span>")
            #w.span.setPlainText( w.subs[w.currentRow].text)

            #scroll to option. should center current item in list though.
            subsList.ScrollHint = QtGui.QAbstractItemView.EnsureVisible
            subsList.scrollToItem(subsList.item(subsList.currentRow), subsList.ScrollHint)


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

    def browseClicked(self):
        f, _ = QtGui.QFileDialog.getOpenFileName(self)
        if f != "":
            self.fileEdit.setText(f)

    def checkFileName(self, s):
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
            if self.qp.player.state() == Phonon.PausedState:
                self.qp.player.play()
            else:
                self.qp.player.pause()

class cDockKanji(QtGui.QDockWidget):
    def __init__(self):
        super(cDockKanji, self).__init__()
        #self.dockKanji = QtGui.QDockWidget(MainWindowReader)
        #self.dockKanji.setObjectName(_fromUtf8("dockKanji"))
        self.dockWidgetContents = QtGui.QWidget()
        #self.dockWidgetContents_3.setObjectName(_fromUtf8("dockWidgetContents_3"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        #self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.textKanjiDefs = QtGui.QTextBrowser(self.dockWidgetContents)
        self.textKanjiDefs.setAcceptDrops(False)
        self.textKanjiDefs.setOpenLinks(False)
        #self.textKanjiDefs.setObjectName(_fromUtf8("textKanjiDefs"))
        self.verticalLayout.addWidget(self.textKanjiDefs)
        self.horizontalLayout = QtGui.QHBoxLayout()
        #self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label = QtGui.QLabel(self.dockWidgetContents)
        #self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label)
        self.textKanjiSearch = QtGui.QLineEdit(self.dockWidgetContents)
        #self.textKanjiSearch.setObjectName(_fromUtf8("textKanjiSearch"))
        self.horizontalLayout.addWidget(self.textKanjiSearch)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.setWidget(self.dockWidgetContents)
        self.setWindowTitle("Kanji")

class cDockVocab(QtGui.QDockWidget):
    def __init__(self):
        super(cDockVocab, self).__init__()
        #self.dockVocab = QtGui.QDockWidget("dockVocab")
        #self.setObjectName(_fromUtf8("dockVocab"))
        self.dockWidgetContents = QtGui.QWidget()
        #self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        #self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.textVocabDefs = QtGui.QTextBrowser(self.dockWidgetContents)
        self.textVocabDefs.setAcceptDrops(False)
        self.textVocabDefs.setOpenLinks(False)
        #self.textVocabDefs.setObjectName("textVocabDefs") #_fromUtf8("textVocabDefs")
        self.verticalLayout.addWidget(self.textVocabDefs)
        self.horizontalLayout = QtGui.QHBoxLayout()
        #self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(self.dockWidgetContents)
        #self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.textVocabSearch = QtGui.QLineEdit(self.dockWidgetContents)
        #self.textVocabSearch.setObjectName(_fromUtf8("textVocabSearch"))
        self.horizontalLayout.addWidget(self.textVocabSearch)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.setWidget(self.dockWidgetContents)
        self.setWindowTitle("Vocabulary")

class cDockDirSelect(QtGui.QDockWidget):
    def __init__(self):
        super(cDockDirSelect, self).__init__()
        self.dockWidgetContents = QtGui.QWidget()
        self.horizontalLayout = QtGui.QHBoxLayout(self.dockWidgetContents)
        self.dockWidgetContents.setLayout(self.horizontalLayout)

        self.comboVideo = QtGui.QComboBox(self.dockWidgetContents)
        self.horizontalLayout.addWidget(self.comboVideo)
        self.btnVideo = QtGui.QPushButton(self.dockWidgetContents)
        self.btnVideo.setText("+")
        self.horizontalLayout.addWidget(self.btnVideo)
        self.btnVideo.clicked.connect(self.showDialogV)

        self.comboTranscr = QtGui.QComboBox(self.dockWidgetContents)
        self.horizontalLayout.addWidget(self.comboTranscr)
        self.btnTranscr = QtGui.QPushButton(self.dockWidgetContents)
        self.btnTranscr.setText("+")
        self.horizontalLayout.addWidget(self.btnTranscr)
        self.btnTranscr.clicked.connect(self.showDialogT)

        self.comboDefs = QtGui.QComboBox(self.dockWidgetContents)
        self.horizontalLayout.addWidget(self.comboDefs)
        self.btnDefs = QtGui.QPushButton(self.dockWidgetContents)
        self.btnDefs.setText("+")
        self.horizontalLayout.addWidget(self.btnDefs)
        self.btnDefs.clicked.connect(self.showDialogD)

        self.btnVideo.setMaximumWidth(20)
        self.btnTranscr.setMaximumWidth(20)
        self.btnDefs.setMaximumWidth(20)

        self.setWidget(self.dockWidgetContents)
        self.setWindowTitle("Directory Select")
        self.setMinimumHeight(50)

        self.comboVideoDir = ""
        self.comboVideo.currentIndexChanged.connect(self.setvideofile)

        self.comboTranscrDir = ""
        self.comboTranscr.currentIndexChanged.connect(self.settranscrfile)


    def setvideofile(self):
        qp.init = True  # reset video source
        fn = self.comboVideoDir
        qp.fileEdit = fn+"\\"+self.comboVideo.currentText()

    def settranscrfile(self):
        fn = self.comboTranscrDir
        subsList.loadSubs(fn+"\\"+self.comboTranscr.currentText())

    def showDialogV(self):
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        dirNames = QtGui.QFileDialog.getOpenFileName
        if dialog.exec_():
            dirNames = dialog.selectedFiles()
        onlyfiles = [ f for f in listdir(dirNames[0]) if isfile(join(dirNames[0],f)) ]
        self.comboVideo.addItems(onlyfiles)
        self.comboVideoDir = dirNames[0]

    def showDialogT(self):
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        dirNames = QtGui.QFileDialog.getOpenFileName
        if dialog.exec_():
            dirNames = dialog.selectedFiles()
        onlyfiles = [ f for f in listdir(dirNames[0]) if isfile(join(dirNames[0],f)) ]
        self.comboTranscr.addItems(onlyfiles)
        self.comboTranscrDir = dirNames[0]

    def showDialogD(self):
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        dirNames = QtGui.QFileDialog.getOpenFileName
        if dialog.exec_():
            dirNames = dialog.selectedFiles()
        onlyfiles = [ f for f in listdir(dirNames[0]) if isfile(join(dirNames[0],f)) ]
        self.comboDefs.addItems(onlyfiles)

if __name__ == "__main__":
    qapp = QtGui.QApplication(sys.argv)
    w = QtGui.QMainWindow()
    w.setWindowTitle("Trans-Player-Desktop v0.1")

    # Video Player
    dockVideo = QtGui.QDockWidget("Translation Player")
    qp = QPlayer()
    dockVideo.setWidget(qp)
    w.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dockVideo)
    #fn = "G:/Documents and Settings/5k3105/Desktop/anime/sidonia/[DeadFish] Sidonia no Kishi - 04 [720p][AAC].mp4"
    #qp.fileEdit = fn
    dockVideo.setMinimumWidth(500)

    # Transcript List
    subsList = cSubsList()
    subsList.itemDoubleClicked.connect(subsList.gotoLine)
    #fn = "G:/Documents and Settings/5k3105/Desktop/anime/sidonia/timed for [Underwater] release Shidonia_No_Kishi_004.srt"
    #subsList.loadSubs(fn)
    w.setCentralWidget(subsList)

    dockVocab = cDockVocab()
    w.addDockWidget(QtCore.Qt.RightDockWidgetArea, dockVocab)
    dockKanji = cDockKanji()
    w.addDockWidget(QtCore.Qt.RightDockWidgetArea, dockKanji)
    dockKanji.hide()

    # Line Defs -- add defs load/save
    LineDefs = QtGui.QTextBrowser()
    dockLineDefs = QtGui.QDockWidget("Line Defs")
    dockLineDefs.setWidget(LineDefs)
    font = QtGui.QFont()
    font.setPointSize(16)
    LineDefs.setFont(font)
    LineDefs.setMinimumWidth(250)

    # Minireader / Lookup Line
    lookupLine = MiniReader(dockKanji, dockVocab, dockVocab.textVocabDefs, dockKanji.textKanjiDefs, LineDefs)
    dockLookupLine = QtGui.QDockWidget("Lookup Line")
    dockLookupLine.setWidget(lookupLine)
    dockLookupLine.setMaximumHeight(90)

    w.addDockWidget(QtCore.Qt.RightDockWidgetArea, dockLookupLine)
    w.addDockWidget(QtCore.Qt.RightDockWidgetArea, dockLineDefs)

    dockDirSelect = cDockDirSelect()
    w.addDockWidget(QtCore.Qt.TopDockWidgetArea, dockDirSelect)


    w.showMaximized()
    qapp.exec_()
