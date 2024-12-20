import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QTextEdit, QToolBar, QAction, QSplitter, QCalendarWidget, 
    QDialog, QPushButton, QLabel, QGroupBox, QMessageBox, QComboBox, 
    QFontComboBox, QColorDialog, QStyleFactory, QStyle
)
from PyQt5.QtGui import QIcon, QKeySequence, QTextListFormat, QTextCursor, QFont, QPalette, QColor, QTextCharFormat, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QDate, QTimer

DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

HIGHLIGHT_COLOR = QColor("#FFFACD")  # Pastel yellow
AUTO_SAVE_DELAY = 1000  # 1 second delay

class CalendarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Date")
        layout = QVBoxLayout(self)

        self.calendar = QCalendarWidget(self)
        self.calendar.setSelectedDate(QDate.currentDate())
        layout.addWidget(self.calendar)

        select_btn = QPushButton("Select", self)
        select_btn.clicked.connect(self.accept)
        layout.addWidget(select_btn)

    def selectedDate(self):
        return self.calendar.selectedDate()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Journaling & To-Do App (Advanced Formatting)")
        self.resize(900, 600)

        self.selected_date = datetime.today().strftime("%Y-%m-%d")
        self.auto_save_timer = QTimer(self)
        self.auto_save_timer.setSingleShot(True)
        self.auto_save_timer.timeout.connect(self.save_journal)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10,10,10,10)

        # Top bar with date and calendar
        top_bar = QHBoxLayout()
        self.date_label = QLabel(f"Date: {self.selected_date}")
        top_bar.addWidget(self.date_label)
        top_bar.addStretch()

        calendar_btn = QPushButton("📅")
        calendar_btn.clicked.connect(self.open_calendar)
        calendar_btn.setFixedWidth(30)  # Make the calendar button narrower
        top_bar.addWidget(calendar_btn)

        main_layout.addLayout(top_bar)

        # Splitter for 50/50 layout
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(2)
        splitter.setStyleSheet("QSplitter::handle { background: #ddd; }")
        main_layout.addWidget(splitter)

        # ===== Journal Section =====
        journal_frame = QWidget()
        journal_layout = QVBoxLayout(journal_frame)
        journal_layout.setContentsMargins(5,5,5,5)

        j_title = QLabel("What's on your mind ?")
        j_title.setAlignment(Qt.AlignCenter)
        journal_layout.addWidget(j_title)

        # Formatting group with two lines
        formatting_group = QGroupBox("")  # We'll have a border now
        fg_layout = QVBoxLayout(formatting_group)
        fg_layout.setContentsMargins(5,5,5,5)

        # Top line: font size, font family, font color
        top_line = QHBoxLayout()
        self.font_size_combo = QComboBox()
        self.font_size_combo.setToolTip("Font Size")
        font_sizes = ["8", "9", "10", "11", "12", "14", "16", "18", "20", "24", "28", "32", "36", "48"]
        self.font_size_combo.addItems(font_sizes)
        self.font_size_combo.setEditable(True)
        self.font_size_combo.setCurrentText("14")
        self.font_size_combo.setFixedWidth(60)
        self.font_size_combo.currentIndexChanged.connect(self.change_font_size)
        self.font_size_combo.lineEdit().editingFinished.connect(self.change_font_size)

        self.font_family_combo = QFontComboBox()
        self.font_family_combo.setToolTip("Font Family")
        self.font_family_combo.currentFontChanged.connect(self.change_font_family)

        self.font_color_button = QPushButton()
        self.font_color_button.setToolTip("Change font color")
        # Use SP_DialogYesButton as a placeholder icon for font color
        color_icon_size = 16
        color_pixmap = QPixmap(color_icon_size, color_icon_size)
        color_pixmap.fill(Qt.transparent)

        painter = QPainter(color_pixmap)
        painter.fillRect(0, 0, color_icon_size, color_icon_size, QColor("#000000"))  # Black box for text color
        painter.end()

        self.font_color_button.setIcon(QIcon(color_pixmap))
        self.font_color_button.clicked.connect(self.select_font_color)

        top_line.addWidget(self.font_size_combo)
        top_line.addWidget(self.font_family_combo)
        top_line.addWidget(self.font_color_button)
        top_line.addStretch()
        fg_layout.addLayout(top_line)

        # Bottom line: formatting actions (bold, italic, underline, strike, bullet, number, highlight)
        bottom_line = QHBoxLayout()
        self.format_toolbar = QToolBar()
        self.format_toolbar.setMovable(False)

        bold_action = QAction("B", self)
        bold_action.setShortcut(QKeySequence.Bold)
        bold_action.triggered.connect(self.toggle_bold)
        self.format_toolbar.addAction(bold_action)

        italic_action = QAction("I", self)
        italic_action.setShortcut(QKeySequence.Italic)
        italic_action.triggered.connect(self.toggle_italic)
        self.format_toolbar.addAction(italic_action)

        underline_action = QAction("U", self)
        underline_action.setShortcut(QKeySequence.Underline)
        underline_action.triggered.connect(self.toggle_underline)
        self.format_toolbar.addAction(underline_action)

        strike_action = QAction("S", self)
        strike_action.setToolTip("Strikethrough")
        strike_action.triggered.connect(self.toggle_strike)
        self.format_toolbar.addAction(strike_action)

        bullet_action = QAction("•", self)
        bullet_action.setToolTip("Toggle bullet list")
        bullet_action.triggered.connect(self.toggle_bullet_list)
        self.format_toolbar.addAction(bullet_action)

        number_action = QAction("#", self)
        number_action.setToolTip("Toggle numbered list")
        number_action.triggered.connect(self.toggle_number_list)
        self.format_toolbar.addAction(number_action)

        highlight_action = QAction(self)
        highlight_action.setToolTip("Highlight text")
        # Use SP_TitleBarContextHelpButton as a placeholder icon for highlight
        highlight_icon_size = 16
        highlight_pixmap = QPixmap(highlight_icon_size, highlight_icon_size)
        highlight_pixmap.fill(Qt.transparent)

        painter = QPainter(highlight_pixmap)
        painter.fillRect(0, 0, highlight_icon_size, highlight_icon_size, QColor("#FFFACD"))  # Highlight color box

        # Draw the "H" inside using a contrasting color (e.g., black)
        painter.setPen(Qt.black)
        font = painter.font()
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(highlight_pixmap.rect(), Qt.AlignCenter, "H")
        painter.end()

        highlight_action.setIcon(QIcon(highlight_pixmap))
        highlight_action.triggered.connect(self.toggle_highlight)
        self.format_toolbar.addAction(highlight_action)

        bottom_line.addWidget(self.format_toolbar)
        bottom_line.addStretch()
        fg_layout.addLayout(bottom_line)

        journal_layout.addWidget(formatting_group)

        self.journal_text = QTextEdit()
        self.journal_text.setAcceptRichText(True)
        self.journal_text.textChanged.connect(self.on_journal_text_changed)
        # Always wrap at widget width
        self.journal_text.setLineWrapMode(QTextEdit.WidgetWidth)
        journal_layout.addWidget(self.journal_text)

        # ===== To-Do Section =====
        todo_frame = QWidget()
        todo_layout = QVBoxLayout(todo_frame)
        todo_layout.setContentsMargins(5,5,5,5)

        t_title = QLabel("What to do ?")
        t_title.setAlignment(Qt.AlignCenter)
        todo_layout.addWidget(t_title)

        self.todo_input = QTextEdit()
        self.todo_input.setPlaceholderText("Shift+Enter to add a new task, Enter for newline")
        self.todo_input.setFixedHeight(30)
        todo_layout.addWidget(self.todo_input)

        self.todo_scroll = QScrollArea()
        self.todo_scroll.setWidgetResizable(True)
        self.todo_container = QWidget()
        self.todo_vlayout = QVBoxLayout(self.todo_container)
        self.todo_vlayout.setContentsMargins(0,0,0,0)
        self.todo_vlayout.setSpacing(5)
        self.todo_scroll.setWidget(self.todo_container)
        todo_layout.addWidget(self.todo_scroll)

        splitter.addWidget(journal_frame)
        splitter.addWidget(todo_frame)
        splitter.setSizes([self.width()//2, self.width()//2])

        self.load_journal()
        self.load_tasks()

        self.journal_text.installEventFilter(self)
        self.todo_input.installEventFilter(self)

        # Apply simple light theme with white text boxes
        self.apply_light_theme()

    def eventFilter(self, source, event):
        if event.type() == event.KeyPress:
            if source == self.journal_text:
                if event.key() == Qt.Key_Return and (event.modifiers() & Qt.ShiftModifier):
                    self.save_journal()
                    return True
            elif source == self.todo_input:
                if event.key() == Qt.Key_Return:
                    if event.modifiers() & Qt.ShiftModifier:
                        self.add_task()
                        return True
                    else:
                        return False
        return super().eventFilter(source, event)

    def apply_light_theme(self):
        base_font_size = 14
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(236,236,236))  # Light gray UI background
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.Base, QColor(255,255,255))
        palette.setColor(QPalette.AlternateBase, QColor(235,235,235))
        palette.setColor(QPalette.ToolTipBase, Qt.black)
        palette.setColor(QPalette.ToolTipText, Qt.black)
        palette.setColor(QPalette.Text, Qt.black)
        palette.setColor(QPalette.Button, QColor(230,230,230))
        palette.setColor(QPalette.ButtonText, Qt.black)
        palette.setColor(QPalette.Highlight, QColor(180,220,240))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #ECECEC; /* Light gray background */
                color: #333;
                font-family: Arial;
                font-size: {base_font_size}px;
            }}
            QToolBar {{
                background: #F0F0F0;
                border: 1px solid #CCC;
            }}
            QGroupBox {{
                border: 1px solid #CCC; /* Reintroduce border around QGroupBox */
                margin-top: 6px;
            }}
            QPushButton {{
                background-color: #E6E6E6;
                color: #333;
                border-radius: 5px;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: #D8D8D8;
            }}
            QTextEdit, QComboBox, QFontComboBox {{
                background: #FFFFFF; /* White text boxes */
                color: #333;
                border: 1px solid #CCC;
            }}
            QScrollArea {{
                background: #ECECEC; /* Scroll areas remain light gray */
            }}
            QLabel {{
                color: #333;
            }}
        """)
        self.setPalette(palette)

    def change_font_size(self):
        text = self.font_size_combo.currentText().strip()
        if text.isdigit():
            size = int(text)
            if size > 0:
                fmt = self.journal_text.currentCharFormat()
                fmt.setFontPointSize(size)
                self.journal_text.setCurrentCharFormat(fmt)

    def change_font_family(self, font):
        fmt = self.journal_text.currentCharFormat()
        fmt.setFontFamily(font.family())
        self.journal_text.setCurrentCharFormat(fmt)

    def select_font_color(self):
        color = QColorDialog.getColor(initial=QColor("#333333"), parent=self, title="Select Font Color")
        if color.isValid():
            fmt = self.journal_text.currentCharFormat()
            fmt.setForeground(color)
            self.journal_text.setCurrentCharFormat(fmt)

    def toggle_bold(self):
        fmt = self.journal_text.currentCharFormat()
        new_weight = QFont.Bold if fmt.fontWeight() != QFont.Bold else QFont.Normal
        fmt.setFontWeight(new_weight)
        self.journal_text.setCurrentCharFormat(fmt)

    def toggle_italic(self):
        fmt = self.journal_text.currentCharFormat()
        fmt.setFontItalic(not fmt.fontItalic())
        self.journal_text.setCurrentCharFormat(fmt)

    def toggle_underline(self):
        fmt = self.journal_text.currentCharFormat()
        fmt.setFontUnderline(not fmt.fontUnderline())
        self.journal_text.setCurrentCharFormat(fmt)

    def toggle_strike(self):
        fmt = self.journal_text.currentCharFormat()
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())
        self.journal_text.setCurrentCharFormat(fmt)

    def toggle_bullet_list(self):
        cursor = self.journal_text.textCursor()
        cursor.beginEditBlock()
        current_list = cursor.currentList()
        if current_list and current_list.format().style() == QTextListFormat.ListDisc:
            self.remove_list_format(cursor)
        else:
            list_fmt = QTextListFormat()
            list_fmt.setStyle(QTextListFormat.ListDisc)
            cursor.createList(list_fmt)
        cursor.endEditBlock()

    def toggle_number_list(self):
        cursor = self.journal_text.textCursor()
        cursor.beginEditBlock()
        current_list = cursor.currentList()
        if current_list and current_list.format().style() == QTextListFormat.ListDecimal:
            self.remove_list_format(cursor)
        else:
            list_fmt = QTextListFormat()
            list_fmt.setStyle(QTextListFormat.ListDecimal)
            cursor.createList(list_fmt)
        cursor.endEditBlock()

    def remove_list_format(self, cursor):
        block_fmt = cursor.blockFormat()
        block_fmt.setObjectIndex(-1)
        cursor.setBlockFormat(block_fmt)

    def toggle_highlight(self):
        cursor = self.journal_text.textCursor()
        if cursor.hasSelection():
            cf = cursor.charFormat()
            current_bg = cf.background().color()
            fmt = QTextCharFormat(cf)
            if current_bg == HIGHLIGHT_COLOR:
                fmt.clearBackground()
            else:
                fmt.setBackground(HIGHLIGHT_COLOR)
            cursor.mergeCharFormat(fmt)

    def on_journal_text_changed(self):
        self.auto_save_timer.start(AUTO_SAVE_DELAY)

    def load_journal(self):
        html_content = ""
        file_path = self.get_journal_file_path(self.selected_date)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                html_content = f.read()
        self.journal_text.setHtml(html_content)

    def save_journal(self):
        file_path = self.get_journal_file_path(self.selected_date)
        html_content = self.journal_text.toHtml()
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    def load_tasks(self):
        # Remove existing tasks
        for i in reversed(range(self.todo_vlayout.count())):
            w = self.todo_vlayout.itemAt(i).widget()
            if w:
                w.deleteLater()

        tasks = []
        file_path = self.get_todo_file_path(self.selected_date)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                tasks = f.read().strip().split("\n")

        for t in tasks:
            if t.strip():
                self.create_task_widget(t)

    def save_tasks(self):
        tasks = []
        for i in range(self.todo_vlayout.count()):
            task_widget = self.todo_vlayout.itemAt(i).widget()
            if task_widget:
                lbl = task_widget.findChild(QLabel, "task_label")
                if lbl:
                    tasks.append(lbl.text().strip())
        file_path = self.get_todo_file_path(self.selected_date)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(tasks))

    def add_task(self):
        task = self.todo_input.toPlainText().strip()
        if task:
            self.create_task_widget(task)
            self.todo_input.clear()
            self.save_tasks()

    def create_task_widget(self, task_text):
        task_widget = QWidget()
        hbox = QHBoxLayout(task_widget)
        hbox.setContentsMargins(0,0,0,0)
        hbox.setSpacing(5)

        lbl = QLabel(task_text, objectName="task_label")
        lbl.setWordWrap(False)
        lbl.adjustSize()
        hbox.addWidget(lbl)

        remove_btn = QPushButton()
        remove_btn.setToolTip("Remove this task")
        remove_btn.setIcon(self.style().standardIcon(QStyle.SP_DockWidgetCloseButton))
        remove_btn.setFixedSize(20,20)
        remove_btn.clicked.connect(lambda: self.remove_task_widget(task_widget))
        hbox.addWidget(remove_btn)

        task_widget.adjustSize()

        self.todo_vlayout.addWidget(task_widget)
        self.todo_container.adjustSize()

    def remove_task_widget(self, widget):
        self.todo_vlayout.removeWidget(widget)
        widget.deleteLater()
        self.save_tasks()

    def open_calendar(self):
        dlg = CalendarDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            qdate = dlg.selectedDate()
            dt = datetime(qdate.year(), qdate.month(), qdate.day())
            self.selected_date = dt.strftime("%Y-%m-%d")
            self.date_label.setText(f"Date: {self.selected_date}")
            self.load_journal()
            self.load_tasks()

    def get_date_folder(self, date_str):
        date_folder = os.path.join(DATA_FOLDER, date_str)
        os.makedirs(date_folder, exist_ok=True)
        return date_folder

    def get_journal_file_path(self, date_str):
        date_folder = self.get_date_folder(date_str)
        return os.path.join(date_folder, "journal.html")

    def get_todo_file_path(self, date_str):
        date_folder = self.get_date_folder(date_str)
        return os.path.join(date_folder, "tasks.txt")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
