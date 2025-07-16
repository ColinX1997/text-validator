# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_screen.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QSize
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QListWidget,
    QPlainTextEdit,
    QPushButton,
    QMessageBox,
    QComboBox,
    QRadioButton,
    QCheckBox,
)
from PySide6.QtGui import QIcon
from ui.telegram_import import Ui_telegram_import
from ui.valiation_result import Ui_validation_form
from objects.my_template_import import MyTemplateImport
from objects.my_validation_result import MyValidationResult
from objects.my_log_handler import LoggerManager
import glob, os, json


class Ui_TelegramValidator(object):
    def setupUi(self, TelegramValidator):
        if not TelegramValidator.objectName():
            TelegramValidator.setObjectName("TelegramValidator")
        TelegramValidator.resize(773, 578)

        icon = QIcon()
        icon.addFile(
            "resource\\icon.ico",
            QSize(97, 44),
            QIcon.Normal,
            QIcon.Off,
        )
        TelegramValidator.setWindowIcon(icon)

        self.tele_selector = QComboBox(TelegramValidator)
        self.tele_selector.setObjectName("tele_selector")
        self.tele_selector.setGeometry(QRect(20, 20, 256, 40))
        self.tele_selector_edit = self.tele_selector.lineEdit()
        self.tele_selector.setEditable(True)
        self.telegram_list = QListWidget(TelegramValidator)
        self.telegram_list.setObjectName("telegram_list")
        self.telegram_list.setGeometry(QRect(20, 60, 256, 480))
        self.telegram_list.setStyleSheet(
            "QListWidget::item:selected { background-color: lightblue; }"
        )
        self.import_btn = QPushButton(TelegramValidator)
        self.import_btn.setObjectName("import_btn")
        self.import_btn.setGeometry(QRect(310, 40, 101, 41))
        self.delete_btn = QPushButton(TelegramValidator)
        self.delete_btn.setObjectName("delete_btn")
        self.delete_btn.setGeometry(QRect(430, 40, 101, 41))
        self.refresh_btn = QPushButton(TelegramValidator)
        self.refresh_btn.setObjectName("refresh_btn")
        self.refresh_btn.setGeometry(QRect(550, 40, 101, 41))
        self.telegram_list_label = QLabel(TelegramValidator)
        self.telegram_list_label.setObjectName("telegram_list_label")
        self.telegram_list_label.setGeometry(QRect(310, 20, 201, 16))
        self.telegram_list_label.setFrameShape(QFrame.Shape.NoFrame)
        self.telegram_list_label.setFrameShadow(QFrame.Shadow.Plain)
        self.telegram_input_label = QLabel(TelegramValidator)
        self.telegram_input_label.setObjectName("telegram_input_label")
        self.telegram_input_label.setGeometry(QRect(310, 110, 201, 16))
        self.telegram_input_label.setFrameShape(QFrame.Shape.NoFrame)
        self.telegram_input_label.setFrameShadow(QFrame.Shadow.Plain)
        self.telegram_input = QPlainTextEdit(TelegramValidator)
        self.telegram_input.setObjectName("telegram_input")
        self.telegram_input.setGeometry(QRect(310, 140, 450, 380))
        self.validate_btn = QPushButton(TelegramValidator)
        self.validate_btn.setObjectName("validate_btn")
        self.validate_btn.setGeometry(QRect(660, 530, 101, 41))
        self.auto_paste_radio_open = QCheckBox(
            "Open Auto Paste Mode ", TelegramValidator
        )
        self.auto_paste_radio_open.setGeometry(310, 510, 200, 40)
        self.auto_paste_radio_open.setChecked(False)
        self.is_auto_paste = False

        self.retranslateUi(TelegramValidator)
        self.init_logger()
        self.init_telegram_selector()
        self.init_telegram_list()

        self.delete_btn.setDisabled(True)
        self.validate_btn.setDisabled(True)
        self.validate_btn.setToolTip(
            "Please choose one telegram type before do validation"
        )
        self.validate_btn.setStyleSheet(
            "QPushButton:disabled { background - color: gray; color: red; }"
        )

        self.import_btn.clicked.connect(self.import_template)
        self.delete_btn.clicked.connect(self.delete_template)
        self.refresh_btn.clicked.connect(self.init_telegram_list)
        self.validate_btn.clicked.connect(self.validate_telegram_format)
        self.telegram_list.itemClicked.connect(self.on_topic_item_click)
        self.tele_selector.activated.connect(self.set_telegram_list)
        self.tele_selector.currentTextChanged.connect(self.set_telegram_list)
        self.auto_paste_radio_open.toggled.connect(lambda: self.change_paste_mode())

        QMetaObject.connectSlotsByName(TelegramValidator)

    # setupUi

    def retranslateUi(self, TelegramValidator):
        TelegramValidator.setWindowTitle(
            QCoreApplication.translate(
                "TelegramValidator", "Telegram Validator v1.3", None
            )
        )
        self.import_btn.setText(
            QCoreApplication.translate("TelegramValidator", "Import", None)
        )
        self.delete_btn.setText(
            QCoreApplication.translate("TelegramValidator", "Delete", None)
        )
        self.validate_btn.setText(
            QCoreApplication.translate("TelegramValidator", "Validate", None)
        )
        self.refresh_btn.setText(
            QCoreApplication.translate("TelegramValidator", "Refresh", None)
        )
        self.telegram_input_label.setText(
            QCoreApplication.translate(
                "TelegramValidator", "Input your telegram content here:", None
            )
        )
        self.telegram_list_label.setText(
            QCoreApplication.translate(
                "TelegramValidator", "Manage the telegram list", None
            )
        )

    def init_logger(self):
        self.log_handler_info = LoggerManager.get_logger("MainScreen")

    # retranslateUi
    def import_template(self):
        ui_template_import = Ui_telegram_import()
        self.template_selector = MyTemplateImport(ui_template_import)
        self.template_selector.show()

    def init_telegram_selector(self):
        with open("config\\telegram_types.json") as file:
            config = json.load(file)
            connect_params = config["types"]
        self.tele_selector.addItems(connect_params)

    def init_telegram_list(self):
        self.telegram_list.clear()
        self.file_list = [
            os.path.basename(file)
            for file in glob.glob(os.path.join("telegrams", "*.json"))
        ]
        self.set_telegram_list()

    def set_telegram_list(self):
        self.telegram_list.clear()
        for file in self.file_list:
            telegram = file.replace(".json", "")
            if str(self.tele_selector.currentText()).lower() in str(telegram).lower():
                self.telegram_list.addItem(telegram)

    def delete_template(self):
        current_file = self.telegram_list.currentItem().text()

        files_to_delete = glob.glob(os.path.join("telegrams", current_file + ".json"))

        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                self.log_handler_info.info(file_path + " deleted successfully")
            except OSError as e:
                self.log_handler_info.info(
                    file_path + " cannot be deleted because" + str(e)
                )
        self.init_telegram_list()

    def validate_telegram_format(self):
        ui_validation_result = Ui_validation_form(
            str(self.telegram_list.currentItem().text()),
            str(self.telegram_input.toPlainText()),
        )
        try:
            self.validation_result_table = MyValidationResult(ui_validation_result)
            self.validation_result_table.show()
        except Exception as e:
            msg_box = QMessageBox()
            msg_box.setText(
                "Pleasea double check the telegram content and type!" + "\n" + str(e)
            )
            msg_box.setWindowTitle("Error")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

    def on_topic_item_click(self):
        self.delete_btn.setDisabled(False)
        self.validate_btn.setDisabled(False)

    def change_paste_mode(self):
        self.is_auto_paste = self.auto_paste_radio_open.isChecked()
