"""
Aplikasi Catatan Harian / Jurnal
Entry point utama aplikasi

Nama  : Yudhi Fajar Pratama
NIM   : F1D02310142
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from views.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Jurnal Harianku")
    app.setOrganizationName("PV26")

    # Load QSS styling dari file eksternal
    try:
        with open("styles/style.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Warning: File style.qss tidak ditemukan.")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
