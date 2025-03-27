from PyQt6.QtWidgets import QApplication
import sys
from gui import POSApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = POSApp()
    window.show()
    sys.exit(app.exec())
