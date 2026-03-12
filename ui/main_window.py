from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QPushButton, 
                             QHBoxLayout, QFrame, QLabel, QGraphicsDropShadowEffect,
                             QStackedWidget, QSizePolicy)
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QKeyEvent, QColor, QMouseEvent
from widgets.display import Display
from core.engine import CalculatorEngine


class TitleBar(QFrame):
    """Custom title bar sa Windows 11 stilom"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self._drag_pos = QPoint()
        self._is_dragging = False
        
        self.setFixedHeight(40)
        self.setObjectName("titleBar")
        
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(10)
        
        # Ikonica
        self.icon = QLabel("🧮", self)
        self.icon.setObjectName("titleIcon")
        self.icon.setFixedSize(24, 24)
        
        # Naslov
        self.title = QLabel("PyCalc Pro", self)
        self.title.setObjectName("titleLabel")
        self.title.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))  # ISPRAVLJENO
        
        # Spacer
        layout.addWidget(self.icon)
        layout.addWidget(self.title)
        layout.addStretch()
        
        # Dugmad za kontrolu prozora
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(0)
        
        self.min_btn = QPushButton("─", self)
        self.max_btn = QPushButton("□", self)
        self.close_btn = QPushButton("✕", self)
        
        for btn in [self.min_btn, self.max_btn, self.close_btn]:
            btn.setFixedSize(45, 30)
            btn.setFont(QFont("Segoe UI", 10))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_layout.addWidget(btn)
            
        self.min_btn.setObjectName("minBtn")
        self.max_btn.setObjectName("maxBtn")
        self.close_btn.setObjectName("closeBtn")
        
        layout.addLayout(btn_layout)
        
        # Konekcije
        self.min_btn.clicked.connect(self._minimize)
        self.max_btn.clicked.connect(self._maximize)
        self.close_btn.clicked.connect(self._close)
        
    def _minimize(self):
        self._parent.showMinimized()
        
    def _maximize(self):
        if self._parent.isMaximized():
            self._parent.showNormal()
            self.max_btn.setText("□")
        else:
            self._parent.showMaximized()
            self.max_btn.setText("❐")
            
    def _close(self):
        self._parent.close()
        
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_dragging = True
            self._drag_pos = event.globalPosition().toPoint() - self._parent.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event: QMouseEvent):
        if self._is_dragging and event.buttons() & Qt.MouseButton.LeftButton:
            if self._parent.isMaximized():
                self._parent.showNormal()
                self.max_btn.setText("□")
                self._drag_pos = QPoint(self._parent.width() // 2, 20)
            self._parent.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
            
    def mouseReleaseEvent(self, event: QMouseEvent):
        self._is_dragging = False
        
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._maximize()


class ModeSwitcher(QFrame):
    """Prebacivanje Standard/Scientific"""
    
    mode_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(36)
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        
        self.standard_btn = QPushButton("Standard")
        self.scientific_btn = QPushButton("Scientific")
        
        for btn in [self.standard_btn, self.scientific_btn]:
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Medium))  # ISPRAVLJENO
            layout.addWidget(btn)
            
        self.standard_btn.setChecked(True)
        
        self.standard_btn.clicked.connect(lambda: self._switch_mode("standard"))
        self.scientific_btn.clicked.connect(lambda: self._switch_mode("scientific"))
        
    def _switch_mode(self, mode):
        self.standard_btn.setChecked(mode == "standard")
        self.scientific_btn.setChecked(mode == "scientific")
        self.mode_changed.emit(mode)


class AnimatedButton(QPushButton):
    """Dugme sa animacijama"""
    
    def __init__(self, text, btn_type="number", parent=None):
        super().__init__(text, parent)
        self.btn_type = btn_type
        self.setFixedSize(70, 55)
        self.setFont(QFont("Segoe UI", 12))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Shadow efekat
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(0)
        self.shadow.setColor(QColor(0, 0, 0, 50))
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)
        
        # Animacije
        self.anim = QPropertyAnimation(self.shadow, b"blurRadius")
        self.anim.setDuration(150)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self.offset_anim = QPropertyAnimation(self.shadow, b"offset")
        self.offset_anim.setDuration(150)
        self.offset_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    def enterEvent(self, event):
        self.anim.setStartValue(0)
        self.anim.setEndValue(15)
        self.anim.start()
        
        self.offset_anim.setStartValue(QPoint(0, 0))
        self.offset_anim.setEndValue(QPoint(0, 4))
        self.offset_anim.start()
        
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.anim.setStartValue(15)
        self.anim.setEndValue(0)
        self.anim.start()
        
        self.offset_anim.setStartValue(QPoint(0, 4))
        self.offset_anim.setEndValue(QPoint(0, 0))
        self.offset_anim.start()
        
        super().leaveEvent(event)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        
        # Frameless prozor
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setFixedSize(380, 600)
        self.dark_mode = False
        self.engine = CalculatorEngine()
        
        self._setup_ui()
        self.apply_theme()
        self.setFocus()
        
    def _setup_ui(self):
        # Glavni layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Container za glassmorphism efekat
        self.container = QFrame()
        self.container.setObjectName("container")
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Title bar
        self.title_bar = TitleBar(self)
        container_layout.addWidget(self.title_bar)
        
        # Content area
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 10, 20, 20)
        content_layout.setSpacing(15)
        
        # Display
        self.display = Display()
        content_layout.addWidget(self.display)
        
        # Toolbar sa mode switcher-om i theme dugmetom
        toolbar = QHBoxLayout()
        
        self.mode_switcher = ModeSwitcher()
        self.mode_switcher.mode_changed.connect(self.switch_mode)
        toolbar.addWidget(self.mode_switcher)
        
        toolbar.addStretch()
        
        self.theme_btn = QPushButton("🌙")
        self.theme_btn.setFixedSize(40, 40)
        self.theme_btn.setObjectName("themeBtn")
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.clicked.connect(self.toggle_theme)
        toolbar.addWidget(self.theme_btn)
        
        content_layout.addLayout(toolbar)
        
        # Memory dugmad
        memory_layout = QHBoxLayout()
        memory_layout.setSpacing(8)
        
        for text in ["MC", "MR", "M+", "M-", "MS"]:
            btn = QPushButton(text)
            btn.setFixedHeight(32)
            btn.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold))  # ISPRAVLJENO
            btn.setObjectName("memoryBtn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            memory_layout.addWidget(btn)
            
        content_layout.addLayout(memory_layout)
        
        # Stacked widget za modove
        self.mode_stack = QStackedWidget()
        
        # Standard mod
        self.standard_widget = self._create_standard_buttons()
        self.mode_stack.addWidget(self.standard_widget)
        
        # Scientific mod
        self.scientific_widget = self._create_scientific_buttons()
        self.mode_stack.addWidget(self.scientific_widget)
        
        content_layout.addWidget(self.mode_stack)
        container_layout.addWidget(content)
        main_layout.addWidget(self.container)
        
    def _create_standard_buttons(self):
        widget = QWidget()
        grid = QGridLayout(widget)
        grid.setSpacing(8)
        
        buttons = [
            ("%", "special"), ("CE", "special"), ("C", "special"), ("⌫", "special"),
            ("¹/ₓ", "special"), ("x²", "special"), ("√x", "special"), ("÷", "operator"),
            ("7", "number"), ("8", "number"), ("9", "number"), ("×", "operator"),
            ("4", "number"), ("5", "number"), ("6", "number"), ("-", "operator"),
            ("1", "number"), ("2", "number"), ("3", "number"), ("+", "operator"),
            ("+/-", "special"), ("0", "number"), (",", "special"), ("=", "equals")
        ]
        
        positions = [(i, j) for i in range(6) for j in range(4)]
        
        for position, (text, btn_type) in zip(positions, buttons):
            btn = AnimatedButton(text, btn_type)
            btn.clicked.connect(self.button_clicked)
            btn.setProperty("btn_type", btn_type)
            grid.addWidget(btn, *position)
            
        return widget
        
    def _create_scientific_buttons(self):
        widget = QWidget()
        grid = QGridLayout(widget)
        grid.setSpacing(8)
        
        # Scientific dugmad
        sci_buttons = [
            ("2ⁿᵈ", "special"), ("π", "special"), ("e", "special"), ("C", "special"), ("⌫", "special"),
            ("x²", "special"), ("¹/ₓ", "special"), ("|x|", "special"), ("exp", "special"), ("mod", "special"),
            ("√x", "special"), ("(", "special"), (")", "special"), ("n!", "special"), ("÷", "operator"),
            ("xʸ", "special"), ("7", "number"), ("8", "number"), ("9", "number"), ("×", "operator"),
            ("10ˣ", "special"), ("4", "number"), ("5", "number"), ("6", "number"), ("-", "operator"),
            ("log", "special"), ("1", "number"), ("2", "number"), ("3", "number"), ("+", "operator"),
            ("ln", "special"), ("+/-", "special"), ("0", "number"), (",", "special"), ("=", "equals")
        ]
        
        positions = [(i, j) for i in range(7) for j in range(5)]
        
        for position, (text, btn_type) in zip(positions, sci_buttons):
            btn = AnimatedButton(text, btn_type)
            btn.setFixedSize(60, 48)  # Malo manje zbog više dugmadi
            btn.clicked.connect(self.button_clicked)
            btn.setProperty("btn_type", btn_type)
            grid.addWidget(btn, *position)
            
        return widget
        
    def switch_mode(self, mode):
        if mode == "standard":
            self.mode_stack.setCurrentIndex(0)
            self.setFixedSize(380, 600)
        else:
            self.mode_stack.setCurrentIndex(1)
            self.setFixedSize(420, 650)
            
    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        text = event.text()
        
        if text.isdigit():
            self.process_input(text)
        elif text in ['+', '-', '*', '/']:
            self.process_input(text)
        elif key == Qt.Key.Key_Plus:
            self.process_input('+')
        elif key == Qt.Key.Key_Minus:
            self.process_input('-')
        elif key == Qt.Key.Key_Asterisk:
            self.process_input('*')
        elif key == Qt.Key.Key_Slash:
            self.process_input('/')
        elif text in ['.', ',']:
            self.process_input('.')
        elif key in [Qt.Key.Key_Period, Qt.Key.Key_Comma]:
            self.process_input('.')
        elif key in [Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Equal]:
            self.calculate()
        elif key == Qt.Key.Key_Escape:
            self.clear_all()
        elif key == Qt.Key.Key_Backspace:
            self.backspace()
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
            styles = {
                "number": "background-color: #3c3c3c; color: white; border: none; border-radius: 8px;",
                "operator": "background-color: #323232; color: #4cc2ff; border: none; border-radius: 8px;",
                "equals": "background-color: #4cc2ff; color: black; border: none; border-radius: 8px; font-weight: bold;",
                "special": "background-color: #323232; color: white; border: none; border-radius: 8px; font-size: 11px;"
            }
        else:
            styles = {
                "number": "background-color: #f9f9f9; color: black; border: 1px solid #e5e5e5; border-radius: 8px;",
                "operator": "background-color: #f0f0f0; color: #0078d4; border: 1px solid #e5e5e5; border-radius: 8px;",
                "equals": "background-color: #0078d4; color: white; border: none; border-radius: 8px; font-weight: bold;",
                "special": "background-color: #f0f0f0; color: black; border: 1px solid #e5e5e5; border-radius: 8px; font-size: 11px;"
            }
        return styles.get(btn_type, styles["number"])
        
    def apply_theme(self):
        if self.dark_mode:
            # Tamna tema sa glassmorphism efektom
            self.setStyleSheet("""
                QWidget {
                    background: transparent;
                }
                #container {
                    background: rgba(32, 32, 32, 0.95);
                    border-radius: 16px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }
                #titleBar {
                    background: rgba(40, 40, 40, 0.8);
                    border-top-left-radius: 16px;
                    border-top-right-radius: 16px;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                }
                #titleLabel {
                    color: #ffffff;
                }
                #minBtn, #maxBtn {
                    background: transparent;
                    color: #ffffff;
                    border: none;
                    border-radius: 6px;
                }
                #minBtn:hover, #maxBtn:hover {
                    background: rgba(255, 255, 255, 0.1);
                }
                #closeBtn {
                    background: transparent;
                    color: #ffffff;
                    border: none;
                    border-radius: 6px;
                }
                #closeBtn:hover {
                    background: #e81123;
                    color: white;
                }
                #themeBtn {
                    background: rgba(255, 255, 255, 0.1);
                    color: white;
                    border: none;
                    border-radius: 20px;
                    font-size: 16px;
                }
                #themeBtn:hover {
                    background: rgba(255, 255, 255, 0.2);
                }
                ModeSwitcher {
                    background: rgba(255, 255, 255, 0.05);
                    border-radius: 8px;
                }
                ModeSwitcher QPushButton {
                    background: transparent;
                    color: #888;
                    border: none;
                    border-radius: 6px;
                    padding: 6px 16px;
                }
                ModeSwitcher QPushButton:checked {
                    background: rgba(255, 255, 255, 0.15);
                    color: white;
                }
                ModeSwitcher QPushButton:hover:!checked {
                    color: #aaa;
                }
                #memoryBtn {
                    background: rgba(255, 255, 255, 0.05);
                    color: #888;
                    border: none;
                    border-radius: 6px;
                }
                #memoryBtn:hover {
                    background: rgba(255, 255, 255, 0.1);
                    color: white;
                }
            """)
            self.theme_btn.setText("☀️")
            self.display.setStyleSheet("""
                QLineEdit {
                    background: transparent;
                    color: white;
                    border: none;
                    selection-background-color: #0078d4;
                    selection-color: white;
                }
            """)
        else:
            # Svetla tema sa glassmorphism efektom
            self.setStyleSheet("""
                QWidget {
                    background: transparent;
                }
                #container {
                    background: rgba(243, 243, 243, 0.95);
                    border-radius: 16px;
                    border: 1px solid rgba(255, 255, 255, 0.8);
                    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
                }
                #titleBar {
                    background: rgba(255, 255, 255, 0.6);
                    border-top-left-radius: 16px;
                    border-top-right-radius: 16px;
                    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
                }
                #titleLabel {
                    color: #1a1a1a;
                }
                #minBtn, #maxBtn {
                    background: transparent;
                    color: #1a1a1a;
                    border: none;
                    border-radius: 6px;
                }
                #minBtn:hover, #maxBtn:hover {
                    background: rgba(0, 0, 0, 0.05);
                }
                #closeBtn {
                    background: transparent;
                    color: #1a1a1a;
                    border: none;
                    border-radius: 6px;
                }
                #closeBtn:hover {
                    background: #e81123;
                    color: white;
                }
                #themeBtn {
                    background: rgba(0, 0, 0, 0.05);
                    color: #1a1a1a;
                    border: none;
                    border-radius: 20px;
                    font-size: 16px;
                }
                #themeBtn:hover {
                    background: rgba(0, 0, 0, 0.1);
                }
                ModeSwitcher {
                    background: rgba(0, 0, 0, 0.03);
                    border-radius: 8px;
                }
                ModeSwitcher QPushButton {
                    background: transparent;
                    color: #666;
                    border: none;
                    border-radius: 6px;
                    padding: 6px 16px;
                }
                ModeSwitcher QPushButton:checked {
                    background: white;
                    color: #1a1a1a;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                }
                ModeSwitcher QPushButton:hover:!checked {
                    color: #333;
                }
                #memoryBtn {
                    background: rgba(0, 0, 0, 0.03);
                    color: #666;
                    border: none;
                    border-radius: 6px;
                }
                #memoryBtn:hover {
                    background: rgba(0, 0, 0, 0.06);
                    color: #1a1a1a;
                }
            """)
            self.theme_btn.setText("🌙")
            self.display.setStyleSheet("""
                QLineEdit {
                    background: transparent;
                    color: black;
                    border: none;
                    selection-background-color: #0078d4;
                    selection-color: white;
                }
            """)
            
        # Osveži stilove dugmadi
        for btn in self.findChildren(AnimatedButton):
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
            "π": "3.14159265359", "e": "2.71828182846",
            "mod": "%", "n!": "factorial", "|x|": "abs",
            "(": "(", ")": ")",
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
        elif mapped in ["factorial", "abs"]:
            current = self.display.get_main()
            try:
                if mapped == "factorial":
                    import math
                    result = str(math.factorial(int(float(current))))
                    self.display.set_history(f"fact({current})")
                elif mapped == "abs":
                    result = str(abs(float(current)))
                    self.display.set_history(f"abs({current})")
                self.display.set_main(result)
                self.engine.expression = result
            except:
                self.display.set_main("Error")
                self.engine.expression = ""
        else: 
            self.process_input(mapped)