from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QPushButton, 
                             QHBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QKeyEvent
from widgets.display import Display
from core.engine import CalculatorEngine


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyCalc")
        self.setFixedSize(320, 500)
        
        self.dark_mode = False
        self.engine = CalculatorEngine()
        self.display = Display()

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self.display)

        # Dugme za temu
        theme_layout = QHBoxLayout()
        self.theme_btn = QPushButton("🌙")
        self.theme_btn.setFixedSize(40, 40)
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.clicked.connect(self.toggle_theme)
        theme_layout.addStretch()
        theme_layout.addWidget(self.theme_btn)
        layout.addLayout(theme_layout)

        # Grid dugmadi
        grid = QGridLayout()
        grid.setSpacing(8)

        buttons = [
            ("%", "special"), ("CE", "special"), ("C", "special"), ("⌫", "special"),
            ("¹/ₓ", "special"), ("x²", "special"), ("√x", "special"), ("÷", "operator"),
            ("7", "number"), ("8", "number"), ("9", "number"), ("×", "operator"),
            ("4", "number"), ("5", "number"), ("6", "number"), ("-", "operator"),
            ("1", "number"), ("2", "number"), ("3", "number"), ("+", "operator"),
            ("+/-", "number"), ("0", "number"), (",", "number"), ("=", "equals")
        ]

        positions = [(i, j) for i in range(6) for j in range(4)]

        for position, (text, btn_type) in zip(positions, buttons):
            button = QPushButton(text)
            button.setFixedSize(70, 55)
            button.setFont(QFont("Segoe UI", 12))
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(self.button_clicked)
            button.setProperty("btn_type", btn_type)
            button.setStyleSheet(self.get_button_style(btn_type))
            grid.addWidget(button, *position)

        layout.addLayout(grid)
        self.setLayout(layout)
        
        self.apply_theme()
        
        # Fokus za tastaturu
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()

    def keyPressEvent(self, event: QKeyEvent):
        """TASTATURA - obrada pritisaka"""
        key = event.key()
        text = event.text()
        
        # Brojevi (glavni i numpad preko text())
        if text.isdigit():
            self.process_input(text)
        
        # Operatori iz text()
        elif text in ['+', '-', '*', '/']:
            self.process_input(text)
        
        # Operatori iz key codes (kao backup)
        elif key == Qt.Key.Key_Plus:
            self.process_input('+')
        elif key == Qt.Key.Key_Minus:
            self.process_input('-')
        elif key == Qt.Key.Key_Asterisk:
            self.process_input('*')
        elif key == Qt.Key.Key_Slash:
            self.process_input('/')
        
        # Decimalna tačka (tačka, zarez)
        elif text in ['.', ',']:
            self.process_input('.')
        elif key in [Qt.Key.Key_Period, Qt.Key.Key_Comma]:
            self.process_input('.')
        
        # Enter = izračunaj (više varijanti)
        elif key in [Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Equal]:
            self.calculate()
        
        # Escape = C
        elif key == Qt.Key.Key_Escape:
            self.clear_all()
        
        # Backspace
        elif key == Qt.Key.Key_Backspace:
            self.backspace()
        
        # Delete = CE
        elif key == Qt.Key.Key_Delete:
            self.clear_entry()

    def process_input(self, text):
        value = self.engine.input(text)
        self.display.set_main(value)

    def calculate(self):
        history, value = self.engine.evaluate()
        self.display.set_history(history)
        self.display.set_main(value)

    def clear_all(self):
        history, value = self.engine.clear()
        self.display.set_history(history)
        self.display.set_main(value)

    def clear_entry(self):
        self.display.set_main("0")
        self.engine.expression = ""

    def backspace(self):
        current = self.display.get_main()
        if len(current) > 1:
            new_val = current[:-1]
            self.engine.expression = new_val
            self.display.set_main(new_val)
        else:
            self.engine.expression = ""
            self.display.set_main("0")

    def get_button_style(self, btn_type):
        if self.dark_mode:
            if btn_type == "number":
                return "QPushButton { background-color: #3c3c3c; color: white; border: none; border-radius: 4px; } QPushButton:hover { background-color: #4c4c4c; }"
            elif btn_type == "operator":
                return "QPushButton { background-color: #323232; color: #4cc2ff; border: none; border-radius: 4px; } QPushButton:hover { background-color: #424242; }"
            elif btn_type == "equals":
                return "QPushButton { background-color: #4cc2ff; color: black; border: none; border-radius: 4px; font-weight: bold; } QPushButton:hover { background-color: #5cd2ff; }"
            else:
                return "QPushButton { background-color: #323232; color: white; border: none; border-radius: 4px; } QPushButton:hover { background-color: #424242; }"
        else:
            if btn_type == "number":
                return "QPushButton { background-color: #f9f9f9; color: black; border: 1px solid #e0e0e0; border-radius: 4px; } QPushButton:hover { background-color: #e9e9e9; }"
            elif btn_type == "operator":
                return "QPushButton { background-color: #f0f0f0; color: #0078d4; border: 1px solid #e0e0e0; border-radius: 4px; } QPushButton:hover { background-color: #e0e0e0; }"
            elif btn_type == "equals":
                return "QPushButton { background-color: #0078d4; color: white; border: none; border-radius: 4px; font-weight: bold; } QPushButton:hover { background-color: #1088e4; }"
            else:
                return "QPushButton { background-color: #f0f0f0; color: black; border: 1px solid #e0e0e0; border-radius: 4px; } QPushButton:hover { background-color: #e0e0e0; }"

    def apply_theme(self):
        if self.dark_mode:
            self.setStyleSheet("QWidget { background-color: #202020; }")
            self.theme_btn.setText("☀️")
            self.display.setStyleSheet("""
                QLineEdit {
                    background-color: #202020;
                    color: white;
                    border: none;
                    selection-background-color: #0078d4;
                    selection-color: white;
                }
            """)
        else:
            self.setStyleSheet("QWidget { background-color: #f3f3f3; }")
            self.theme_btn.setText("🌙")
            self.display.setStyleSheet("""
                QLineEdit {
                    background-color: #f3f3f3;
                    color: black;
                    border: none;
                    selection-background-color: #0078d4;
                    selection-color: white;
                }
            """)
        
        for btn in self.findChildren(QPushButton):
            if btn != self.theme_btn:
                btn_type = btn.property("btn_type")
                if btn_type:
                    btn.setStyleSheet(self.get_button_style(btn_type))

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def button_clicked(self):
        button = self.sender()
        text = button.text()

        text_map = {
            "×": "*", "÷": "/", ",": ".", "⌫": "backspace",
            "CE": "clear_entry", "C": "clear", "+/-": "negate",
            "x²": "**2", "√x": "**0.5", "¹/ₓ": "1/",
        }

        mapped = text_map.get(text, text)

        if mapped == "clear": 
            self.clear_all()
        elif mapped == "clear_entry": 
            self.clear_entry()
        elif mapped == "backspace": 
            self.backspace()
        elif mapped == "negate":
            current = self.display.get_main()
            if current != "0":
                new_val = current[1:] if current.startswith("-") else "-" + current
                self.engine.expression = new_val
                self.display.set_main(new_val)
        elif mapped == "=": 
            self.calculate()
        elif mapped in ["**2", "**0.5", "1/"]:
            current = self.display.get_main()
            try:
                if mapped == "**2": 
                    result = str(eval(current + "**2"))
                    self.display.set_history(f"sqr({current})")
                elif mapped == "**0.5": 
                    result = str(eval(current + "**0.5"))
                    self.display.set_history(f"√({current})")
                elif mapped == "1/": 
                    result = str(eval("1/" + current))
                    self.display.set_history(f"1/({current})")
                self.display.set_main(result)
                self.engine.expression = result
            except: 
                self.display.set_main("Error")
                self.engine.expression = ""
        else: 
            self.process_input(mapped)