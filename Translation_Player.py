#!/usr/bin/python
# --coding: utf-8 --

import sys, pysrt, yomichan, subterms

from PySide import QtCore, QtGui, QtWebKit

try:
    from PySide.phonon import Phonon
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "Music Player",
                               "Your Qt installation does not have Phonon support.",
                               QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                               QtGui.QMessageBox.NoButton)
    sys.exit(1)


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
        self.volumeSlider.setMaximumVolume(0.35)

        self.buildGUI()
        self.setupConnections()
        self.init = True

        self.stLineNumber = list()
        self.stTermEnd = list()
        self.stTermStart = list()
        self.stTermStart.append(4)


    def buildGUI(self):

        self.fileLabel = QtGui.QLabel("File")
        self.fileEdit = QtGui.QLineEdit()
        self.fileLabel.setBuddy(self.fileEdit)

        self.lcdTimer = QtGui.QLCDNumber()
        self.lcdTimer.display("00:00")

        self.browseButton = QtGui.QPushButton("Browse")
        self.browseButton.setIcon(QtGui.QIcon(":/images/folder-music.png"))

        self.playButton = QtGui.QPushButton("Play")
        self.playButton.setIcon(QtGui.QIcon(":/images/play.png"))
        self.playButton.setEnabled(False)

        self.pauseButton = QtGui.QPushButton("Pause")
        self.pauseButton.setIcon(QtGui.QIcon(":/images/pause.png"))

        self.stopButton = QtGui.QPushButton("Stop")
        self.stopButton.setIcon(QtGui.QIcon(":/images/stop.png"))

        self.fullScreenButton = QtGui.QPushButton("Full Screen") ######

        upperLayout = QtGui.QHBoxLayout()
        upperLayout.addWidget(self.fileLabel)
        upperLayout.addWidget(self.fileEdit)
        upperLayout.addWidget(self.browseButton)

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
        layout.addLayout(upperLayout)
        layout.addWidget(self.videoWidget)
        layout.addLayout(midLayout)
        layout.addLayout(lowerLayout)

        self.setLayout(layout)
        self.lcdTimer.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.seekSlider.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.volumeSlider.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)


    def setupConnections(self):
        self.browseButton.clicked.connect(self.browseClicked)
        self.playButton.clicked.connect(self.playClicked)
        self.pauseButton.clicked.connect(self.pauseClicked)
        self.stopButton.clicked.connect(self.stopClicked)
        self.fileEdit.textChanged.connect(self.checkFileName)
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

        if time > w.currentSubEnd :
            w.subsList.item(w.currentRow).setBackground(QtGui.QColor('grey'))

        if time > w.nextSubStart :
            w.currentRow = w.currentRow + 1
            i = w.subs[w.currentRow]
            w.currentSubStart = i.start.ordinal
            w.currentSubEnd = i.end.ordinal
            n = w.subs[w.currentRow + 1]
            w.nextSubStart = n.start.ordinal
            w.nextSubEnd = n.end.ordinal

            w.subsList.item(w.currentRow-1).setBackground(QtGui.QColor('white'))
            w.subsList.item(w.currentRow).setBackground(QtGui.QColor('red'))

            #browser text
            #w.body.appendInside("<span>" + w.subs[w.currentRow].text + "</span>")
            w.span.setPlainText( w.subs[w.currentRow].text)

            #scroll to option. should center current item in list though.
            w.subsList.ScrollHint = QtGui.QAbstractItemView.EnsureVisible
            w.subsList.scrollToItem(w.subsList.item(w.currentRow), w.subsList.ScrollHint)



    def playClicked(self):
        if self.init:
            self.player.setCurrentSource(Phonon.MediaSource(self.fileEdit.text()))
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
             if w.qp.player.state() == Phonon.PausedState:
                w.qp.player.play()
             else:
                w.qp.player.pause()

