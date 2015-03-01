# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore    #PyQt4
#import about
import constants
#import gen.reader_ui
import japanese.util
import os
#import preferences
import reader_util
import tarfile
import update
#import Translation_Player


class MiniReader(QtGui.QPlainTextEdit): # QtGui.QMainWindow, gen.reader_ui.Ui_MainWindowReader
    class State:
        def __init__(self):
            self.filename = unicode()
            self.kanjiDefs = list()
            self.scanPosition = 0
            self.searchPosition = 0
            self.searchText = unicode()
            self.vocabDefs = list()


    def __init__(self, dockKanji, dockVocab, textVocabDefs, textKanjiDefs, LineDefs):
        super(MiniReader, self).__init__()

        self.dockKanji = dockKanji
        self.dockVocab = dockVocab
        self.textVocabDefs = textVocabDefs
        self.textKanjiDefs = textKanjiDefs

        self.LineDefs = LineDefs

        self.setMouseTracking(True)
        self.setReadOnly(True)

        font = QtGui.QFont()
        font.setPointSize(16)
        self.setFont(font)

        #self.textContent.setObjectName(_fromUtf8("textContent"))
        #self.verticalLayout_4.addWidget(self.textContent)

        self.mouseMoveEvent = self.onContentMouseMove
        self.mousePressEvent = self.onContentMousePress

        self.facts = list()
        self.language = japanese.initLanguage()
        #self.preferences = preferences
        self.state = self.State()
        #self.updater = update.UpdateFinder()
        self.zoom = 0

        #self.applyPreferences()
        #self.updateRecentFiles()
        #self.updateVocabDefs()
        #self.updateKanjiDefs()


        #self.dockKanji.visibilityChanged.connect(self.onVisibilityChanged)
        #self.dockVocab.visibilityChanged.connect(self.onVisibilityChanged)
        #self.listDefinitions.itemDoubleClicked.connect(self.onDefinitionDoubleClicked)

        ### self.textKanjiDefs.anchorClicked.connect(self.onKanjiDefsAnchorClicked)

        #self.textKanjiSearch.returnPressed.connect(self.onKanjiDefSearchReturn)
        self.textVocabDefs.anchorClicked.connect(self.onVocabDefsAnchorClicked)
        #self.textVocabSearch.returnPressed.connect(self.onVocabDefSearchReturn)
        #self.updater.updateResult.connect(self.onUpdaterSearchResult)

        #if self.preferences['checkForUpdates']:
        #    self.updater.start()


    # def applyPreferences(self):
    #     if self.preferences['windowState'] is not None:
    #         self.restoreState(QtCore.QByteArray.fromBase64(self.preferences['windowState']))
    #     if self.preferences['windowPosition'] is not None:
    #         self.move(QtCore.QPoint(*self.preferences['windowPosition']))
    #     if self.preferences['windowSize'] is not None:
    #         self.resize(QtCore.QSize(*self.preferences['windowSize']))
    #
    #     self.comboTags.addItems(self.preferences['tags'])
    #     self.applyPreferencesContent()




    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Shift:
            self.updateSampleFromPosition()
        elif ord('0') <= event.key() <= ord('9'):
            index = event.key() - ord('0') - 1
            if index < 0:
                index = 9
            if event.modifiers() & QtCore.Qt.ShiftModifier:
                if event.modifiers() & QtCore.Qt.ControlModifier:
                    self.executeKanjiCommand('addKanji', index)
            else:
                if event.modifiers() & QtCore.Qt.ControlModifier:
                    self.executeVocabCommand('addVocabExp', index)
                if event.modifiers() & QtCore.Qt.AltModifier:
                    self.executeVocabCommand('addVocabReading', index)
        elif event.key() == ord('[') and self.state.scanPosition > 0:
            self.state.scanPosition -= 1
            self.updateSampleFromPosition()
        elif event.key() == ord(']') and self.state.scanPosition < len(self.textContent.toPlainText()) - 1:
            self.state.scanPosition += 1
            self.updateSampleFromPosition()


    #def moveEvent(self, event):
    #    self.preferences['windowPosition'] = event.pos().x(), event.pos().y()


    #def resizeEvent(self, event):
    #    self.preferences['windowSize'] = event.size().width(), event.size().height()


    def onActionZoomIn(self):
        font = self.textContent.font()
        if font.pointSize() < 72:
            font.setPointSize(font.pointSize() + 1)
            self.textContent.setFont(font)
            self.zoom += 1


    def onActionZoomOut(self):
        font = self.font()
        if font.pointSize() > 1:
            font.setPointSize(font.pointSize() - 1)
            self.setFont(font)
            self.zoom -= 1


    def onActionZoomReset(self):
        if self.zoom:
            font = self.font()
            font.setPointSize(font.pointSize() - self.zoom)
            self.setFont(font)
            self.zoom = 0


    def onActionToggleWrap(self, wrap):
        self.preferences['wordWrap'] = wrap
        self.setLineWrapMode(QtGui.QPlainTextEdit.WidgetWidth if self.preferences['wordWrap'] else QtGui.QPlainTextEdit.NoWrap)


    def onVocabDefsAnchorClicked(self, url):
        command, index = unicode(url.toString()).split(':')
        self.executeVocabCommand(command, int(index))


    def onKanjiDefsAnchorClicked(self, url):
        command, index = unicode(url.toString()).split(':')
        self.executeKanjiCommand(command, int(index))


    def onVocabDefSearchReturn(self):
        text = unicode(self.textVocabSearch.text())
        self.state.vocabDefs, length = self.language.findTerm(text, True)
        self.updateVocabDefs()
        if self.dockKanji.isVisible():
            self.state.kanjiDefs = self.language.findCharacters(text)
            self.updateKanjiDefs()


    def onKanjiDefSearchReturn(self):
        text = unicode(self.textKanjiSearch.text())
        self.state.kanjiDefs = self.language.findCharacters(text)
        self.updateKanjiDefs()


    def onDefinitionDoubleClicked(self, item):
        if self.anki is not None:
            row = self.listDefinitions.row(item)
            self.anki.browseNote(self.facts[row])


    def onVisibilityChanged(self, visible):
        #self.actionToggleAnki.setChecked(self.dockAnki.isVisible())
        self.actionToggleVocab.setChecked(self.dockVocab.isVisible())
        self.actionToggleKanji.setChecked(self.dockKanji.isVisible())


    def onContentMouseMove(self, event):
        #QtGui.QPlainTextEdit.mouseMoveEvent(self.textContent, event)
        self.updateSampleMouseEvent(event)


    def onContentMousePress(self, event):
        #QtGui.QPlainTextEdit.mousePressEvent(self.textContent, event)
        self.updateSampleMouseEvent(event)



    def executeVocabCommand(self, command, index):
        if index >= len(self.state.vocabDefs):
            return

        definition = self.state.vocabDefs[index]
        #if command == 'addVocabExp':
        #    markup = reader_util.markupVocabExp(definition)
        #    self.ankiAddFact('vocab', markup)
        #if command == 'addVocabReading':
        #    markup = reader_util.markupVocabReading(definition)
        #    self.ankiAddFact('vocab', markup)
        if command == 'copyVocabDef':
            reader_util.copyVocabDef(definition)

            #if definition['reading']:
            #    result = u'{expression}\t{reading}\t{glossary}\n'.format(**definition)
            #else:
            #    result = u'{expression}\t{glossary}\n'.format(**definition)

            if definition['reading']:
                result = u'{expression} [{reading}] {glossary}\n'.format(**definition)
            else:
                result = u'{expression} {glossary}\n'.format(**definition)


            #self.LineDefs.append(result)  # REMOVE #

            self.LineDefs.Result = result
            expression = u'{expression}'.format(**definition)
            reading =  u'{reading}'.format(**definition)
            glossary =  u'{glossary}'.format(**definition)
            self.LineDefs.add(expression, reading, glossary)


    def executeKanjiCommand(self, command, index):
        if index >= len(self.state.kanjiDefs):
            return

        definition = self.state.kanjiDefs[index]
        if command == 'addKanji':
            markup = reader_util.markupKanji(definition)
            self.ankiAddFact('kanji', markup)
        elif command == 'copyKanjiDef':
            reader_util.copyKanjiDef(definition)

            self.LineDefs.append(u'{character}\t{kunyomi}\t{onyomi}\t{glossary}'.format(**definition))


    def updateSampleMouseEvent(self, event):
        cursor = self.cursorForPosition(event.pos())
        self.state.scanPosition = cursor.position()
        if event.buttons() & QtCore.Qt.MidButton or event.modifiers() & QtCore.Qt.ShiftModifier:
            self.updateSampleFromPosition()


    def updateSampleFromPosition(self):
        samplePosStart = self.state.scanPosition
        samplePosEnd = self.state.scanPosition + 20 #self.preferences['scanLength']

        cursor = self.textCursor()
        content = unicode(self.toPlainText())
        contentSample = content[samplePosStart:samplePosEnd]
        contentSampleFlat = contentSample.replace(u'\n', unicode())

        if len(contentSampleFlat) == 0 or not japanese.util.isJapanese(contentSampleFlat[0]):
            cursor.clearSelection()
            self.setTextCursor(cursor)
            return

        lengthMatched = 0
        if self.dockVocab.isVisible():
            self.state.vocabDefs, lengthMatched = self.language.findTerm(contentSampleFlat)
            sentence = reader_util.findSentence(content, samplePosStart)
            for definition in self.state.vocabDefs:
                definition['sentence'] = sentence
            self.updateVocabDefs()

        if self.dockKanji.isVisible():
            if lengthMatched == 0:
                self.state.kanjiDefs = self.language.findCharacters(contentSampleFlat[0])
                if len(self.state.kanjiDefs) > 0:
                    lengthMatched = 1
            else:
                self.state.kanjiDefs = self.language.findCharacters(contentSampleFlat[:lengthMatched])
            self.updateKanjiDefs()

        lengthSelect = 0
        for c in contentSample:
            if lengthMatched <= 0:
                break
            lengthSelect += 1
            if c != u'\n':
                lengthMatched -= 1

        cursor.setPosition(samplePosStart, QtGui.QTextCursor.MoveAnchor)
        cursor.setPosition(samplePosStart + lengthSelect, QtGui.QTextCursor.KeepAnchor)
        self.setTextCursor(cursor)

    def updateVocabDefs(self):
        html = reader_util.buildVocabDefs(
            self.state.vocabDefs[:20], #:self.preferences['maxResults']
            None #self.ankiIsFactValid
        )
        self.textVocabDefs.setHtml(html)


    def updateKanjiDefs(self):
        html = reader_util.buildKanjiDefs(
            self.state.kanjiDefs[:20], #self.state.kanjiDefs[:self.preferences['maxRsults']],
            None #self.ankiIsFactValid
        )
        self.textKanjiDefs.setHtml(html)
