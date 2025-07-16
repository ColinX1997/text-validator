# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'valiation_result.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QMetaObject,
    QRect,
)
from PySide6.QtWidgets import (
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QTextBrowser,
    QApplication,
    QMessageBox,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QBrush
from PySide6.QtGui import QIcon
from objects.my_log_handler import LoggerManager
from objects.rule.rule import Validator
import json, datetime


class Ui_validation_form(object):
    def __init__(self, telegram_template, telegram_content):
        self.telegram_template = telegram_template
        self.telegram_content = telegram_content

    def setupUi(self, validation_form):
        if not validation_form.objectName():
            validation_form.setObjectName("validation_form")
        validation_form.resize(1200, 649)
        icon = QIcon()
        icon.addFile(
            "resource\\icon.ico",
            QSize(97, 44),
            QIcon.Normal,
            QIcon.Off,
        )
        validation_form.setWindowIcon(icon)
        self.ok_btn = QPushButton(validation_form)
        self.ok_btn.setObjectName("ok_btn")
        self.ok_btn.setGeometry(QRect(1050, 610, 75, 30))
        self.status_summary_box = QTextBrowser(validation_form)
        self.status_summary_box.setObjectName("status_summary_box")
        self.status_summary_box.setGeometry(QRect(400, 610, 600, 30))
        self.regen_btn = QPushButton(validation_form)
        self.regen_btn.setObjectName("regen_btn")
        self.regen_btn.setGeometry(QRect(150, 610, 221, 30))
        self.randomDate_btn = QPushButton(validation_form)
        self.randomDate_btn.setObjectName("randomDate_btn")
        self.randomDate_btn.setGeometry(QRect(20, 610, 120, 30))

        self.result_table = QTableWidget(validation_form)
        if self.result_table.columnCount() < 6:
            self.result_table.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.result_table.setObjectName("result_table")
        self.result_table.setGeometry(QRect(20, 20, 1150, 581))
        self.result_table.setColumnWidth(1, 50)
        self.result_table.setColumnWidth(2, 50)

        header = self.result_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.Stretch)

        self.retranslateUi(validation_form)
        self.init_logger()
        self.init_config(self.telegram_template)
        self.ok_btn.clicked.connect(validation_form.hide)
        self.regen_btn.clicked.connect(self.regenerate_tele)
        self.randomDate_btn.clicked.connect(self.regenerate_date)
        self.result_table.itemChanged.connect(self.on_cell_changed)

        QMetaObject.connectSlotsByName(validation_form)

    # setupUi

    def retranslateUi(self, validation_form):
        validation_form.setWindowTitle(
            QCoreApplication.translate(
                "validation_form", "Validation result: " + self.telegram_template, None
            )
        )
        self.ok_btn.setText(QCoreApplication.translate("validation_form", "OK", None))
        self.regen_btn.setText(
            QCoreApplication.translate(
                "validation_form", "Generate telegram based on new values", None
            )
        )
        self.randomDate_btn.setText(
            QCoreApplication.translate("validation_form", "Use current datetime", None)
        )
        ___qtablewidgetitem = self.result_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(
            QCoreApplication.translate("validation_form", "Description", None)
        )
        ___qtablewidgetitem1 = self.result_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(
            QCoreApplication.translate("validation_form", "Position", None)
        )
        ___qtablewidgetitem2 = self.result_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(
            QCoreApplication.translate("validation_form", "Length", None)
        )
        ___qtablewidgetitem3 = self.result_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(
            QCoreApplication.translate("validation_form", "Format", None)
        )
        ___qtablewidgetitem4 = self.result_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(
            QCoreApplication.translate("validation_form", "Status", None)
        )
        ___qtablewidgetitem5 = self.result_table.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(
            QCoreApplication.translate("validation_form", "Value", None)
        )

    def init_config(self, telegram_template):
        validator = Validator()
        path = "telegrams\\" + telegram_template + ".json"
        with open(path, "r") as file:
            template_data = json.load(file)
        if len(template_data) > 0:
            # get how many info rows
            info_rows_count = 0
            last_valid_startpoint = 0
            # insert template and content into table
            for row in range(len(template_data)):
                start_point = template_data[row]["StartPoint"]
                length = template_data[row]["Length"]

                # insert startpoint, length, desc & format
                self.result_table.insertRow(row)
                for col, value in enumerate(template_data[row]):
                    if isinstance(value, bytes):
                        value = value.decode()
                    item = QTableWidgetItem(str(template_data[row][value]))
                    self.result_table.setItem(row, col, item)

                # normal case
                if isinstance(start_point, int):
                    if "x" in str(length) and row == len(template_data) - 1:
                        context_part = self.telegram_content[start_point - 1 :]
                    else:
                        context_part = self.telegram_content[
                            start_point - 1 : start_point - 1 + length
                        ]
                        last_valid_startpoint = start_point - 1 + length

                    # insert value parts
                    value_item = QTableWidgetItem(str(context_part))
                    self.result_table.setItem(
                        row, self.result_table.columnCount() - 1, value_item
                    )
                else:
                    info_rows_count += 1

                # insert validation result
                if (
                    not isinstance(start_point, int)
                    or str(template_data[row]["StartPoint"]).lower() == "info"
                ):
                    status_item = QTableWidgetItem("Please check manually")
                else:
                    valid_result = validator.validate_rule(
                        template_data[row]["Format"], context_part
                    )
                    status_item = QTableWidgetItem(str(valid_result))
                    if "Correct" in valid_result:
                        status_item.setBackground(QBrush(QColor("lightgreen")))
                    else:
                        if (
                            "Optional" in template_data[row]
                            and str(template_data[row]["Optional"]) == "O"
                        ):
                            status_item.setBackground(QBrush(QColor("lightblue")))
                        else:
                            status_item.setBackground(QBrush(QColor("red")))

                self.result_table.setItem(
                    row, self.result_table.columnCount() - 2, status_item
                )

            if (info_rows_count) > 0:
                self.result_table.setSpan(
                    len(template_data) - info_rows_count,
                    self.result_table.columnCount() - 1,
                    info_rows_count,
                    1,
                )
                self.result_table.setItem(
                    len(template_data) - info_rows_count,
                    self.result_table.columnCount() - 1,
                    QTableWidgetItem(
                        str(self.telegram_content[last_valid_startpoint:])
                    ),
                )

            # check length
            status = "Length correct"
            if info_rows_count > 0 or isinstance(
                template_data[len(template_data) - 1]["Length"], str
            ):
                status = "Skip length check since there are dynamic fields"
            else:
                template_length = (
                    int(template_data[len(template_data) - 1]["StartPoint"])
                    + int(template_data[len(template_data) - 1]["Length"])
                    - 1
                )
                if len(self.telegram_content) != template_length:
                    status = f"Length wrong, template: {template_length}, actual content: {len(self.telegram_content)}"
                    if len(self.telegram_content) > template_length:
                        status += (
                            " Redundant parts: "
                            + self.telegram_content[template_length:]
                        )
                    self.log_handler_info.info(status)
            self.status_summary_box.append(status)
            self.disable_result()

    def disable_result(self):
        for col in range(self.result_table.columnCount()):
            for row in range(self.result_table.rowCount()):
                item = self.result_table.item(row, col)
                if col != 5:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

        last_column = self.result_table.columnCount() - 1
        for row in range(self.result_table.rowCount()):
            item = self.result_table.item(row, last_column)
            if item:
                item.setFlags(
                    Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
                )
                item.setBackground(QColor(204, 239, 240))

    def init_logger(self):
        self.log_handler_info = LoggerManager.get_logger("ValidationScreen")

    def regenerate_tele(self):
        new_tele = ""
        row_count = self.result_table.rowCount()
        for row in range(row_count):
            item = self.result_table.item(row, self.result_table.columnCount() - 1)
            if item:
                new_tele += item.text()

        clipboard = QApplication.clipboard()
        clipboard.setText(new_tele)
        msg_box = QMessageBox()
        msg_box.setText("Telegram copied to clipboard")
        msg_box.setWindowTitle("Info")
        msg_box.setStandardButtons(QMessageBox.Ok)

        msg_box.exec()

    def regenerate_date(self):
        row_count = self.result_table.rowCount()
        for row in range(row_count):
            last_item = self.result_table.item(row, self.result_table.columnCount() - 1)
            last_item_text = last_item.text()
            if len(last_item_text) >= 14:
                old_date_str = last_item_text[:14]
                if self.is_valid_timestamp(old_date_str):
                    now = datetime.datetime.now()
                    new_date_str = now.strftime("%Y%m%d%H%M%S")
                    last_item.setText(
                        last_item_text.replace(old_date_str, new_date_str)
                    )

    def is_valid_timestamp(self, timestamp_str):
        try:
            dt = datetime.datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
            return True
        except ValueError:
            return False

    def on_cell_changed(self, item):
        row = self.result_table.row(item)
        column = self.result_table.column(item)

        if column != self.result_table.columnCount() - 1:
            return
        current_text = self.result_table.item(row, column).text()
        current_rule = self.result_table.item(
            row, self.result_table.columnCount() - 3
        ).text()

        # if current rule is 'xx padded with spaces', then fullfill the text with space automatically
        if "padded with spaces" in current_rule:
            desired_length = int(
                self.result_table.item(row, self.result_table.columnCount() - 4).text()
            )
            current_text = "{:<{}}".format(current_text, desired_length)
            item.setText(current_text)

        validator = Validator()
        valid_result = validator.validate_rule(current_rule, current_text)
        status_item = QTableWidgetItem(str(valid_result))
        if "Correct" in valid_result:
            status_item.setBackground(QBrush(QColor("lightgreen")))
        else:
            status_item.setBackground(QBrush(QColor("red")))
        self.result_table.setItem(row, self.result_table.columnCount() - 2, status_item)
