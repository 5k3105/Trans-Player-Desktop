#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore                        #PyQt4
from yomi_base import japanese
from yomi_base.preference_data import Preferences

from yomi_base.reader import MainWindowReader
from yomi_base.minireader import MiniReader
import sys, pysrt, subterms
from PySide.phonon import Phonon

class YomichanStandalone():
    def __init__(self):

        """
        :rtype : object
        """
        self.language = japanese.initLanguage()
        self.preferences = Preferences()
        self.preferences.load()

        self.window = MainWindowReader(
            None,
            self.preferences,
            self.language,
            filename = sys.argv[1] if len(sys.argv) >= 2 else None
        )

        self.window.show()


class cSubsList(QtGui.QListWidget):
    def __init__(self):
        super(cSubsList, self).__init__()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            if qp.player.state() == Phonon.PausedState:
                qp.player.play()
            else:
                qp.player.pause()

    def loadSubs(self):
        #self.qp.fileEdit.setText("G:\Documents and Settings\\5k3105\Desktop\\anime\sidonia\[DeadFish] Sidonia no Kishi - 04 [720p][AAC].mp4")
        #self.qp.fileEdit.setText("G:\Documents and Settings\\5k3105\Desktop\\anime\sidonia\[Underwater] Knights of Sidonia - 04 (720p) [1CBC15DE].mkv")

        self.subs = pysrt.open("G:\Documents and Settings\\5k3105\Desktop\\anime\sidonia\\timed for [Underwater] release Shidonia_No_Kishi_004.srt",
                               encoding='utf-8')

        g = 0
        for i in self.subs:
            self.insertItem(g, i.text)
            g= g + 1

        for i in xrange(self.count()):
            self.item(i).setFont(QtGui.QFont('Meiryo', 16)) #MS Mincho

        #back up 1:33
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

 #   def itemDoubleClicked(self):
 #       #self.gotoLine()


    def gotoLine(self):
        self.item(self.currentRow).setBackground(QtGui.QColor('white'))

        g = self.currentIndex()
        self.currentRow = g.row()
        i = self.subs[g.row()]
        self.currentSubStart = i.start.ordinal
        self.currentSubEnd = i.end.ordinal
        qp.player.seek(self.currentSubStart)
        i = self.subs[g.row()+1]
        self.nextSubStart = i.start.ordinal
        self.nextSubEnd = i.end.ordinal
        #self.lcdTimer.display("11:00")
        lookupLine.setPlainText(self.subs[g.row()].text)
        #lookupLine.appendPlainText(self.subs[g.row()].text)
        #self.textEditor.append(self.subs[g.row()].text)

class QPlayer(QtGui.QWidget):
    def __init__(self):
        #QtGui.QWidget.__init__(self)
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

        self.player.setTickInterval(500) #1000
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

        #self.fileLabel = QtGui.QLabel("File")
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

        self.fullScreenButton = QtGui.QPushButton("Full Screen") ######

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
        lowerLayout.addWidget(self.fullScreenButton) #########
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
        #self.browseButton.clicked.connect(self.browseClicked)
        self.playButton.clicked.connect(self.playClicked)
        self.pauseButton.clicked.connect(self.pauseClicked)
        self.stopButton.clicked.connect(self.stopClicked)
        #self.fileEdit.textChanged.connect(self.checkFileName)
        self.fullScreenButton.clicked.connect(self.fullScreenClicked)
        #self.videoWidget.keyPressed.connect(self.fullScreenButton)
        #self.mController.availableSubtitlesChanged.connect(self.subsChanged)
        #self.videoWidget.stateChanged.connect(self.vidStateChanged)

    def fullScreenClicked(self):
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

    def tick(self, time):
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

        if time > subsList.currentSubEnd :
            subsList.item(subsList.currentRow).setBackground(QtGui.QColor('grey'))

        if time > subsList.nextSubStart :
            subsList.currentRow = subsList.currentRow + 1
            i = subsList.subs[subsList.currentRow]
            subsList.currentSubStart = i.start.ordinal
            subsList.currentSubEnd = i.end.ordinal
            n = subsList.subs[subsList.currentRow + 1]
            subsList.nextSubStart = n.start.ordinal
            subsList.nextSubEnd = n.end.ordinal

            subsList.item(subsList.currentRow-1).setBackground(QtGui.QColor('white'))
            subsList.item(subsList.currentRow).setBackground(QtGui.QColor('red'))

            #browser text
            #w.body.appendInside("<span>" + w.subs[w.currentRow].text + "</span>")
            #w.span.setPlainText( w.subs[w.currentRow].text)

            #scroll to option. should center current item in list though.
            subsList.ScrollHint = QtGui.QAbstractItemView.EnsureVisible
            subsList.scrollToItem(subsList.item(subsList.currentRow), subsList.ScrollHint)



    def playClicked(self):
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

    def mouseDoubleClickEvent(self, event):
        if self.FS == True:
            self.exitFullScreen()
            self.FS = False
        else:
            self.enterFullScreen()
            self.FS = True

    def keyPressEvent(self, event):
         if event.key() == QtCore.Qt.Key_Escape:
             if self.FS == True:
                 self.exitFullScreen()
                 self.FS = False
             else:
                 self.enterFullScreen()
                 self.FS = True
         if event.key() == QtCore.Qt.Key_Space:
             if self.qp.player.state() == Phonon.PausedState:
                self.qp.player.play()
             else:
                self.qp.player.pause()


if __name__ == "__main__":
    qapp = QtGui.QApplication(sys.argv)
    qp = QPlayer()

    subsList = cSubsList()
    subsList.itemDoubleClicked.connect(subsList.gotoLine)

    w = YomichanStandalone()

    dock1 = QtGui.QDockWidget("Translation Player", w.window)

    dock1.setWidget(qp)
    w.window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock1)
    fn = "G:/Documents and Settings/5k3105/Desktop/anime/sidonia/[DeadFish] Sidonia no Kishi - 04 [720p][AAC].mp4"
    qp.fileEdit = fn

    #w.window.verticalLayout_4.removeWidget(w.window.textContent)
    w.window.textContent.hide()
    w.window.verticalLayout_4.addChildWidget(subsList)


    # dock2 = QtGui.QDockWidget("Subs List", w.window)
    # dock2.setWidget(subsList)
    # w.window.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock2)
    subsList.loadSubs()


    LineDefs = QtGui.QTextBrowser()
    dock4 = QtGui.QDockWidget("Line Defs", w.window)
    dock4.setWidget(LineDefs)
    w.window.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock4)
    font = QtGui.QFont()
    font.setPointSize(16)
    LineDefs.setFont(font)

    x, y, z, q = w.window.giveIt()
    lookupLine = MiniReader(x, y, z, q, LineDefs) # dockKanji, dockVocab

    dock3 = QtGui.QDockWidget("Lookup Line", w.window)
    dock3.setWidget(lookupLine)
    w.window.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock3)

    #w.window.verticalLayout_4.removeWidget(w.window.textContent)
    #w.window.removeDockWidget(w.window.verticalLayout_4)
    #w.window.textContent.hide()


    #file1 = "G:\Documents and Settings\\5k3105\Desktop\\anime\sidonia\\timed for [Underwater] release Shidonia_No_Kishi_004.txt"
    #w.window.openFile(file1)
    qapp.exec_()
