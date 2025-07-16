from ui.valiation_result import Ui_validation_form
from PySide6.QtWidgets import QWidget


class MyTemplateImport(QWidget):
    def __init__(self, validation_result: Ui_validation_form):
        super().__init__()
        self.ui_validation_result = validation_result
        self.ui_validation_result.setupUi(self)