class cSubsList(QtGui.QListWidget):
    def __init__(self):
        super(cSubsList, self).__init__()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            if w.qp.player.state() == Phonon.PausedState:
                w.qp.player.play()
            else:
                w.qp.player.pause()

                #QtGui.QMdiSubWindow

class TranslationPlayer(QtGui.QMainWindow):
    def __init__(self):
        super(TranslationPlayer, self).__init__()

        self.qp = QPlayer()
        self.setCentralWidget(self.qp)
        self.setWindowTitle("Translation Player")

        self.addDock()
        self.loadSubs()
        self.subsList.itemDoubleClicked.connect(self.gotoLine)

        self.clipboard = QtGui.QClipboard()

        self.qp.volumeSlider.setMaximumVolume(0.35)
        #self.qp.audioOuptut.setVolumeDecibel(0.25)
        #QtGui.QWindowsStyle(QtGui.QPlastiqueStyle)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Space:
            if self.qp.player.state() == Phonon.PausedState:
                self.qp.player.play()
            else:
                self.qp.player.pause()

        if e.key() == QtCore.Qt.Key_Left:
            self.qp.player.seek(self.qp.player.currentTime() - 10000)
        elif e.key() == QtCore.Qt.Key_Right:
            self.qp.player.seek(self.qp.player.currentTime() + 10000)
        elif e.key() == QtCore.Qt.Key_Down:
            self.qp.player.seek(self.qp.player.currentTime() - 60000)
        elif e.key() == QtCore.Qt.Key_Up:
            self.qp.player.seek(self.qp.player.currentTime() + 60000)
        # elif e.key() == QtCore.Qt.Key_F:
        #     self.toggle_fullscreen()
        # elif e.key() == QtCore.Qt.Key_Space:
        #     self.toggle_play()


    def gotoLine(self):
        self.subsList.item(self.currentRow).setBackground(QtGui.QColor('white'))

        g = self.subsList.currentIndex()
        self.currentRow = g.row()
        i = self.subs[g.row()]
        self.currentSubStart = i.start.ordinal
        self.currentSubEnd = i.end.ordinal
        self.qp.player.seek(self.currentSubStart)
        i = self.subs[g.row()+1]
        self.nextSubStart = i.start.ordinal
        self.nextSubEnd = i.end.ordinal
        #self.lcdTimer.display("11:00")

        self.textEditor.append(self.subs[g.row()].text)


        #copy to clipboard
        #self.clipboard.clear()
        #self.clipboard.setMimeData(self.subs[g.row()].text, QClipboard)
        #self.clipboard.setTextFormat(Qt.RichText)
        #print self.subs[g.row()].text

        #replace space character for correct paste.
        # content = self.subs[g.row()].text
        # content = unicode(content.toPlainText())
        #txtUni = self.subs[g.row()].text.decode('utf-8')
        #unicode(txtUni,"utf-8")
        #txtUni = self.subs[g.row()].text.replace(' ','\u200b' )
        # self.clipboard.setText(content)
        #self.clipboard.setText(self.subs[g.row()].text)

    def addDock(self):
        dock = QtGui.QDockWidget("Subtitles", self)
        dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.subsList = cSubsList() #(dock)
        dock.setWidget(self.subsList)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)

        dock = QtGui.QDockWidget("Text Editor", self)
        dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.textEditor = QtGui.QTextEdit(dock)
        dock.setWidget(self.textEditor)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.textEditor.setFont(font)


        dock = QtGui.QDockWidget("Browser", self)
        dock.setAllowedAreas(QtCore.Qt.TopDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)

        self.browser = QtWebKit.QWebView(dock)
        dock.setWidget(self.browser)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock)

        self.browserSettings = self.browser.settings()
        #self.browserSettings.setAttribute(QtWebKit.QWebSettings.PluginsEnabled,True)
        self.browserSettings.setAttribute(QtWebKit.QWebSettings.JavascriptEnabled,True)
        self.browserSettings.setFontSize(QtWebKit.QWebSettings.MinimumFontSize,30)
        #self.browserSettings.setFontFamily(QtWebKit.QWebSettings.FontFamily,"MS Mincho")

        self.browser.load("G:\Documents and Settings\\5k3105\Desktop\\anime\sidonia\\timed for [Underwater] release Shidonia_No_Kishi_004.txt")
        self.browser.show()

        wp = "G:\Documents and Settings\5k3105\Local Settings\Application Data\Google\Chrome\User Data\Default\Extensions\jipdnfibhldikgcjhfnomkfpcebammhp\0.8.9_0\background2.html"
        self.browser.load(wp)

        page = self.browser.page()
        frame = page.mainFrame()
        html = frame.documentElement()
        head = html.firstChild()

        self.body = head.nextSibling()
        self.body.appendInside(u"<span> </span>")
        self.span = self.body.firstChild()

        """
        print html.tagName()
        print head.tagName()
        print self.body.tagName()
        print self.span.tagName()


        elem.appendInside("<span>Intro</span>")
        print elem.toPlainText()
        print elem.tagName()
        elem2 = elem.firstChild()
        print elem2.tagName()
        print elem2.toPlainText()
        """
        #self.browser.setHtml(u"ザシュ！")

    """
    def set_font(self, font):
        family = font.family()
        settings = self.page().settings()
        settings.setFontFamily(settings.StandardFont, family)
        settings.setFontFamily(settings.SerifFont, family)
        settings.setFontFamily(settings.SansSerifFont, family)
        settings.setFontFamily(settings.CursiveFont, family)
        size = font.pointSize()
        settings.setFontSize(settings.DefaultFontSize, size)
        settings.setFontSize(settings.DefaultFixedFontSize, size)
    """

    def loadSubs(self):
        self.qp.fileEdit.setText("G:\Documents and Settings\\5k3105\Desktop\\anime\sidonia\[DeadFish] Sidonia no Kishi - 04 [720p][AAC].mp4")
        #self.qp.fileEdit.setText("G:\Documents and Settings\\5k3105\Desktop\\anime\sidonia\[Underwater] Knights of Sidonia - 04 (720p) [1CBC15DE].mkv")

        self.subs = pysrt.open("G:\Documents and Settings\\5k3105\Desktop\\anime\sidonia\\timed for [Underwater] release Shidonia_No_Kishi_004.srt",
                               encoding='utf-8')

        g = 0
        for i in self.subs:
            self.subsList.insertItem(g, i.text)
            g= g + 1

        for i in xrange(self.subsList.count()):
            self.subsList.item(i).setFont(QtGui.QFont('Meiryo', 16)) #MS Mincho

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


