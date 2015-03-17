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
#import copy
#import gen.preferences_ui


class DialogPreferences(QtGui.QDialog): # , gen.preferences_ui.Ui_DialogPreferences
    def __init__(self, parent, preferences): # , anki
        QtGui.QDialog.__init__(self, parent)

        self.setupUi(self)
        self.preferences = preferences
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

        vlayout = QtGui.QVBoxLayout()
        hlayout = QtCore.QHBoxLayout()

        # combo set action
        self.comboBoxAction = QtGui.QComboBox()
        self.comboBoxAction.addItems("Transcript List","Transcript Line Lookup",
                                     "Vocabulary:Expression", "Vocabulary:Reading", "Vocabulary:Glossary",
                                     "Definition:Expression", "Definition:Reading", "Definition:Glossary")
        hlayout.addWidget(self.comboBoxAction)

        # combo set font
        self.comboFontFamily = QtGui.QFontComboBox()
        self.comboFontFamily.currentFontChanged.connect(self.onFontFamilyChanged)
        hlayout.addWidget(self.comboFontFamily)

        # spin font-size
        self.spinFontSize = QtGui.QSpinBox()
        self.spinFontSize.valueChanged.connect(self.onFontSizeChanged)
        hlayout.addWidget(self.spinFontSize)

        # button fg bg
        self.buttonColorFg = QtGui.QPushButton()
        self.buttonColorBg = QtGui.QPushButton()
        self.buttonColorBg.clicked.connect(self.onButtonColorBgClicked)
        self.buttonColorFg.clicked.connect(self.onButtonColorFgClicked)
        hlayout.addWidget(self.buttonColorFg)
        hlayout.addWidget(self.buttonColorBg)

        # text area
        self.textSample = QtGui.QTextEdit()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textSample.setFont(font)
        text = "34他リニ遣熱南極えざ真杉を愛輪すぜて叡統づ棋世とえんけ方世ルみずど非実あ旧加ヲチ殖郵ムハミリ騒取エフヤマ治最フせスけ継乏咋ぞ。遺んぞこり対乗アオツタ志案ク欠慮ニ応米ホヌカヤ延必ぽさざッ再数ト転主ワマタツ復錦ヤミエシ事呼レせ気価ケ事出老シ景育沖ちだひゃ。7蓮エメ面村へ童占ナ緒経認断イッさぴ朝学2車付消ス里1差ルで明女こ職子映しな高価ょゆ群準くはふ。\
                間タウ府誕クヒヱソ応避社ムニキ要直克えむ輸続ノ氏行ワ理見ふをゆぶ評始オルキロ応活マス定断キノ応立ど巻3批テ達定の提演ラけばー要疑績べとね域演未誇もじげく。注げ性崎つ稿7小おすフへ吉乱月トじ期7育左スコテエ症高サヲ悪相35詐はべッぽ会続ねょ情梨フ総岡レのるひ速策ヘ制功ノ吉愛ぐ。\
                一ち表分ぼでぜざ社放う社無攻タリロワ治志ミイカ惑請タ秋先治よド正小セ棋員ルかめぐ戦76格ゅに格金ラ周心リ引際録て。専チクヱナ任台キミナ村後2特ぼ尚90検ツヱ表軽ロムタワ津疾校とで生愛山んス術衛メミムナ真物金ゃざよ変申ロモ梅政挑伏涙煮ぎ。米せ受司相後ど万使ほざめ発2都ツ運月スト政技ぱだふ苦重ヌニ央合でまぜル断掲ユ筋勝クづ土替あ間担株伐唄ゆほて。\
                最よとわ階市カテ周那ンゅ第象ヤオ展面とばラせ表抜おレつ廃刊隆キアヌ稿8月なてルト誓悲チネサ権国異びか白言清リ果5傘忌昆め。辺ふをみ断申たゆがょ的博むぱお全超違ツト省点イモ挙朝ッリゅれ木品づよぐ対上朝ヒヘマ望子ルみぶラ回面ツマ午奨貯鏡トレ。9合区べやぎ青変日ヲヘム防3決サウ小田ミ東君れぐ着80一フヌ本権つっ理決そイ技線殺ヤニル払止ぐぶば平何平をそらば。\
                内回ょルを会寄ヤヘ弘化ぱい息載ステヒク青紙ぜぱのど載問ア円問刊エア護条ワテラウ特一へ誇活ぽいも辞生サク使手ッ全横がよ午何9仰巣か。飯ニ乾台神サ道意カスヲワ野今ルあさ敏1報げらゆや第34旅属到準39同ウ属成連う押読マ踊問禁メネミタ効入制ドッむい棋村ナ改薬セヨキソ巡面るこもけ。""
        self.textSample.setText(text)
        vlayout.addWidget(self.textSample)

        # button ok cancel
        hlayout2 = QtGui.QHBoxLayout()

        buttonOK = QtGui.QPushButton()
        buttonCancel = QtGui.QPushButton()
        buttonOK.setText("Save")
        buttonCancel.setText("Cancel")
        hlayout2.addWidget(buttonOK)
        hlayout2.addWidget(buttonCancel)
        self.setLayout(hlayout2)
        buttonOK.clicked.connect(self.onAccept)
        buttonCancel.clicked.connect(self.buttonCancelClicked)

        #self.comboBoxDeck.currentIndexChanged.connect(self.onDeckChanged)

        self.setWindowTitle("Preferences")
        self.show()
