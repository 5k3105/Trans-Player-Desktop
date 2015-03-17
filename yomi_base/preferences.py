# -*- coding: utf-8 -*-

# Copyright (C) 2013  Alex Yatskov
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
import copy
#import gen.preferences_ui


class DialogPreferences(QtGui.QDialog, gen.preferences_ui.Ui_DialogPreferences):
    def __init__(self, parent, preferences, anki):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)



        self.preferences = preferences
        #self.anki = anki

        self.dataToDialog()


    def dataToDialog(self):
#        self.checkCheckForUpdates.setChecked(self.preferences['checkForUpdates'])
#        self.checkLoadRecentFile.setChecked(self.preferences['loadRecentFile'])
#        self.checkStripReadings.setChecked(self.preferences['stripReadings'])
#        self.spinMaxResults.setValue(self.preferences['maxResults'])
#        self.spinScanLength.setValue(self.preferences['scanLength'])

        self.updateSampleText()
        font = self.textSample.font()
        self.comboFontFamily.setCurrentFont(font)
        self.spinFontSize.setValue(font.pointSize())

#        if self.anki is not None:
#            self.tabAnki.setEnabled(True)
#            self.profiles = copy.deepcopy(self.preferences['profiles'])
#            self.profileToDialog()


#    def dialogToData(self):
#        self.preferences['checkForUpdates'] = self.checkCheckForUpdates.isChecked()
#        self.preferences['loadRecentFile'] = self.checkLoadRecentFile.isChecked()
#        self.preferences['maxResults'] = self.spinMaxResults.value()
#        self.preferences['scanLength'] = self.spinScanLength.value()
#        self.preferences['stripReadings'] = self.checkStripReadings.isChecked()

#        if self.anki is not None:
#            self.dialogToProfile()
#            self.preferences['profiles'] = self.profiles


#    def dialogToProfile(self):
#        self.setActiveProfile({
#            'deck': unicode(self.comboBoxDeck.currentText()),
#            'model': unicode(self.comboBoxModel.currentText()),
#            'fields': self.ankiFields()
#        })


#    def profileToDialog(self):
#        profile, name = self.activeProfile()

#        deck = str() if profile is None else profile['deck']
#        model = str() if profile is None else profile['model']

#        self.comboBoxDeck.blockSignals(True)
#        self.comboBoxDeck.clear()
#        self.comboBoxDeck.addItems(self.anki.deckNames())
#        self.comboBoxDeck.setCurrentIndex(self.comboBoxDeck.findText(deck))
#        self.comboBoxDeck.blockSignals(False)

#        self.comboBoxModel.blockSignals(True)
#        self.comboBoxModel.clear()
#        self.comboBoxModel.addItems(self.anki.modelNames())
#        self.comboBoxModel.setCurrentIndex(self.comboBoxModel.findText(model))
#        self.comboBoxModel.blockSignals(False)

#        allowedTags = {
#            'vocab': ['expression', 'reading', 'glossary', 'sentence'],
#            'kanji': ['character', 'onyomi', 'kunyomi', 'glossary'],
#        }[name]

#        allowedTags = map(lambda t: '<strong>{' + t + '}<strong>', allowedTags)
#        self.labelTags.setText('Allowed tags are {0}'.format(', '.join(allowedTags)))

#        self.updateAnkiFields()


    def updateSampleText(self):
        palette = self.textSample.palette()
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(self.preferences['bgColor']))
        palette.setColor(QtGui.QPalette.Text, QtGui.QColor(self.preferences['fgColor']))
        self.textSample.setPalette(palette)

        font = self.textSample.font()
        font.setFamily(self.preferences['fontFamily'])
        font.setPointSize(self.preferences['fontSize'])
        self.textSample.setFont(font)


#    def setAnkiFields(self, fields, fieldsPrefs):
#        if fields is None:
#            fields = list()

#        self.tableFields.blockSignals(True)
#        self.tableFields.setRowCount(len(fields))

#        for i, name in enumerate(fields):
#            columns = list()

#            itemName = QtGui.QTableWidgetItem(name)
#            itemName.setFlags(QtCore.Qt.ItemIsSelectable)
#            columns.append(itemName)

