import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import pathlib
import calc

class MaiApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('resources/main-win.ui', self)
        self.init_window()
        self.show()

    def init_window(self):
        self.img_placeholder_path = 'resources/img_holder.jpg'
        self.image_paths = {}
        self.clean_images()
        self.before_btn.clicked.connect(self.load_before_img)
        self.after_btn.clicked.connect(self.load_after_img)
        self.calculate_btn.clicked.connect(self.calculate)
        self.action_about.triggered.connect(self.show_about_win)

    def load_before_img(self):
        pixmap = self.load_image_to_pixmap('before')
        self.before_img.setPixmap(pixmap)

    def load_after_img(self):
        pixmap = self.load_image_to_pixmap('after')
        self.after_img.setPixmap(pixmap)

    def load_image_to_pixmap(self, key):
        path = str(pathlib.Path(__file__).parent.absolute()).replace("\\", "\\\\")
        fname = QFileDialog.getOpenFileName(self, 'Open file', path, "Image files (*.jpg *.gif)")
        imagePath = fname[0]
        if (imagePath == ''):
            return QPixmap(self.img_placeholder_path)
        self.image_paths[key] = imagePath
        return QPixmap(imagePath)

    def clean_images(self):
        self.before_img.setPixmap(QPixmap(self.img_placeholder_path))
        self.after_img.setPixmap(QPixmap(self.img_placeholder_path))

    def calculate(self):
        if ('before' in self.image_paths and 'after' in self.image_paths):
            current_method = str(self.choose_method.currentText())
            calc.calculate(self.image_paths['before'], self.image_paths['after'], current_method)
        else:
            error_dialog = self.create_error_dialog('Необходимо добавить оба изображения!')
            error_dialog.exec_()

    def create_error_dialog(self, error_msg):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error_msg)
        msg.setWindowTitle("Error")
        return msg

    def show_about_win(self):
        self.about_app = AboutApp()
        self.about_app.setFixedSize(self.about_app.size())
        self.about_app.show()

class AboutApp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('resources/about-win.ui', self)

#-------------------------------------------
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MaiApp()
    window.show()
    window.setFixedSize(window.size())
    app.exec_()

if __name__ == '__main__':
    main()
