# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'telegram_import.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QFileDialog
from objects.my_log_handler import LoggerManager
import pandas as pd
import json
import os


class Ui_telegram_import(object):
    def setupUi(self, telegram_import):
        if not telegram_import.objectName():
            telegram_import.setObjectName("telegram_import")
        telegram_import.resize(515, 143)
        icon = QIcon()
        icon.addFile(
            "resource\\icon.ico",
            QSize(97, 44),
            QIcon.Normal,
            QIcon.Off,
        )
        telegram_import.setWindowIcon(icon)

        self.telegram_import_window = telegram_import

        self.file_path_input = QLineEdit(telegram_import)
        self.file_path_input.setObjectName("file_path")
        self.file_path_input.setGeometry(QRect(20, 50, 421, 31))
        self.file_selector_btn = QPushButton(telegram_import)
        self.file_selector_btn.setObjectName("file_selector_btn")
        self.file_selector_btn.setGeometry(QRect(450, 50, 51, 31))
        icon = QIcon(QIcon.fromTheme("go-home"))
        self.file_selector_btn.setIcon(icon)
        self.import_btn = QPushButton(telegram_import)
        self.import_btn.setObjectName("import_btn")
        self.import_btn.setGeometry(QRect(200, 100, 180, 31))
        self.hint_label = QLabel(telegram_import)
        self.hint_label.setObjectName("hint_label")
        self.hint_label.setGeometry(QRect(20, 20, 151, 16))
        self.file_dialog = QFileDialog(telegram_import)

        self.retranslateUi(telegram_import)
        self.init_logger()

        self.file_selector_btn.clicked.connect(self.open_file_dialog)
        self.import_btn.clicked.connect(self.import_telegram_templates)

        QMetaObject.connectSlotsByName(telegram_import)

    # setupUi

    def retranslateUi(self, telegram_import):
        telegram_import.setWindowTitle(
            QCoreApplication.translate("telegram_import", "Import telegrams", None)
        )
        self.file_selector_btn.setText("")
        self.import_btn.setText(
            QCoreApplication.translate(
                "telegram_import", "Import Telegram Templates", None
            )
        )
        self.hint_label.setText(
            QCoreApplication.translate(
                "telegram_import", "Please choose one excel file to import:", None
            )
        )

    def init_logger(self):
        self.log_handler_info = LoggerManager.get_logger("TelegramImpot")

    def open_file_dialog(self):
        file_path, _ = self.file_dialog.getOpenFileName(
            self.telegram_import_window,
            "Choose File",
            "",
            "Excel(*.xlsx)",
        )
        if file_path:
            self.file_path_input.setText(file_path)

    # check why only one could be imported successfully
    def import_telegram_templates(self):
        excel_file_path = self.file_path_input.text()
        # excel_file_path = ""
        output_dir = "telegrams"
        # read excel
        workbook = pd.read_excel(excel_file_path, sheet_name=None)
        # ensure it's valid path
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            for sheet_name, df in workbook.items():
                # check columns
                if (
                    "Description" in df.columns
                    and "StartPoint" in df.columns
                    and "Length" in df.columns
                    and "Format" in df.columns
                ):
                    # replce space with _
                    df["Description"] = df["Description"].str.replace(" ", "_")
                    columns_to_use = ["Description", "StartPoint", "Length", "Format"]
                    if "Optional" in df.columns:
                        columns_to_use.append("Optional")
                    # transfer DataFrame into dict
                    data = df[columns_to_use].to_dict(orient="records")

                    # create json for each sheet
                    json_file_path = os.path.join(output_dir, f"{sheet_name}.json")
                    if os.path.exists(json_file_path):
                        self.log_handler_info.info(
                            json_file_path
                            + " already exist, delete old one and replace with new one"
                        )
                        os.remove(json_file_path)

                    with open(json_file_path, "w", encoding="utf-8") as json_file:
                        json.dump(data, json_file, indent=4, ensure_ascii=False)
                    self.log_handler_info.info(
                        str(json_file_path) + " generated successfully"
                    )
                else:
                    self.log_handler_info.info(
                        f"Sheet '{sheet_name}'lack of needed columns, please check again"
                    )

        except Exception as e:
            self.log_handler_info.info(str(e))
        finally:
            self.telegram_import_window.close()
