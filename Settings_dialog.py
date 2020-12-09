# окно диалога создания новой сессии
from PyQt5.QtWidgets import QHBoxLayout, QRadioButton, QFormLayout, QPushButton, QLineEdit, QSpinBox, QDialog, \
    QButtonGroup
from SQLite_back import change, get_values, get_setting


class PreDialog(QDialog):
    def __init__(self):  # + parent
        super(PreDialog, self).__init__()  #

        self.setWindowTitle('Settings')
        self.setModal(True)

        hint = get_values()[0]
        opens = get_setting()[0]

        self.ngroup = QButtonGroup()
        self.hints = QHBoxLayout()
        self.disable_hints = QRadioButton("Hints")
        self.disable_hints2 = QRadioButton("Hints_off")
        self.ngroup.addButton(self.disable_hints)
        self.hints.addWidget(self.disable_hints)
        self.ngroup.addButton(self.disable_hints2)
        self.hints.addWidget(self.disable_hints2)

        self.fgroup = QButtonGroup()
        self.last = QHBoxLayout()
        self.last_path_on = QRadioButton("Reopening")
        self.last_path_on2 = QRadioButton("Clear")
        self.last.addWidget(self.last_path_on)
        self.fgroup.addButton(self.last_path_on)
        self.last.addWidget(self.last_path_on2)
        self.fgroup.addButton(self.last_path_on2)

        self.fgroup.buttonClicked.connect(self.send_event)
        self.ngroup.buttonClicked.connect(self.send_event)

        self.form = QFormLayout()
        self.form.setSpacing(20)

        self.form.addRow("&Do you want see:", self.hints)
        self.form.addRow("&Do you want use:", self.last)

        if get_values()[0] == 1 or get_values()[0] == "1":
            self.disable_hints.setChecked(True)
            self.disable_hints2.setChecked(False)
        else:
            self.disable_hints2.setChecked(True)
            self.disable_hints.setChecked(False)

        if get_setting()[0] == 1 or get_setting()[0] == "1":
            self.last_path_on.setChecked(True)
            self.last_path_on2.setChecked(False)

        else:
            self.last_path_on2.setChecked(True)
            self.last_path_on.setChecked(False)
        print(hint, opens)

        self.setLayout(self.form)

    def closeEvent(self, event):  # +++
        pass

    def send_event(self, radioButton):
        if radioButton.text() == "Hints":
            change("hints", 1)
        elif radioButton.text() == "Hints_off":
            change("hints", 0)
        elif radioButton.text() == "Reopening":
            change("opens", 1)
        elif radioButton.text() == "Clear":
            change("opens", 0)
