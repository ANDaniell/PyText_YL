import sys

from PyQt5.QtWidgets import QApplication

from test01 import MainWindow


def main():
    app = QApplication(sys.argv)
    # QApplication.setStyle(QStyleFactory.create('Fusion'))
    myGUI = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    # time.sleep(10)