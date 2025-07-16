from ui.main_screen import Ui_TelegramValidator
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QWidget,
    QApplication,
)


class MyMainScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.ui_main = Ui_TelegramValidator()
        self.ui_main.setupUi(self)

        self.clipboard_timer = QTimer(self)
        self.clipboard_timer.timeout.connect(self.onClipboardChanged)
        self.clipboard_timer.start(2000)

        self.clipboard_text = ""

    def onClipboardChanged(self):
        clipboard = QApplication.clipboard()
        if clipboard.mimeData().hasText() and self.ui_main.is_auto_paste:
            text_from_clipboard = clipboard.text()
            if (
                self.ui_main.telegram_input.toPlainText() == ""
                and text_from_clipboard != self.clipboard_text
            ):
                cursor = self.ui_main.telegram_input.textCursor()
                cursor.insertText(text_from_clipboard)
                self.clipboard_text = text_from_clipboard
                self.ui_main.validate_btn.setFocus()