#            itemValue = QtGui.QTableWidgetItem(fieldsPrefs.get(name, unicode()))
#            columns.append(itemValue)

#            for j, column in enumerate(columns):
#                self.tableFields.setItem(i, j, column)

#        self.tableFields.blockSignals(False)


#    def ankiFields(self):
#        result = dict()

#        for i in range(0, self.tableFields.rowCount()):
#            itemName = unicode(self.tableFields.item(i, 0).text())
#            itemValue = unicode(self.tableFields.item(i, 1).text())
#            result[itemName] = itemValue

#        return result


    def onAccept(self):
        self.dialogToData()


    def onButtonColorFgClicked(self):
        color, ok = QtGui.QColorDialog.getRgba(self.preferences['fgColor'], self)
        if ok:
            self.preferences['fgColor'] = color
            self.updateSampleText()


    def onButtonColorBgClicked(self):
        color, ok = QtGui.QColorDialog.getRgba(self.preferences['bgColor'], self)
        if ok:
            self.preferences['bgColor'] = color
            self.updateSampleText()


    def onFontFamilyChanged(self, font):
        self.preferences['fontFamily'] = str(font.family())
        self.updateSampleText()


    def onFontSizeChanged(self, size):
        self.preferences['fontSize'] = size
        self.updateSampleText()


#    def onModelChanged(self, index):
#        self.updateAnkiFields()
#        self.dialogToProfile()


#    def onDeckChanged(self, index):
#        self.dialogToProfile()


#    def onFieldsChanged(self, item):
#        self.dialogToProfile()


#    def onProfileChanged(self, data):
#        self.profileToDialog()


#    def updateAnkiFields(self):
#        modelName = self.comboBoxModel.currentText()
#        fieldNames = self.anki.modelFieldNames(modelName) or list()

#        profile, name = self.activeProfile()
#        fields = dict() if profile is None else profile['fields']

#        self.setAnkiFields(fieldNames, fields)


#    def activeProfile(self):
#        name = 'vocab' if self.radioButtonVocab.isChecked() else 'kanji'
#        return self.profiles.get(name), name


#    def setActiveProfile(self, profile):
#        name = 'vocab' if self.radioButtonVocab.isChecked() else 'kanji'
#        self.profiles[name] = profile


#class editDialog(QDialog):
#    def __init__(self, text, index):

    def setupUI(self):

        # combo set action
        self.comboBoxAction = QtGui.QComboBox()

        # combo set font
        self.comboFontFamily = QtGui.QFontComboBox()
        self.comboFontFamily.currentFontChanged.connect(self.onFontFamilyChanged)


        # font font-size
        self.spinFontSize = QtGui.QSpinBox()
        self.spinFontSize.valueChanged.connect(self.onFontSizeChanged)

        # button fg bg
        self.buttonColorFg = QtGui.QPushButton()
        self.buttonColorBg = QtGui.QPushButton()
        self.buttonColorBg.clicked.connect(self.onButtonColorBgClicked)
        self.buttonColorFg.clicked.connect(self.onButtonColorFgClicked)

        # text area

        # button ok cancel
        buttonOK = QtGui.QPushButton()
        buttonCancel = QtGui.QPushButton()
        buttonOK.setText("Save")
        buttonCancel.setText("Cancel")
        vlayout.addWidget(buttonOK)
        vlayout.addWidget(buttonCancel)
        self.setLayout(vlayout)
        buttonOK.clicked.connect(self.onAccept)
        #self.accepted.connect(self.onAccept)
        buttonCancel.clicked.connect(self.buttonCancelClicked)



        #self.comboBoxDeck.currentIndexChanged.connect(self.onDeckChanged)




        self.texteditor = QtGui.QTextEdit()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.texteditor.setFont(font)
        self.texteditor.setText(text)
        vlayout = QtGui.QVBoxLayout()
        vlayout.addWidget(self.texteditor)



        self.setWindowTitle("Preferences")
        self.show()

#    def btnOKclicked(self):
#        LineDefs.Glossary[self.index] = self.texteditor.toPlainText()
#        LineDefs.lookup(subsList.currentRow)
#        self.close()

#    def btnCancelclicked(self):
#        self.close()



