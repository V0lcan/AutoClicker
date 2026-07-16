import sys, os, ctypes, clicker
from pynput.mouse import Button
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit,
                             QRadioButton, QButtonGroup, QComboBox, QVBoxLayout, QHBoxLayout,
                             QFormLayout, QMessageBox)
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtCore import Qt, pyqtSignal

# App ID for the taskbar icon
app_id = 'Volcan\'s Autoclicker'
if sys.platform == 'win32':
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

STYLESHEET = """
QWidget {
    background-color: #101010;
    color: white;
    font-family: Arial;
    font-size: 12px;
}
QLineEdit, QComboBox {
    border: 1px solid #292929;
    padding: 5px;
}
QPushButton {
    border: 1px solid #292929;
    padding: 6px;
}
QPushButton:hover {
    background-color: #1a1a1a;
}
QLabel#status {
    color: #8a8a8a;
    padding: 4px;
}
"""


# PyInstaller unpacks a --onefile build into a temp dir at runtime, so asset
# paths can't be relative to the current working directory
def resource_path(relative):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)


# Main window class
class MainWindow(QMainWindow):

    # Emitted from the clicker and hotkey threads, which must not touch widgets
    # directly. Qt queues these back onto the UI thread.
    state_changed = pyqtSignal()

    # Constructor
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Volcan's Autoclicker")
        self.setWindowIcon(QIcon(resource_path("assets/icon.png")))
        self.setStyleSheet(STYLESHEET)

        self.clicker = clicker.Clicker(on_stopped=self.state_changed.emit)
        self.clicker.start()
        self.listener = None

        self.initUI()
        self.state_changed.connect(self.refresh_status)
        self.refresh_status()

    # Function to initialize the UI
    def initUI(self):
        central = QWidget(self)
        self.setCentralWidget(central)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)

        # Input field for the delay
        self.delay_input = QLineEdit(self)
        self.delay_input.setValidator(QIntValidator(1, 3600000, self))
        self.delay_input.setText("100")
        form.addRow("Delay (ms):", self.delay_input)

        # Randomises the delay by up to +/- this many milliseconds
        self.jitter_input = QLineEdit(self)
        self.jitter_input.setValidator(QIntValidator(0, 3600000, self))
        self.jitter_input.setText("0")
        form.addRow("Jitter (± ms):", self.jitter_input)

        # 0 clicks means keep going until stopped
        self.limit_input = QLineEdit(self)
        self.limit_input.setValidator(QIntValidator(0, 100000000, self))
        self.limit_input.setText("0")
        form.addRow("Stop after (0 = never):", self.limit_input)

        # M1 and M2 radio buttons
        self.m1_radio = QRadioButton("M1", self)
        self.m1_radio.setChecked(True)
        self.m2_radio = QRadioButton("M2", self)

        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.m1_radio)
        self.button_group.addButton(self.m2_radio)

        button_row = QHBoxLayout()
        button_row.addWidget(self.m1_radio)
        button_row.addWidget(self.m2_radio)
        button_row.addStretch()
        form.addRow("Mouse button:", button_row)

        # Hotkey selection
        self.toggle_key = QComboBox(self)
        self.toggle_key.addItems(clicker.HOTKEYS.keys())
        self.toggle_key.setCurrentText("F6")
        form.addRow("Toggle key:", self.toggle_key)

        self.stop_key = QComboBox(self)
        self.stop_key.addItems(clicker.HOTKEYS.keys())
        self.stop_key.setCurrentText("F7")
        form.addRow("Stop key:", self.stop_key)

        self.status_label = QLabel(self)
        self.status_label.setObjectName("status")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_on_click)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        layout.addLayout(form)
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_button)

    @property
    def armed(self):
        return self.listener is not None

    # Function to start the autoclicker
    def start_on_click(self):
        if self.armed:
            self.stop()
            return

        if not self.delay_input.hasAcceptableInput():
            QMessageBox.warning(self, "Invalid delay", "Enter a delay of at least 1 ms.")
            return

        toggle = self.toggle_key.currentText()
        stop = self.stop_key.currentText()
        if toggle == stop:
            QMessageBox.warning(self, "Invalid hotkeys", "The toggle and stop keys must differ.")
            return

        self.clicker.delay = int(self.delay_input.text()) / 1000
        self.clicker.jitter = int(self.jitter_input.text() or 0) / 1000
        self.clicker.limit = int(self.limit_input.text() or 0)
        self.clicker.button = Button.left if self.m1_radio.isChecked() else Button.right

        self.listener = clicker.HotkeyListener({
            clicker.HOTKEYS[toggle]: self.on_toggle,
            clicker.HOTKEYS[stop]: self.stop,
        })
        self.listener.start()
        self.refresh_status()

    def on_toggle(self):
        self.clicker.toggle()
        self.state_changed.emit()

    # Stops the clicker and releases the hotkeys
    def stop(self):
        self.clicker.stop_clicking()
        if self.listener:
            self.listener.stop()
            self.listener = None
        self.state_changed.emit()

    def refresh_status(self):
        toggle = self.toggle_key.currentText()
        stop = self.stop_key.currentText()

        if not self.armed:
            self.status_label.setText("Idle — press Start to arm the hotkeys.")
        elif self.clicker.running:
            self.status_label.setText(f"Clicking — {toggle} to pause, {stop} to stop.")
        else:
            self.status_label.setText(f"Ready — {toggle} to click, {stop} to stop.")

        self.start_button.setText("Stop" if self.armed else "Start")
        for widget in (self.delay_input, self.jitter_input, self.limit_input, self.m1_radio,
                       self.m2_radio, self.toggle_key, self.stop_key):
            widget.setEnabled(not self.armed)

    # Without this the clicker thread outlives the window and keeps clicking
    def closeEvent(self, event):
        self.stop()
        self.clicker.shutdown()
        super().closeEvent(event)


def Main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    Main()
