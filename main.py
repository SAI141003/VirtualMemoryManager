from PyQt6.QtWidgets import QApplication
from gui import VirtualMemoryGUI  # ✅ Changed from ui_design to gui
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VirtualMemoryGUI()
    window.show()
    sys.exit(app.exec())
