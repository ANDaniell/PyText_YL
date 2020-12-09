#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
import sys
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, qApp, QTabWidget, QMessageBox,
                             QInputDialog, QLineEdit, QHBoxLayout, QSpinBox, QRadioButton, QPushButton, QDialog,
                             QWidget, QColorDialog)
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5 import QtCore
import logging
from analisation import analis_encoding, analis_morph, new_analis

from Settings_dialog import PreDialog
import time
from searching_page import MySearchWidget
from SQLite_back import change, get_setting, get_values, get_path, set_color


class MemoryWorker():
    def __init__(self):
        pass

    def search_word(self):
        txt = self.textEdit.toPlainText()
        self.search_form = MySearchWidget(txt)
        self.search_form.show()
        if self.search_form.pushButton.isChecked():
            print("Done")
        pass

    def text_render(self, pattern=None, time_s=0):
        time.sleep(time_s)
        data = self.textEdit.toPlainText().split("\n")
        HTML = ""
        for i in data:
            i = i.split(" ")
            for j in i:
                # color = analis_morph(j)
                color = new_analis(j)
                # print(data)
                # print(color, j)
                HTML += f"<font color='{color}' >{j + ' '}</font>"
            HTML += "<br>"
            # print(i)
        self.textEdit.setHtml(HTML)
        # print(HTML)
        if pattern is None:
            pass
        else:
            try:
                cursor = self.textEdit.textCursor()
                # Setup the desired format for matches
                format = QtGui.QTextCharFormat()
                format.setBackground(QtGui.QBrush(QtGui.QColor("red")))
                # Setup the regex engine
                regex = QtCore.QRegExp(pattern)
                # Process the displayed document
                pos = 0
                index = regex.indexIn(self.textEdit.toPlainText(), pos)
                while index != -1:
                    # Select the matched text and apply the desired format
                    cursor.setPosition(index)
                    cursor.movePosition(QtGui.QTextCursor.EndOfWord, 1)
                    cursor.mergeCharFormat(format)
                    # Move to the next match
                    pos = index + regex.matchedLength()
                    index = regex.indexIn(self.textEdit.toPlainText(), pos)
            except Exception:
                pass

    def change_color_settings(self):
        color = QColorDialog.getColor()

        if color.isValid():
            return (color.name())
        pass

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Color dialog',
                                        'Enter the part of speech:')
        if ok:
            color = self.change_color_settings()
            set_color(text, color)

    def txt_treads(self):
        e1 = threading.Event()
        e2 = threading.Event()
        # init threads
        while True:
            t1 = threading.Thread(target=self.text_render, args=(None, 10))
            t1.start()


