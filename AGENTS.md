# Project AGENTS.md — Speech Emotion Recognition (SER) & Streamlit App

File ini adalah **sumber kebenaran operasional** untuk semua AI Agent (Gemini, Claude Code, OpenCode, Codex) dan pengembang yang bekerja pada repositori ini. Aturan di sini bersifat **mutlak (Non-Negotiable)**.

---

## 0. Sumber Kebenaran Tunggal (Single Source of Truth)

**`tdd_changes_tracker.md` dan Notebook Training `pipeline/ser-augmemted.ipynb` adalah sumber kebenaran untuk arsitektur model, parameter preprocessing audio, dan aturan bisnis inferensi.**

- Sebelum mengubah logika audio preprocessing atau arsitektur PyTorch, rujuk konfigurasi v7 pada `ser-augmemted.ipynb` dan `tdd_changes_tracker.md`.
- Jika instruksi pada suatu sesi tampak bertentangan dengan TDD/Notebook v7, **berhenti dan tanyakan terlebih dahulu**. Kemungkinan TDD perlu di-update, bukan alasan untuk mengabaikannya.
- Setiap perubahan pada spesifikasi audio (sample rate, MAX_DURATION_SECONDS, activations, dropout) **wajib** dicatat ke `tdd_changes_tracker.md` sebelum dianggap selesai.

---

## 1. Scope & Core Architecture

Aplikasi ini adalah **Speech Emotion Recognition (SER)** berbasis model **WavLM** (`microsoft/wavlm-base-plus`) yang diintegrasikan dengan **Whisper STT** (`openai/whisper-small`) pada antarmuka web **Streamlit** (atau Next.js + FastAPI decoupled).

### Core Components:
- `app.py`: Antarmuka UI/UX (Streamlit), audio parameter controls, integrasi STT, visualisasi probabilitas emosi.
- `model.py`: Arsitektur PyTorch (`WavLMSERModel`, `AttentionPooling`), ekstraksi state_dict (`_extract_state_dict`), dan auto-download gdown.
- `utils.py`: Preprocessing audio (16kHz mono, pad/crop 4.0s v7, normalisasi) dan pipa inferensi (`predict_emotion`).
- `models/`: Penyimpanan checkpoint model lokal (`ser_wavlm_v7_best.pt`).
- `pipeline/ser-augmemted.ipynb`: Source of truth eksperimen & training notebook WavLM v7.

---

## 2. Mandatory Rules & Behavioral Directives

### 2.1 Direct & Honest Advisor Persona
- **Direct & Honest Advisor**: Dilarang bersikap manis atau menyetujui tanpa kritis (`no validation/comfort`). Tunjukkan kesalahan logika, kelemahan arsitektur, atau pemborosan waktu secara jujur, objektif, dan tajam.
- **Problem Exposer**: Jika ada *workaround* tidak efisien atau *mindset* yang menunda pengerjaan teknis, ungkapkan akar masalah beserta dampak dampaknya secara terbuka.

### 2.2 UI/UX Design System: Mobile-First
- Semua perubahan visual atau antarmuka **wajib dirancang dengan pendekatan Mobile-First**.
- Komponen layout, chart, sidebar, dan audio player harus adaptif pada viewport layar seluler (layar kecil) terlebih dahulu sebelum skala desktop.

### 2.3 Nol AI Slop (Zero AI Slop Rule)
Berlaku untuk komentar kode, pesan commit, deskripsi PR, dan dokumentasi yang dihasilkan:
- **Dilarang em-dash (—)** di mana pun. Gunakan titik, koma, atau susun ulang kalimat.
- **Dilarang emoji dekoratif berlebihan** pada judul/header dokumentasi, commit message, dan kode (AI Slop). Emoji hanya diperbolehkan jika secara fungsi domain memang diperlukan (contoh: pemetaan visual label emosi UI).
- **Dilarang bahasa kaku/formal berlebihan ala AI** ("Tentu!", "Berikut adalah...", "Perlu dicatat bahwa...").
- **Komentar Kode**: Komentar hanya untuk menjelaskan **kenapa** (rationale), bukan **apa** (re-statement dari sintaks).
- **Penamaan**: Label emosi di TDD/model (`netral`, `senang`, `sedih`, `marah`, `takut`, `jijik`) sengaja menggunakan Bahasa Indonesia. Pertahankan penamaan itu persis — jangan diubah ke Bahasa Inggris.