if __name__ == "__main__":
    #qapp = QtGui.QApplication(sys.argv)
    instance = yomichan.YomichanStandalone()
    file1 = "G:\Documents and Settings\\5k3105\Desktop\\anime\sidonia\\timed for [Underwater] release Shidonia_No_Kishi_004.txt"
    instance.window.openFile(file1)
    #instance.window.openFile("G:\Documents and Settings\\5k3105\Desktop\\anime\sidonia\\timed for [Underwater] release Shidonia_No_Kishi_004.txt")
    #instance.window.textContent.frameRect()

    #dock = QtGui.QDockWidget("Translation Player", instance.window)
    #dock.setWidget(QPlayer())
    #instance.window.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)

    #qp = QPlayer()
    #self.setCentralWidget(self.qp)
    #self.setWindowTitle("Translation Player")
    #instance.window.addDockWidget(instance.window.dockWidgetArea., qp)
    #instance.window.verticalLayout.addWidget(QPlayer())
    #instance.window.repaint()

    #qp.show()
    #instance.window.setWindowTitle("Translation Player")
    #w = MainWindow()
    #w.show()

    #print QtGui.QApplication.focusWidget.windowTitle()
    #print QtGui.QApplication.activeWindow.windowTitle()
    #sys.exit(qapp.exec_())
