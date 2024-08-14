import sys, clicker, ctypes, threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

app_id = 'Volcan\'s Autoclicker'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Volcan's Autoclicker")
        self.setGeometry(100, 100, 400, 160)
        self.setFixedSize(self.width(), self.height())
        self.setWindowIcon(QIcon("./assets/icon.png"))
        self.setStyleSheet("background-image: url(./assets/main_bg.jpg);")

        self.initUI()

    def initUI(self):

        # Label for the delay
        delay_label = QLabel("Delay (ms):", self)
        delay_label.setFont(QFont('Arial', 10))
        delay_label.setGeometry(50, 15, 100, 30)
        delay_label.setStyleSheet("color: white;"
                                  "padding: 5px;")
        
        # Input field for the delay
        self.delay_input = QLineEdit(self)
        self.delay_input.setGeometry(150, 15, 100, 30)
        self.delay_input.setStyleSheet("color: white;"
                                       "padding: 5px;"
                                       "border: 1px solid #292929;"
                                       "font-size: 12px;")
        
        # Label for the window select
        instruction_label = QLabel("When the program is running press O to toggle\nor P to stop the autoclicker.", self)
        instruction_label.setFont(QFont('Arial', 10))
        instruction_label.setGeometry(60, 50, 300, 50)
        instruction_label.setStyleSheet("color: white;"
                                        "padding: 0px;")
        instruction_label.setAlignment(Qt.AlignCenter)
        
        # Start buttonq
        start_button = QPushButton("Start", self)
        start_button.setGeometry(150, 110, 100, 30)
        start_button.setStyleSheet("color: white;"
                                   "padding: 5px;")
        start_button.clicked.connect(self.start_on_click)

    # Function to start the autoclicker
    def start_on_click(self):
        ms = int(self.delay_input.text())
        thread = threading.Thread(target=clicker.clicker, args=(ms,))
        thread.start()
        print(ms)

def Main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    Main()