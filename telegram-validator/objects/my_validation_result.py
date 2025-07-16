from ui.telegram_import import Ui_telegram_import
from PySide6.QtWidgets import QWidget


class MyValidationResult(QWidget):
    def __init__(self, template_importor: Ui_telegram_import):
        super().__init__()
        self.ui_template_importor = template_importor
        self.ui_template_importor.setupUi(self)
