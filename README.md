# SPK Seleksi Beasiswa — Streamlit App

Sistem Pendukung Keputusan untuk seleksi penerima beasiswa menggunakan
metode SAW, SMART, MOORA, dan Weighted Product.

## Cara Deploy ke Streamlit Community Cloud

### Langkah 1 — Siapkan Repository GitHub

1. Buat akun GitHub di https://github.com jika belum punya
2. Buat repository baru (klik New repository)
   - Nama: `spk-beasiswa` (atau nama lain)
   - Visibility: **Public**
   - Klik **Create repository**

### Langkah 2 — Upload File ke Repository

Upload file-file berikut ke repository:
```
spk-beasiswa/
├── app.py
├── requirements.txt
└── .streamlit/
    └── config.toml
```

**Cara upload via GitHub web:**
1. Buka repository yang baru dibuat
2. Klik **Add file → Upload files**
3. Drag & drop semua file di atas
4. Klik **Commit changes**

**Atau via Git (jika sudah install Git):**
```bash
git clone https://github.com/USERNAME/spk-beasiswa.git
cd spk-beasiswa
# copy semua file ke folder ini
git add .
git commit -m "Initial commit"
git push origin main
```

### Langkah 3 — Deploy ke Streamlit Cloud

1. Buka https://share.streamlit.io
2. Login dengan akun GitHub
3. Klik **New app**
4. Isi form:
   - **Repository**: `USERNAME/spk-beasiswa`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Klik **Deploy!**
6. Tunggu 2–3 menit proses build

### Langkah 4 — Selesai

App akan tersedia di URL:
`https://USERNAME-spk-beasiswa-app-XXXX.streamlit.app`

---

## Cara Jalankan Lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```

App akan terbuka di http://localhost:8501