class Graphic:
    def setup(self):
        ##############################################
        #  Строим меню файла
        ##############################################
        # меню файла - пункт Exit
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        # меню файла - пункт New
        newAction = QAction(QIcon('new.png'), '&New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New file')
        newAction.triggered.connect(self.newFile)

        # меню файла - пункт open anyway
        openAny = QAction(QIcon('open_anyway.png'), '&OpenAnyway', self)
        openAny.setShortcut('Ctrl+J')
        openAny.setStatusTip('Open File in not stated format')
        openAny.triggered.connect(self.openAnyway)

        # меню файла - пункт Open
        openAction = QAction(QIcon('open.png'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open File')
        openAction.triggered.connect(self.openFile)

        # меню файла - пункт Save As
        saveasAction = QAction(QIcon('save_as.png'), '&SaveAs', self)
        saveasAction.setShortcut('Ctrl+S')
        saveasAction.setStatusTip('Save file as...')
        saveasAction.triggered.connect(self.saveAs)

        # анализ
        searchAction = QAction(QIcon('refresh.png'), '&refresh', self)
        searchAction.setShortcut('Ctrl+I')
        searchAction.setStatusTip('Refresh words in text')
        searchAction.triggered.connect(self.text_render)

        # кнопка настроек
        settingsAction = QAction(QIcon('settings.png'), '&Settings', self)
        settingsAction.setShortcut('Ctrl+B')
        settingsAction.setStatusTip('Configure your setup, dude!')
        settingsAction.triggered.connect(self.config_settings)

        # кнопка выбора цвета
        colorAction = QAction(QIcon('colors.png'), '&Colors', self)
        colorAction.setShortcut('Ctrl+L')
        colorAction.setStatusTip('Configure your setup, dude!')
        colorAction.triggered.connect(self.change_color_settings)

        self.statusBar()

        # добавляем элементы в меню
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(openAny)
        fileMenu.addAction(saveasAction)
        fileMenu.addAction(exitAction)

        menu_search = self.menuBar()
        search = menubar.addMenu('Refresh')
        search.addAction(searchAction)

        search = menubar.addMenu('Settings')
        search.addAction(settingsAction)
        search.addAction(colorAction)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Menubar')
        self.show()
        try:
            self.reopenFile(get_path()[0])
        except TypeError as ex:
            print(ex)
            self.newFile()


class MainWindow(QMainWindow, MemoryWorker, Graphic):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.resize(700, 500)

        self.textEdit = QTextEdit()

        self.setCentralWidget(self.textEdit)
        self.setup()

    def config_settings(self):
        #        self.dialog = PreDialog(self)
        self.dialog = PreDialog()
        self.dialog.show()

    def error_name_file(self):
        if get_values()[0] == 1:
            try:
                self.message = QMessageBox()
                self.message.setWindowTitle("Warning")
                self.message.setText("There is incorrect file path")
                self.message.setInformativeText("please retry")
                okButton = self.message.addButton('Ok', QMessageBox.AcceptRole)
                self.message.addButton('Cancel', QMessageBox.RejectRole)
                self.message.show()
                self.message.exec()
                if self.message.clickedButton() == okButton:
                    return True
                else:
                    return False
            except Exception as exc:
                logging.debug(f"{exc}")
                pass
            return False
        else:
            return False

    def open_dialog(self):
        if get_values()[0] == 1:
            try:
                self.message = QMessageBox()
                self.message.setWindowTitle("Warning")
                self.message.setText("Do you want save changes?")
                self.message.setInformativeText("It may destroy your data")
                okButton = self.message.addButton('Ok', QMessageBox.AcceptRole)
                self.message.addButton('Cancel', QMessageBox.RejectRole)
                self.message.show()
                self.message.exec()
                if self.message.clickedButton() == okButton:
                    return True
                else:
                    return False
            except Exception as exc:
                logging.debug(f"{exc}")
                pass
            return False
        else:
            return False

    def newFile(self):
        try:
            if get_values()[0] == 1:
                if self.check_changes():
                    if self.open_dialog():
                        try:
                            fname = get_path()[0]
                            openedFile = open(fname, 'w')
                            txt = self.textEdit.toPlainText()
                            openedFile.write(txt)
                            openedFile.close()
                            pass
                        except Exception as exc:
                            logging.debug(f"{exc}")
                            pass
                self.textEdit.setText("")
                change("last_path", "")
            else:
                if get_setting()[0] == 1:
                    fname = get_path()[0]
                    if fname != "":
                        openedFile = open(fname, 'w')
                        txt = self.textEdit.toPlainText()
                        openedFile.write(txt)
                        openedFile.close()
                else:
                    pass
                self.textEdit.setText("")
        except TypeError:
            self.textEdit.setText("")
            change("last_path", "")

    def check_changes(self):
        try:
            fname = get_path()[0]

            txt = self.textEdit.toPlainText()

            if fname != "":
                orig_txt_file = open(fname, 'rt')
                orig_txt = orig_txt_file.read()
                orig_txt_file.close()
                if txt != orig_txt:
                    return True
                else:
                    return False
            else:
                if txt != "":
                    return True
                else:
                    return False
        except FileNotFoundError:
            return False

    def reopenFile(self, path):
        try:
            openedFile = open(path, 'r')
            txt = openedFile.read()
            openedFile.close()
            self.textEdit.setText(txt)
            self.text_render()
            if get_setting()[0] == 1:
                change("last_paths", str(path))
            self.statusBar().showMessage(f"file path: {path}")
        except FileNotFoundError:
            pass

    def openFile(self):
        if self.check_changes():
            if self.open_dialog():
                try:
                    if get_setting()[0] == 1:
                        if get_path()[0] == "":
                            self.saveAs()
                        else:
                            fname = get_path()[0]
                            openedFile = open(fname, 'w')
                            txt = self.textEdit.toPlainText()
                            openedFile.write(txt)
                            openedFile.close()
                        pass
                except Exception as exc:
                    logging.debug(f"{exc}")
                    pass
        else:
            pass
        # диалог открытия файла
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file')[0]
            openedFile = open(fname, 'r')
            txt = openedFile.read()
            openedFile.close()
            self.textEdit.setText(txt)
            self.text_render()
            if get_setting()[0] == 1:
                change("last_path", str(fname))
            self.statusBar().showMessage(f"file path: {fname}")
        except FileNotFoundError:
            if self.error_name_file():
                self.openFile()
            pass

    def change_encoding_dialog(self):
        text, okPressed = QInputDialog.getText(self, "Get text", "Your name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            return text
        pass

    def error_encoding_dialog(self):
        if get_setting()[0] == 1:
            try:
                self.message = QMessageBox()
                self.message.setWindowTitle("Warning")
                self.message.setText(
                    "Incorrect file code. You may continue with your encoding")
                self.message.setInformativeText(
                    "If you dont change encoding, you will continue utf-8")
                okButton = self.message.addButton('Continue', QMessageBox.AcceptRole)
                changeButton = self.message.addButton('Change encoding', QMessageBox.ApplyRole)
                self.message.addButton("Cancel", QMessageBox.RejectRole)
                self.message.show()
                self.message.exec()
                if self.message.clickedButton() == okButton:
                    return "utf-8"
                elif self.message.clickedButton() == changeButton:
                    return self.change_encoding_dialog()
                else:
                    return None
            except Exception as exc:
                logging.debug(f"{exc}")
                pass
            return None
        else:
            return None

    def openAnyway(self):
        # открываем файл
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file')[0]
            self.statusBar().showMessage(f"file path: {fname}")
            change("last_path", fname)
            if analis_encoding(fname) is None:
                encode = self.error_encoding_dialog()
                if encode is not None:
                    try:
                        f = open(fname, "rb")
                        data = f.read()
                        data = data.decode(encode, errors='ignore')
                        f.close()
                        self.textEdit.setText(data)
                        self.text_render()
                    except Exception as exc:
                        logging.debug(f"{exc}")
                        self.message = QMessageBox()
                        self.message.setWindowTitle("Warning")
                        self.message.setText("Its incorrect encoding")
                        okButton = self.message.addButton('Retry', QMessageBox.AcceptRole)
                        if self.message.clickedButton() == okButton:
                            pass
                        else:
                            pass
            else:
                try:
                    f = open(fname, "rb")
                    data = f.read()
                    encode = analis_encoding(fname)
                    data = data.decode(encode, errors='ignore')
                    f.close()
                    self.textEdit.setText(data)
                    self.text_render()
                except Exception as exc:
                    logging.debug(f"{exc}")
                pass

        except FileNotFoundError:
            pass

    def saveAs(self):
        try:
            # диалог сохранения файла
            fname = QFileDialog.getSaveFileName(self)[0]
            change("last_path", fname)
            openedFile = open(fname, 'w')
            txt = self.textEdit.toPlainText()
            openedFile.write(txt)
            openedFile.close()
        except FileNotFoundError:
            pass
