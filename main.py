#!/home/vitaliy/Programming/Desktop_App/venv/bin/python3

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, \
    QFileDialog, QDesktopWidget, QGridLayout
from PyQt5.QtCore import pyqtSlot
from core import Classified, show_table
import os


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'My App'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 140
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(260, 30)

        self.graph_button = QPushButton('Show graph', self)
        self.graph_button.move(20, 80)

        self.csv_button = QPushButton('Search', self)
        self.csv_button.move(280, 20)

        self.excel_button = QPushButton('Save excel file', self)
        self.excel_button.move(180, 80)

        self.graph_button.clicked.connect(self.graph_button_click)
        self.csv_button.clicked.connect(self.csv_button_click)
        self.excel_button.clicked.connect(self.saveFileDialog)

        self.show()

    @pyqtSlot()
    def graph_button_click(self):
        file_path = os.path.abspath("data/data.csv")
        if not os.path.exists(file_path):
           self.graph_button.setEnabled(True)

        else:
            show_table()

    @pyqtSlot()
    def csv_button_click(self):
        textboxValue = self.textbox.text()
        data = Classified(textboxValue)
        data.get_csv_file()
        QMessageBox.question(self, 'Success', "Storage updated",
                             QMessageBox.Ok,
                             QMessageBox.Ok)
        self.textbox.setText("")
        print("Ok!")

    def saveFileDialog(self):
        file_path = os.path.abspath("data/data.csv")
        if not os.path.exists(file_path):
            self.excel_button.setEnabled(True)

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Save file", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)

        if fileName:
            Classified.get_excel_file(fileName)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
