#!/bin/sh
pyside-uic ui/about.ui -o yomi_base/gen/about_ui.py
pyside-uic ui/preferences.ui -o yomi_base/gen/preferences_ui.py
pyside-uic ui/reader.ui -o yomi_base/gen/reader_ui.py
pyside-uic ui/resources.qrc -o yomi_base/gen/resources_rc.py
