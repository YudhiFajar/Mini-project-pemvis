"""
views/dialog_jurnal.py
Dialog terpisah untuk tambah dan edit entri jurnal

Nama  : Yudhi Fajar Pratama
NIM   : F1D02310142
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QComboBox, QDateEdit,
    QPushButton, QLabel, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont


MOODS = ["😊 Senang", "😐 Biasa", "😢 Sedih", "😡 Marah", "😴 Lelah", "🥰 Cinta", "😰 Cemas"]
KATEGORI = ["Pribadi", "Pekerjaan", "Kesehatan", "Perjalanan", "Keluarga", "Hobi", "Lainnya"]
CUACA = ["☀️ Cerah", "⛅ Berawan", "🌧️ Hujan", "⛈️ Badai", "🌫️ Berkabut", "🌙 Malam"]


class DialogJurnal(QDialog):
    """Dialog untuk menambah atau mengedit entri jurnal."""

    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.data = data  # Jika tidak None, mode edit
        self.is_edit = data is not None
        self.setWindowTitle("Edit Jurnal" if self.is_edit else "Tulis Jurnal Baru")
        self.setMinimumWidth(520)
        self.setMinimumHeight(560)
        self.setModal(True)
        self._build_ui()
        if self.is_edit:
            self._populate_data()

    def _build_ui(self):
        """Membangun tampilan dialog."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # Header
        title_label = QLabel("✏️ Edit Jurnal" if self.is_edit else "📖 Tulis Jurnal Baru")
        title_label.setObjectName("dialogTitle")
        main_layout.addWidget(title_label)

        # Garis pemisah
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setObjectName("divider")
        main_layout.addWidget(line)

        # Form layout
        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight)

        # Field 1: Judul
        self.input_judul = QLineEdit()
        self.input_judul.setPlaceholderText("Judul entri jurnal...")
        self.input_judul.setObjectName("inputField")
        form.addRow("📝 Judul:", self.input_judul)

        # Field 2: Tanggal
        self.input_tanggal = QDateEdit()
        self.input_tanggal.setCalendarPopup(True)
        self.input_tanggal.setDate(QDate.currentDate())
        self.input_tanggal.setObjectName("inputField")
        form.addRow("📅 Tanggal:", self.input_tanggal)

        # Field 3: Mood
        self.input_mood = QComboBox()
        self.input_mood.addItems(MOODS)
        self.input_mood.setObjectName("inputField")
        form.addRow("💭 Mood:", self.input_mood)

        # Field 4: Kategori
        self.input_kategori = QComboBox()
        self.input_kategori.addItems(KATEGORI)
        self.input_kategori.setObjectName("inputField")
        form.addRow("🏷️ Kategori:", self.input_kategori)

        # Field 5: Cuaca
        self.input_cuaca = QComboBox()
        self.input_cuaca.addItems(CUACA)
        self.input_cuaca.setObjectName("inputField")
        form.addRow("🌤️ Cuaca:", self.input_cuaca)

        # Field 6: Isi jurnal
        self.input_isi = QTextEdit()
        self.input_isi.setPlaceholderText("Ceritakan hari-harimu di sini...")
        self.input_isi.setMinimumHeight(150)
        self.input_isi.setObjectName("inputIsi")
        form.addRow("📄 Isi:", self.input_isi)

        main_layout.addLayout(form)

        # Tombol aksi
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_batal = QPushButton("Batal")
        self.btn_batal.setObjectName("btnBatal")
        self.btn_batal.clicked.connect(self.reject)

        self.btn_simpan = QPushButton("💾 Simpan Jurnal" if not self.is_edit else "💾 Update Jurnal")
        self.btn_simpan.setObjectName("btnSimpan")
        self.btn_simpan.setDefault(True)
        self.btn_simpan.clicked.connect(self._simpan)

        btn_layout.addWidget(self.btn_batal)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_simpan)
        main_layout.addLayout(btn_layout)

    def _populate_data(self):
        """Mengisi form dengan data yang akan diedit."""
        self.input_judul.setText(self.data["judul"])

        tanggal = QDate.fromString(self.data["tanggal"], "yyyy-MM-dd")
        if tanggal.isValid():
            self.input_tanggal.setDate(tanggal)

        idx_mood = self.input_mood.findText(self.data["mood"])
        if idx_mood >= 0:
            self.input_mood.setCurrentIndex(idx_mood)

        idx_kat = self.input_kategori.findText(self.data["kategori"])
        if idx_kat >= 0:
            self.input_kategori.setCurrentIndex(idx_kat)

        idx_cuaca = self.input_cuaca.findText(self.data["cuaca"])
        if idx_cuaca >= 0:
            self.input_cuaca.setCurrentIndex(idx_cuaca)

        self.input_isi.setPlainText(self.data["isi"])

    def _simpan(self):
        """Validasi dan konfirmasi penyimpanan."""
        judul = self.input_judul.text().strip()
        isi = self.input_isi.toPlainText().strip()

        if not judul:
            QMessageBox.warning(self, "Validasi", "Judul tidak boleh kosong!")
            self.input_judul.setFocus()
            return

        if not isi:
            QMessageBox.warning(self, "Validasi", "Isi jurnal tidak boleh kosong!")
            self.input_isi.setFocus()
            return

        self.accept()

    def get_data(self):
        """Mengembalikan data yang diinput dari form."""
        return {
            "judul": self.input_judul.text().strip(),
            "tanggal": self.input_tanggal.date().toString("yyyy-MM-dd"),
            "mood": self.input_mood.currentText(),
            "kategori": self.input_kategori.currentText(),
            "isi": self.input_isi.toPlainText().strip(),
            "cuaca": self.input_cuaca.currentText(),
        }
