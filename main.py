import sys

from PySide6.QtWidgets import (
    QApplication
)

from src.interface.app import App

def main():

    app = QApplication(
        sys.argv
    )

    janela = App()

    janela.showMaximized()

    sys.exit(
        app.exec()
    )

if __name__ == "__main__":
    main()