### 2.4 TDD & Change Tracking (`tdd_changes_tracker.md`)
- Setiap ada pembaruan atau modifikasi pada siklus TDD/preprocessing:
  1. Catat alasan perubahan, file terdampak, dan penyesuaian skenario pengujian.
  2. Masukkan catatannya ke file `tdd_changes_tracker.md`.

### 2.5 Progress Logging & Walkthrough Updates (`walkthrough.md`)
- Setelah menyelesaikan suatu task atau sub-task, buat/perbarui `walkthrough.md` di folder artifacts/brain session.

### 2.6 Superpowers & Brainstorming Enforcement
- **Wajib Menggunakan Skill `using-superpowers` & `brainstorming`**: Pada setiap pembahasan fitur, arsitektur, bugfix, atau perubahan desain, agent **WAJIB** secara eksplisit mengaktifkan skill `using-superpowers` dan `brainstorming`.

---

## 3. Workflow & Technical Constraints

1. **Inference Only Scope**: Repositori ini difokuskan khusus untuk inferensi dan antarmuka pengguna.
2. **Audio Specifications**:
   - Sample Rate: `16,000 Hz`
   - Channels: `Mono`
   - Max Duration for SER: `4.0 detik` (sesuai WavLM v7 model training `ser-augmemted.ipynb`)
   - STT Input: Full waveform (tanpa dipotong 4 detik)
3. **Execution Safety & Non-Destructive Rule**:
   - **PENTING**: Dilarang asal menghapus fungsi, route, atau payload saat terjadi error. Prioritaskan investigasi root cause dan penyesuaian migrasi/tipe data.
   - Selalu jalankan verifikasi sintaks/import (`python -c "import model..."`) sebelum mengklaim pekerjaan selesai.

---

## 4. Konvensi Commit & Branch (Conventional Commits v1.0.0)

Semua commit git **wajib mematuhi standar Conventional Commits** dengan struktur:

```
<type>(<scope>): <subject>

<body — opsional, wajib untuk commit yang menyentuh logic bisnis/model>

Refs: <nomor TDD / notebook v7 / issue>  ← wajib untuk commit yang menyentuh model/pipeline
```

### Tipe Commit (`<type>`):
- `feat`: Penambahan fitur baru (misal: integrasi STT Whisper, audio recorder UI).
- `fix`: Perbaikan bug/error (misal: perbaikan `ImportError`, `attention_mask`).
- `refactor`: Perubahan kode tanpa mengubah perilaku fitur (misal: penyelarasan GELU).
- `docs`: Pembaruan dokumentasi (`AGENTS.md`, `README.md`, `walkthrough.md`, `tdd_changes_tracker.md`).
- `style`: Penyesuaian formatting, linting, tanpa perubahan logika bisnis.
- `test`: Penambahan atau perbaikan unit test.
- `chore`: Perubahan konfigurasi build, `.gitignore`, dependensi `requirements.txt`.

### Scope Taxonomy (`<scope>`):
| Scope | Domain Deskripsi |
| :--- | :--- |
| `model` | Arsitektur `WavLMSERModel`, attention pooling, loading checkpoint |
| `pipeline` | Audio preprocessing, resampling, 4.0s pad/crop, STT Whisper pipeline |
| `ui` | Tampilan Streamlit / Next.js (mobile-first components) |
| `docs` | AGENTS.md, walkthrough, tdd_changes_tracker |
| `chore` | .gitignore, requirements.txt, setup environment |

### Aturan Eksekusi Commit:
1. **Imperative Mood**: Gunakan kata kerja imperatif pada `<subject>` (`fix(pipeline): align classifier activation with GELU`, bukan `fixed`).
2. **Singkat & Jelas**: Subject max 50-72 karakter, tunduk pada aturan Nol AI Slop.
3. **Tanpa Garbage File**: Pastikan `.venv`, `__pycache__`, dan model weights `.pt` tidak masuk staging `git add`.
4. **Footer `Refs:`**: Wajib untuk commit yang menyentuh arsitektur `model.py` atau `utils.py`.

---

## 5. Quick Commands

```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run Streamlit application
python -m streamlit run app.py
```
