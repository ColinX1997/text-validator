import sys
from PySide6.QtWidgets import QApplication
from objects.my_mainscreen import MyMainScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = MyMainScreen()
    main.show()

    sys.exit(app.exec())
