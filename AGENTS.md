# Project AGENTS.md — Speech Emotion Recognition (SER) & Streamlit App

File ini berisi panduan, aturan, serta standar eksekusi untuk agen AI dan pengembang yang bekerja pada repositori ini.

---

## 1. Project Overview & Architecture

Aplikasi ini adalah **Speech Emotion Recognition (SER)** berbasis model **WavLM** (`microsoft/wavlm-base-plus`) yang diintegrasikan dengan **Whisper STT** (`openai/whisper-small`) pada antarmuka web **Streamlit**.

### Core Architecture:
- `app.py`: Antarmuka Streamlit (UI/UX), pemrosesan parameter audio, integrasi STT, visualisasi probabilitas emosi.
- `model.py`: Arsitektur PyTorch (`WavLMSERModel`, `AttentionPooling`), fungsi ekstraksi checkpoint (`_extract_state_dict`), dan penanganan unduhan otomatis model dari Google Drive via `gdown`.
- `utils.py`: Preprocessing audio (resampling 16kHz, mono, pad/crop 8 detik, normalisasi) dan pipa inferensi.
- `models/`: Penyimpanan checkpoint model lokal (`ser_wavlm_v7_best.pt`).
- `requirements.txt`: Dependensi runtime Python (`torch`, `torchaudio`, `transformers`, `streamlit`, `librosa`, dll).

---

## 2. Mandatory Rules & Guidelines

### 2.1 Communication & Advisor Persona
- **Direct & Honest Advisor**: Jangan bersikap manis atau sekadar menyetujui (`no validation/comfort`). Tunjukkan kesalahan logika, kelemahan arsitektur, atau pemborosan waktu secara jujur, objektif, dan tajam.
- **Problem Exposer**: Jika ada *workaround* tidak efisien atau *mindset* yang menunda pekerjaan teknis, ungkapkan akar masalahnya beserta estimasi dampaknya secara terbuka.

### 2.2 UI/UX Design System: Mobile-First
- Semua perubahan visual atau antarmuka Streamlit **wajib dirancang dengan pendekatan Mobile-First**.
- Komponen layout, chart, sidebar, dan audio player harus adaptif pada viewport layar seluler (layar kecil) terlebih dahulu sebelum skala desktop.
- Hindari komponen yang memotong teks, chart horizontal yang *overflow* tanpa scroll pada layar kecil, atau layout multi-kolom kaku yang tidak merespons *responsive breakpoints*.

### 2.3 TDD & Change Tracking (`tdd_changes_tracker.md`)
- Setiap kali ada pembaruan, pergeseran spesifikasi, atau modifikasi pada siklus Test-Driven Development (TDD):
  1. Catat alasan perubahan, file terdampak, dan penyesuaian skenario pengujian.
  2. Masukkan catatannya ke file `tdd_changes_tracker.md`.

### 2.4 Progress Logging & Walkthrough Updates (`walkthrough.md`)
- Setelah menyelesaikan suatu task atau sub-task:
  1. Buat/perbarui file `walkthrough.md` pada folder artifacts/brain session.
### 2.5 Superpowers & Brainstorming Skill Enforcement
- **Wajib Menggunakan Skill `using-superpowers` & `brainstorming`**: Pada setiap pembahasan fitur, arsitektur, bugfix, atau perubahan desain, agent **WAJIB** secara eksplisit mengaktifkan skill `using-superpowers` dan `brainstorming` sebelum membuat keputusan atau menulis kode.
- **Workflow Pembahasan**: Eksplorasi konteks proyek -> Ajukan 2-3 pendekatan dengan analisis trade-off -> Sajikan rancangan desain -> Minta persetujuan user -> Tulis kode.

---

## 3. Workflow & Technical Constraints

1. **Inference Only Scope**: Repositori ini difokuskan khusus untuk inferensi dan antarmuka pengguna. Jangan menambahkan *script training* berat di dalam folder app utama tanpa pemisahan struktur yang jelas.
2. **Audio Specifications**:
   - Sample Rate: `16,000 Hz`
   - Channels: `Mono`
   - Max Duration for SER: `4.0 detik` (sesuai WavLM v7 model training)
   - STT Input: Full waveform (tanpa dipotong 4 detik)
3. **Execution Safety & Verification**:
   - Selalu jalankan uji verifikasi (unit test, `python -c "import model..."`, atau pembacaan sintaks) sebelum mengklaim pekerjaan selesai.

---

## 4. Professional Git Commit Guidelines (Conventional Commits)

Semua komitmen git pada repositori ini **wajib mematuhi standar Conventional Commits (v1.0.0)** dengan struktur sebagai berikut:

### Format Commit Message:
`<type>(<scope>): <subject>`

`[optional body]`

### Tipe Commit (`<type>`):
- `feat`: Penambahan fitur baru (misal: integrasi STT Whisper, audio recorder UI).
- `fix`: Perbaikan bug/error (misal: perbaikan `ImportError`, perbaikan `attention_mask`).
- `refactor`: Perubahan kode tanpa mengubah perilaku fitur (misal: penyelarasan arsitektur `GELU`).
- `docs`: Pembaruan dokumentasi (`AGENTS.md`, `README.md`, `walkthrough.md`, `tdd_changes_tracker.md`).
- `style`: Penyesuaian formatting, linting, tanpa perubahan logika bisnis.
- `test`: Penambahan atau perbaikan unit test.
- `chore`: Perubahan konfigurasi build, `.gitignore`, dependensi `requirements.txt`.

### Aturan Eksekusi Commit:
1. **Imperative Mood**: Gunakan kata kerja imperatif pada `<subject>` (contoh: `fix(pipeline): align classifier activation with GELU`, bukan `fixed` atau `fixing`).
2. **Singkat & Jelas**: Karakter subjek maksimum 50-72 karakter.
3. **Tanpa Garbage/Weights File**: Pastikan `.venv`, `__pycache__`, dan model weights `.pt` tidak masuk ke dalam staging `git add`.

---

## 5. Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit application
python -m streamlit run app.py
```
