# TDD Changes Tracker

## [2026-08-10] Penyelarasan Arsitektur Model & Preprocessing dengan Notebook Training (`ser-augmemted.ipynb`)

### File Terdampak
- [model.py](file:///c:/Kuliah/Semester%20Antara/PM/EMOTION-DETECTION/ser-streamlit-app/model.py)
- [utils.py](file:///c:/Kuliah/Semester%20Antara/PM/EMOTION-DETECTION/ser-streamlit-app/utils.py)
- [pipeline/ser-augmemted.ipynb](file:///c:/Kuliah/Semester%20Antara/PM/EMOTION-DETECTION/ser-streamlit-app/pipeline/ser-augmemted.ipynb)

### Rincian Perubahan Skenario & Logic:
1. **Penyelarasan Classifier Non-Linearity (`model.py`)**:
   - **Sebelum:** Menggunakan `nn.ReLU()` pada dua layer classifier.
   - **Sesudah:** Diubah menjadi `nn.GELU()` dan disesuaikan posisi `nn.Dropout(dropout * 0.75)` agar **100% identik** dengan kelas `WavLMSER` pada notebook training v7 (`ser-augmemted.ipynb`).
   - **Alasan:** Perbedaan fungsi aktivasi antara training vs inferensi dapat menyebabkan penurunan performa prediksi saat memuat `ser_wavlm_v7_best.pt`.

2. **Koreksi Durasi Maksimum Audio (`utils.py`)**:
   - **Sebelum:** `MAX_DURATION_SECONDS = 8.0`
   - **Sesudah:** `MAX_DURATION_SECONDS = 4.0`
   - **Alasan:** Pada notebook `ser-augmemted.ipynb` Cell 4, `MAX_SECONDS` dikonfigurasi kaku pada **4.0 detik** (`MAX_SAMPLES = 64,000`). Menyesuaikan durasi inferensi ke 4.0s menjamin bentuk tensor input identik dengan kondisi saat model v7 dilatih.

## [2026-08-10] Verifikasi Path Dataset & Early Exit pada Notebook Training (`ser-augmemted.ipynb`)

### File Terdampak
- [ser-augmemted.ipynb](file:///c:/Kuliah/Semester%20Antara/PM/EMOTION-DETECTION/ser-streamlit-app/pipeline/ser-augmemted.ipynb)

### Rincian Perubahan Skenario & Logic:
1. **Verifikasi Jalur Multi-Kandidat & Early Exit (Cell 2 Konfigurasi Global)**:
   - **Sebelum:** Path dataset `KAGGLE_INDOWAVE`, `KAGGLE_RAVDESS`, `KAGGLE_EMODB`, `KAGGLE_CREMAD` di-hardcode ke `/kaggle/input/...` tanpa dilakukan pengecekan keberadaannya di awal. Jika dijalankan di lingkungan lokal/Colab, kode baru akan mendeteksi kegagalan di cell 3 setelah sempat memproses fungsi-fungsi lain.
   - **Sesudah:** Ditambahkan struktur `DATASET_CANDIDATES` untuk setiap dataset yang mencakup path Kaggle, Colab, dan lokal (`RAW_DIR` atau `./pipeline/Dataset`). Setiap dataset diperiksa dengan `os.path.isdir()`, mencetak status terdeteksi (dengan ikon status), dan jika tidak ada 1 pun dataset yang ditemukan (`found_count == 0`), eksekusi cell langsung dihentikan menggunakan `sys.exit()`.
   - **Alasan:** Mencegah notebook berjalan sia-sia sampai pertengahan cell jika dataset belum dimuat/di-mount di sistem.

## [2026-08-10] Pembersihan Emoji Dekoratif & Standarisasi Log Profesional (`ser-augmemted.ipynb`)

### File Terdampak
- [ser-augmemted.ipynb](file:///c:/Kuliah/Semester%20Antara/PM/EMOTION-DETECTION/ser-streamlit-app/pipeline/ser-augmemted.ipynb)

### Rincian Perubahan Skenario & Logic:
1. **Pembersihan Emoji Dekoratif & Simbol Non-Standard**:
   - **Sebelum:** Penggunaan emoji visual secara masif pada judul markdown, header, dan perintah print (`🔍`, `✅`, `❌`, `🛑`, `📌`, `🖥️`, `📂`, `📊`, `🔄`, `🔧`, `⏹`, `📉`, `🔁`, `🟡`, `📥`).
   - **Sesudah:** Mengubah seluruh output log dan header markdown menjadi string teks terstruktur standar berbasis tag profesional seperti `[OK]`, `[NOT FOUND]`, `[ERROR]`, `[CHECK]`, `[NOTE]`, `[STATS]`, `[CONFIG]`, `[BEST]`.
   - **Alasan:** Memenuhi standar Nol AI Slop proyek, meningkatkan keterbacaan log di terminal tanpa ketergantungan render font emoji, dan mencegah masalah encoding cp1252 pada lingkungan Windows.

## [2026-08-10] Pembentukan Custom Skill ML & Matriks Alur Kerja Wajib (`AGENTS.md`)

### File Terdampak
- [AGENTS.md](file:///c:/Kuliah/Semester%20Antara/PM/EMOTION-DETECTION/ser-streamlit-app/AGENTS.md)
- [.agents/skills/audio-pipeline-engineering/SKILL.md](file:///c:/Kuliah/Semester%20Antara/PM/EMOTION-DETECTION/ser-streamlit-app/.agents/skills/audio-pipeline-engineering/SKILL.md)
- [.agents/skills/pytorch-architecture-standards/SKILL.md](file:///c:/Kuliah/Semester%20Antara/PM/EMOTION-DETECTION/ser-streamlit-app/.agents/skills/pytorch-architecture-standards/SKILL.md)
- [.agents/skills/zero-ai-slop/SKILL.md](file:///c:/Kuliah/Semester%20Antara/PM/EMOTION-DETECTION/ser-streamlit-app/.agents/skills/zero-ai-slop/SKILL.md)

### Rincian Perubahan Skenario & Logic:
1. **Pembuatan 3 Custom Skill ML & Governance**:
   - `audio-pipeline-engineering`: Mengunci parameter pemrosesan sinyal suara 16 kHz mono, trim silence 30 dB, peak normalization, 4.0s pad/crop (64,000 sampel), dan SpecAugment.
   - `pytorch-architecture-standards`: Mengunci standar arsitektur PyTorch WavLM base-plus, Attentive Stats Pooling (output 1536), classifier LayerNorm -> Dropout -> Linear -> GELU -> Dropout -> Linear, dan gradual unfreezing 6 layer.
   - `zero-ai-slop`: Mengunci aturan larangan karakter em-dash, larangan emoji dekoratif, larangan basa-basi AI, dan mempertahankan penamaan emosi Bahasa Indonesia.
2. **Pembentukan Matriks Alur Kerja Skill 5-Fase pada `AGENTS.md`**:
   - Menjadikan eksekusi skill wajib berurutan (Fase 1 Hygiene -> Fase 2 Ideation & Planning -> Fase 3 Implementation -> Fase 4 Debugging -> Fase 5 Verification & Progress Tracking).
