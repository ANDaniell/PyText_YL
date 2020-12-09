import sys
from search_page import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets


class MySearchWidget(QMainWindow, Ui_Form):
    def __init__(self, text=""):
        super().__init__()

        # self.text = self.get_text()
        self.text = text
        self.setupUi(self)
        self.lineEdit.setText("поиск")
        self.lineEdit.setPlaceholderText("что каво зачем")
        self.lineEdit.setStyleSheet("QLineEdit {color:red}")

        self.setWindowTitle("Поисковая страница")
        # self.textEdit.print()
        self.pushButton.clicked.connect(self.run)
        # Обратите внимание: имя элемента такое же как в QTDesigner

    def get_text(self):
        try:
            from test01 import MainWindow
            text = MainWindow.textEdit.toPlainText()
            return text
        except Exception:
            return ""

    def run(self):
        a = self.text.lower().split("\n")
        b = self.lineEdit.text()
        numbers = []
        for i in range(len(a)):
            if b in a[i]:
                numbers.append(i + 1)
        if numbers:
            self.lineEdit.setText(f"FIND: '{b}' in lines: {numbers}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MySearchWidget()
    ex.show()
    sys.exit(app.exec_())
