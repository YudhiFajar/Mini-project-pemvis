"""
views/main_window.py
Jendela utama aplikasi Jurnal Harian

Nama  : Yudhi Fajar Pratama
NIM   : F1D02310142
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel,
    QLineEdit, QComboBox, QMessageBox, QFrame, QHeaderView,
    QMenuBar, QMenu, QStatusBar, QSplitter, QTextEdit
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QFont, QColor

from controllers.jurnal_controller import JurnalController
from views.dialog_jurnal import DialogJurnal, KATEGORI, MOODS


class MainWindow(QMainWindow):
    """Jendela utama aplikasi Catatan Harian / Jurnal."""

    NAMA_MAHASISWA = "Yudhi Fajar Pratama"
    NIM_MAHASISWA = "F1D02310142"

    def __init__(self):
        super().__init__()
        self.controller = JurnalController()
        self.setWindowTitle("📔 Jurnal Harianku")
        self.setMinimumSize(1000, 650)
        self.resize(1100, 700)
        self._build_menu()
        self._build_ui()
        self._build_statusbar()
        self.muat_data()

    # ──────────────────────────── MENU BAR ────────────────────────────
    def _build_menu(self):
        menubar = self.menuBar()

        # Menu File
        menu_file = menubar.addMenu("File")
        act_tambah = QAction("➕ Tambah Jurnal Baru", self)
        act_tambah.setShortcut("Ctrl+N")
        act_tambah.triggered.connect(self.buka_dialog_tambah)
        menu_file.addAction(act_tambah)

        menu_file.addSeparator()
        act_keluar = QAction("❌ Keluar", self)
        act_keluar.setShortcut("Ctrl+Q")
        act_keluar.triggered.connect(self.close)
        menu_file.addAction(act_keluar)

        # Menu Data
        menu_data = menubar.addMenu("Data")
        act_refresh = QAction("🔄 Refresh Data", self)
        act_refresh.setShortcut("F5")
        act_refresh.triggered.connect(self.muat_data)
        menu_data.addAction(act_refresh)

        act_hapus = QAction("🗑️ Hapus Entri Dipilih", self)
        act_hapus.triggered.connect(self.hapus_jurnal)
        menu_data.addAction(act_hapus)

        # Menu Tentang
        menu_tentang = menubar.addMenu("Tentang")
        act_tentang = QAction("ℹ️ Tentang Aplikasi", self)
        act_tentang.triggered.connect(self.tampilkan_tentang)
        menu_tentang.addAction(act_tentang)

    # ──────────────────────────── UI UTAMA ────────────────────────────
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Header ──
        header = QWidget()
        header.setObjectName("headerWidget")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 16, 24, 16)

        # Kiri: judul aplikasi
        left = QVBoxLayout()
        app_title = QLabel("📔 Jurnal Harianku")
        app_title.setObjectName("appTitle")
        left.addWidget(app_title)

        tagline = QLabel("Catat setiap momen berharga dalam hidupmu")
        tagline.setObjectName("appTagline")
        left.addWidget(tagline)
        header_layout.addLayout(left)

        header_layout.addStretch()

        # Kanan: nama dan NIM (tidak bisa diedit)
        right = QVBoxLayout()
        right.setAlignment(Qt.AlignRight)
        lbl_nama = QLabel(f"👤 {self.NAMA_MAHASISWA}")
        lbl_nama.setObjectName("labelNama")
        lbl_nim = QLabel(f"🎓 {self.NIM_MAHASISWA}")
        lbl_nim.setObjectName("labelNIM")
        right.addWidget(lbl_nama)
        right.addWidget(lbl_nim)
        header_layout.addLayout(right)

        root.addWidget(header)

        # ── Toolbar (filter + tombol) ──
        toolbar = QWidget()
        toolbar.setObjectName("toolbarWidget")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(20, 10, 20, 10)
        toolbar_layout.setSpacing(10)

        # Search
        self.input_cari = QLineEdit()
        self.input_cari.setPlaceholderText("🔍 Cari jurnal...")
        self.input_cari.setObjectName("searchField")
        self.input_cari.textChanged.connect(self.muat_data)
        toolbar_layout.addWidget(self.input_cari, 2)

        # Filter Kategori
        self.combo_kategori = QComboBox()
        self.combo_kategori.addItem("Semua Kategori")
        self.combo_kategori.addItems(KATEGORI)
        self.combo_kategori.setObjectName("filterCombo")
        self.combo_kategori.currentTextChanged.connect(self._on_filter_changed)
        toolbar_layout.addWidget(self.combo_kategori)

        # Filter Mood
        self.combo_mood = QComboBox()
        self.combo_mood.addItem("Semua Mood")
        self.combo_mood.addItems(MOODS)
        self.combo_mood.setObjectName("filterCombo")
        self.combo_mood.currentTextChanged.connect(self._on_filter_changed)
        toolbar_layout.addWidget(self.combo_mood)

        toolbar_layout.addStretch()

        # Tombol Tambah
        self.btn_tambah = QPushButton("➕ Tulis Jurnal")
        self.btn_tambah.setObjectName("btnPrimary")
        self.btn_tambah.clicked.connect(self.buka_dialog_tambah)
        toolbar_layout.addWidget(self.btn_tambah)

        # Tombol Edit
        self.btn_edit = QPushButton("✏️ Edit")
        self.btn_edit.setObjectName("btnSecondary")
        self.btn_edit.clicked.connect(self.buka_dialog_edit)
        toolbar_layout.addWidget(self.btn_edit)

        # Tombol Hapus
        self.btn_hapus = QPushButton("🗑️ Hapus")
        self.btn_hapus.setObjectName("btnDanger")
        self.btn_hapus.clicked.connect(self.hapus_jurnal)
        toolbar_layout.addWidget(self.btn_hapus)

        root.addWidget(toolbar)

        # ── Splitter: Tabel kiri + Preview kanan ──
        splitter = QSplitter(Qt.Horizontal)
        splitter.setObjectName("mainSplitter")

        # Tabel jurnal
        self.tabel = QTableWidget()
        self.tabel.setObjectName("mainTable")
        self.tabel.setColumnCount(6)
        self.tabel.setHorizontalHeaderLabels(["ID", "Tanggal", "Judul", "Mood", "Kategori", "Cuaca"])
        self.tabel.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabel.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabel.setAlternatingRowColors(True)
        self.tabel.verticalHeader().setVisible(False)
        self.tabel.setColumnHidden(0, True)  # Sembunyikan kolom ID
        header_tabel = self.tabel.horizontalHeader()
        header_tabel.setSectionResizeMode(2, QHeaderView.Stretch)
        self.tabel.doubleClicked.connect(self.buka_dialog_edit)
        self.tabel.selectionModel().selectionChanged.connect(self._on_row_selected)
        splitter.addWidget(self.tabel)

        # Panel preview kanan
        preview_panel = QWidget()
        preview_panel.setObjectName("previewPanel")
        preview_layout = QVBoxLayout(preview_panel)
        preview_layout.setContentsMargins(16, 16, 16, 16)
        preview_layout.setSpacing(8)

        lbl_preview = QLabel("📄 Pratinjau Jurnal")
        lbl_preview.setObjectName("previewTitle")
        preview_layout.addWidget(lbl_preview)

        self.lbl_judul_preview = QLabel("—")
        self.lbl_judul_preview.setObjectName("previewJudul")
        self.lbl_judul_preview.setWordWrap(True)
        preview_layout.addWidget(self.lbl_judul_preview)

        meta_layout = QHBoxLayout()
        self.lbl_tanggal_preview = QLabel()
        self.lbl_tanggal_preview.setObjectName("previewMeta")
        self.lbl_mood_preview = QLabel()
        self.lbl_mood_preview.setObjectName("previewMeta")
        meta_layout.addWidget(self.lbl_tanggal_preview)
        meta_layout.addStretch()
        meta_layout.addWidget(self.lbl_mood_preview)
        preview_layout.addLayout(meta_layout)

        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setObjectName("divider")
        preview_layout.addWidget(line2)

        self.text_isi_preview = QTextEdit()
        self.text_isi_preview.setReadOnly(True)
        self.text_isi_preview.setObjectName("previewIsi")
        self.text_isi_preview.setPlaceholderText("Pilih entri jurnal untuk melihat isinya...")
        preview_layout.addWidget(self.text_isi_preview)

        splitter.addWidget(preview_panel)
        splitter.setSizes([600, 380])

        root.addWidget(splitter, 1)

        # ── Statistik bawah ──
        stats_bar = QWidget()
        stats_bar.setObjectName("statsBar")
        stats_layout = QHBoxLayout(stats_bar)
        stats_layout.setContentsMargins(20, 8, 20, 8)

        self.lbl_total = QLabel("Total: 0 entri")
        self.lbl_total.setObjectName("statsLabel")
        self.lbl_mood_fav = QLabel("Mood favorit: —")
        self.lbl_mood_fav.setObjectName("statsLabel")
        self.lbl_kat_fav = QLabel("Kategori terbanyak: —")
        self.lbl_kat_fav.setObjectName("statsLabel")

        stats_layout.addWidget(self.lbl_total)
        stats_layout.addStretch()
        stats_layout.addWidget(self.lbl_mood_fav)
        stats_layout.addStretch()
        stats_layout.addWidget(self.lbl_kat_fav)

        root.addWidget(stats_bar)

    def _build_statusbar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Siap | Jurnal Harianku - Yudhi Fajar Pratama / F1D02310142")

    # ──────────────────────────── LOGIKA ────────────────────────────
    def _on_filter_changed(self, _):
        self.muat_data()

    def muat_data(self):
        """Memuat ulang data dari database ke tabel."""
        keyword = self.input_cari.text().strip()
        kategori = self.combo_kategori.currentText()
        if kategori == "Semua Kategori":
            kategori = "Semua"
        mood = self.combo_mood.currentText()
        if mood == "Semua Mood":
            mood = "Semua"

        rows = self.controller.ambil_semua(keyword, kategori, mood)
        self.tabel.setRowCount(len(rows))

        for i, row in enumerate(rows):
            self.tabel.setItem(i, 0, QTableWidgetItem(str(row["id"])))
            self.tabel.setItem(i, 1, QTableWidgetItem(row["tanggal"]))
            self.tabel.setItem(i, 2, QTableWidgetItem(row["judul"]))
            self.tabel.setItem(i, 3, QTableWidgetItem(row["mood"]))
            self.tabel.setItem(i, 4, QTableWidgetItem(row["kategori"]))
            self.tabel.setItem(i, 5, QTableWidgetItem(row["cuaca"]))

        # Update statistik
        stat = self.controller.statistik()
        self.lbl_total.setText(f"📚 Total: {stat['total']} entri")
        self.lbl_mood_fav.setText(f"💭 Mood favorit: {stat['mood_terbanyak']}")
        self.lbl_kat_fav.setText(f"🏷️ Kategori terbanyak: {stat['kategori_terbanyak']}")

        self.status_bar.showMessage(f"Menampilkan {len(rows)} entri jurnal")

    def _on_row_selected(self):
        """Memperbarui panel preview saat baris dipilih."""
        selected = self.tabel.selectedItems()
        if not selected:
            self.lbl_judul_preview.setText("—")
            self.lbl_tanggal_preview.setText("")
            self.lbl_mood_preview.setText("")
            self.text_isi_preview.clear()
            return

        row = self.tabel.currentRow()
        jurnal_id = int(self.tabel.item(row, 0).text())
        data = self.controller.ambil_by_id(jurnal_id)
        if data:
            self.lbl_judul_preview.setText(data["judul"])
            self.lbl_tanggal_preview.setText(f"📅 {data['tanggal']}  {data['cuaca']}")
            self.lbl_mood_preview.setText(data["mood"])
            self.text_isi_preview.setPlainText(data["isi"])

    def _get_selected_id(self):
        """Mengambil ID jurnal yang dipilih di tabel."""
        row = self.tabel.currentRow()
        if row < 0:
            return None
        item = self.tabel.item(row, 0)
        return int(item.text()) if item else None

    def buka_dialog_tambah(self):
        """Membuka dialog untuk menambah jurnal baru."""
        dialog = DialogJurnal(self)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.controller.tambah(
                    data["judul"], data["tanggal"], data["mood"],
                    data["kategori"], data["isi"], data["cuaca"]
                )
                self.muat_data()
                self.status_bar.showMessage("✅ Jurnal baru berhasil ditambahkan!")
            except ValueError as e:
                QMessageBox.warning(self, "Gagal Menyimpan", str(e))

    def buka_dialog_edit(self):
        """Membuka dialog untuk mengedit jurnal yang dipilih."""
        jurnal_id = self._get_selected_id()
        if jurnal_id is None:
            QMessageBox.information(self, "Info", "Pilih entri jurnal yang ingin diedit.")
            return

        data = self.controller.ambil_by_id(jurnal_id)
        if data is None:
            return

        dialog = DialogJurnal(self, data=dict(data))
        if dialog.exec():
            form_data = dialog.get_data()
            try:
                self.controller.update(
                    jurnal_id, form_data["judul"], form_data["tanggal"],
                    form_data["mood"], form_data["kategori"],
                    form_data["isi"], form_data["cuaca"]
                )
                self.muat_data()
                self.status_bar.showMessage("✅ Jurnal berhasil diperbarui!")
            except ValueError as e:
                QMessageBox.warning(self, "Gagal Update", str(e))

    def hapus_jurnal(self):
        """Menghapus jurnal yang dipilih setelah konfirmasi."""
        jurnal_id = self._get_selected_id()
        if jurnal_id is None:
            QMessageBox.information(self, "Info", "Pilih entri jurnal yang ingin dihapus.")
            return

        konfirmasi = QMessageBox.question(
            self, "Konfirmasi Hapus",
            "Apakah kamu yakin ingin menghapus entri jurnal ini?\n"
            "Tindakan ini tidak dapat dibatalkan.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if konfirmasi == QMessageBox.Yes:
            self.controller.hapus(jurnal_id)
            self.muat_data()
            self.text_isi_preview.clear()
            self.lbl_judul_preview.setText("—")
            self.status_bar.showMessage("🗑️ Jurnal berhasil dihapus.")

    def tampilkan_tentang(self):
        """Menampilkan dialog Tentang Aplikasi."""
        QMessageBox.information(
            self,
            "Tentang Aplikasi",
            "📔  Jurnal Harianku\n\n"
            "Aplikasi Catatan Harian berbasis PySide6 untuk mencatat\n"
            "momen, perasaan, dan kegiatan sehari-hari.\n\n"
            "Fitur:\n"
            "  • Tulis & kelola entri jurnal harian\n"
            "  • Filter berdasarkan mood dan kategori\n"
            "  • Pencarian cepat\n"
            "  • Penyimpanan data persisten (SQLite)\n\n"
            f"👤 Nama   : {self.NAMA_MAHASISWA}\n"
            f"🎓 NIM    : {self.NIM_MAHASISWA}\n\n"
            "Mata Kuliah : Pemrograman Visual (PV26)\n"
            "Framework   : PySide6 + SQLite"
        )
