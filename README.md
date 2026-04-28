# 📔 Jurnal Harianku

Aplikasi Catatan Harian berbasis **PySide6** untuk mencatat momen, perasaan, dan kegiatan sehari-hari dengan penyimpanan data persisten menggunakan SQLite.

---

## 👤 Identitas Mahasiswa

| Field | Detail |
|-------|--------|
| **Nama** | Yudhi Fajar Pratama |
| **NIM** | F1D02310142 |
| **Mata Kuliah** | Pemrograman Visual (PV26) |

---

## 📋 Deskripsi Aplikasi

**Jurnal Harianku** adalah aplikasi GUI desktop yang memungkinkan pengguna untuk:
- ✍️ Menulis dan menyimpan catatan harian
- 😊 Merekam mood dan cuaca setiap hari
- 🏷️ Mengkategorikan entri jurnal
- 🔍 Mencari dan memfilter catatan dengan cepat
- 👁️ Melihat pratinjau isi jurnal langsung di jendela utama
- 📊 Melihat statistik ringkas (total entri, mood & kategori favorit)

---

## 🚀 Cara Menjalankan

### Persyaratan
- Python 3.10 atau lebih baru
- PySide6

### Instalasi Dependensi
```bash
pip install PySide6
```

### Menjalankan Aplikasi
```bash
# Clone/download repository, lalu masuk ke folder project
cd pv26-miniproject-jurnalharian-F1D02310142

# Jalankan aplikasi
python main.py
```

> Database SQLite (`data/jurnal.db`) akan dibuat secara otomatis saat aplikasi pertama kali dijalankan.

---

## 🏗️ Struktur Project (Separation of Concerns)

```
pv26-miniproject-jurnalharian-F1D02310142/
│
├── main.py                     # Entry point aplikasi
│
├── views/                      # Layer tampilan (UI)
│   ├── __init__.py
│   ├── main_window.py          # Jendela utama
│   └── dialog_jurnal.py        # Dialog tambah / edit
│
├── controllers/                # Layer logika bisnis
│   ├── __init__.py
│   └── jurnal_controller.py    # Controller CRUD jurnal
│
├── database/                   # Layer akses data
│   ├── __init__.py
│   └── db_manager.py           # Manajemen SQLite
│
├── styles/                     # Layer styling
│   └── style.qss               # Stylesheet QSS eksternal
│
├── data/                       # Folder database (auto-generated)
│   └── jurnal.db               # File SQLite
│
└── README.md
```

---

## 🛠️ Teknologi yang Digunakan

| Teknologi | Kegunaan |
|-----------|----------|
| **Python 3.10+** | Bahasa pemrograman utama |
| **PySide6** | Framework GUI desktop |
| **SQLite** | Database penyimpanan lokal |
| **QSS** | Styling antarmuka (eksternal) |

---

## ✅ Fitur yang Diimplementasikan

- [x] Form input dengan **6 field** (Judul, Tanggal, Mood, Kategori, Cuaca, Isi)
- [x] **Signals & Slots** untuk semua interaksi komponen
- [x] Layout rapi menggunakan `QVBoxLayout`, `QHBoxLayout`, `QFormLayout`
- [x] Tampilan data dengan `QTableWidget` + panel pratinjau `QTextEdit`
- [x] **SQLite CRUD** lengkap (Create, Read, Update, Delete) — data persisten
- [x] **Menu bar** dengan menu Tentang Aplikasi
- [x] **Dialog terpisah** untuk tambah/edit (jendela utama hanya menampilkan data)
- [x] **Dialog konfirmasi** sebelum menghapus (`QMessageBox.question`)
- [x] Nama dan NIM tampil di header utama (tidak bisa diedit)
- [x] **Styling QSS dari file eksternal** (`styles/style.qss`)
- [x] **Separation of Concerns** — View / Controller / Database dipisah jelas

---

## 🎬 Link YouTube

> *(Tambahkan link video YouTube di sini setelah upload)*

---

## 📄 Laporan PDF

> *(Tersedia di dalam repository sebagai `laporan.pdf`)*
