import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont


def main():
    app = QApplication(sys.argv)
    
    # Windows 11 stil
    app.setStyle("Fusion")
    
    # Postavi font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    from ui.main_window import MainWindow
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()