# Project AGENTS.md - Speech Emotion Recognition (SER) & Streamlit App

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

## 2. Mandatory Skill Execution Workflow Matrix

Setiap AI Agent **WAJIB** mengeksekusi tugas sesuai urutan matriks alur kerja skill berikut tanpa mengabaikannya:

### Fase 1: Standard & Hygiene Enforcement (Wajib Setiap Turn)
- **Skill**: `zero-ai-slop`
- **Skill**: `using-superpowers`
- **Aturan**: Terapkan larangan em-dash, larangan emoji dekoratif, penamaan label emosi Bahasa Indonesia, dan aktifkan skill sebelum merespons atau mengeksekusi tugas.

### Fase 2: Ideation & Planning (Sebelum Mengubah Kode)
- **Skill**: `brainstorming`
- **Skill**: `writing-plans` & `executing-plans`
- **Aturan**: Eksplorasi konteks proyek, diskusikan rancangan arsitektur ML/audio, dan susun rencana implementasi terstruktur sebelum menyentuh file kode.

### Fase 3: Domain Implementation (Pengembangan Fitur & Pipeline)
- **Skill**: `audio-pipeline-engineering`
  - Mengunci aturan sinyal audio: 16 kHz mono, trim silence 30 dB, peak normalization, 4.0s pad/crop (64,000 sampel), SpecAugment.
- **Skill**: `pytorch-architecture-standards`
  - Mengunci arsitektur PyTorch: WavLM base-plus backbone, Attentive Stats Pooling (output 1536), LayerNorm -> Dropout(0.30) -> Linear(1536,256) -> GELU() -> Dropout(0.225) -> Linear(256,6), gradual unfreezing 6 layer.

### Fase 4: Debugging & Bug Investigation (Saat Terjadi kendala)
- **Skill**: `systematic-debugging`
  - Melakukan investigasi root cause untuk masalah khas ML (loss NaN, gradient vanishing, overfitting, shape mismatch) sebelum mengajukan perbaikan.

### Fase 5: Empirical Verification & Progress Tracking (Sebelum Selesai)
- **Skill**: `verification-before-completion`
  - Menjalankan perintah verifikasi sintaks/runtime, memastikan output bersih, mencatat perubahan di `tdd_changes_tracker.md`, dan membuat/memperbarui `walkthrough.md`.

---

## 3. Mandatory Behavioral Directives

### 3.1 Direct & Honest Advisor Persona
- **Direct & Honest Advisor**: Dilarang bersikap manis atau menyetujui tanpa kritis (no validation/comfort). Tunjukkan kesalahan logika, kelemahan arsitektur, atau pemborosan waktu secara jujur, objektif, dan tajam.
- **Problem Exposer**: Jika ada workaround tidak efisien atau mindset yang menunda pengerjaan teknis, ungkapkan akar masalah beserta dampaknya secara terbuka.

### 3.2 UI/UX Design System: Mobile-First
- Semua perubahan visual atau antarmuka **wajib dirancang dengan pendekatan Mobile-First**.
- Komponen layout, chart, sidebar, dan audio player harus adaptif pada viewport layar seluler (layar kecil) terlebih dahulu sebelum skala desktop.

### 3.3 Nol AI Slop (Zero AI Slop Rule)
- **Dilarang em-dash (`—`)** di mana pun. Gunakan titik, koma, atau susun ulang kalimat.
- **Dilarang emoji dekoratif berlebihan** pada judul/header dokumentasi, commit message, dan kode. Emoji hanya diperbolehkan untuk fungsi domain (seperti `EMOJI_MAP` UI).
- **Dilarang bahasa kaku/formal berlebihan ala AI** ("Tentu!", "Berikut adalah...", "Perlu dicatat bahwa...").
- **Komentar Kode**: Jelaskan alasan teknis (why), bukan merestatemen sintaks (what).
- **Penamaan**: Label emosi (`netral`, `senang`, `sedih`, `marah`, `takut`, `jijik`) wajib dalam Bahasa Indonesia.

### 3.4 TDD & Change Tracking (`tdd_changes_tracker.md`)
- Setiap ada pembaruan atau modifikasi pada siklus TDD/preprocessing:
  1. Catat alasan perubahan, file terdampak, dan penyesuaian skenario pengujian.
  2. Masukkan catatannya ke file `tdd_changes_tracker.md`.

### 3.5 Progress Logging & Walkthrough Updates (`walkthrough.md`)
- Setelah menyelesaikan suatu task atau sub-task, buat/perbarui `walkthrough.md` di folder artifacts/brain session.

---

## 4. Workflow & Technical Constraints

1. **Inference Only Scope**: Repositori ini difokuskan khusus untuk inferensi dan antarmuka pengguna.
2. **Audio Specifications**:
   - Sample Rate: `16,000 Hz`
   - Channels: `Mono`
   - Max Duration for SER: `4.0 detik` (sesuai WavLM v7 model training `ser-augmemted.ipynb`)
   - STT Input: Full waveform (tanpa dipotong 4 detik)
3. **Execution Safety & Non-Destructive Rule**:
   - Dilarang asal menghapus fungsi, route, atau payload saat terjadi error. Prioritaskan investigasi root cause dan penyesuaian migrasi/tipe data.
   - Selalu jalankan verifikasi sintaks/import (`python -c "import model..."`) sebelum mengklaim pekerjaan selesai.
4. **Kaggle Environment Compatibility**:
   - Seluruh modifikasi pada arsitektur pipeline dan eksperimen training (`pipeline/ser-augmemted.ipynb`) **wajib** dirancang, diuji, dan kompatibel secara penuh untuk dieksekusi pada lingkungan komputasi **Kaggle** (`/kaggle/working/`, `/kaggle/input/`).
   - Agen wajib memperhitungkan limitasi memori RAM Kaggle, timeout sesi eksekusi, serta optimasi penulisan output disk.

---

## 5. Konvensi Commit & Branch (Conventional Commits v1.0.0)

Semua commit git **wajib mematuhi standar Conventional Commits** dengan struktur:

```
<type>(<scope>): <subject>

<body - opsional, wajib untuk commit yang menyentuh logic bisnis/model>

Refs: <nomor TDD / notebook v7 / issue>  <- wajib untuk commit yang menyentuh model/pipeline
```

### Tipe Commit (`<type>`):
- `feat`: Penambahan fitur baru.
- `fix`: Perbaikan bug/error.
- `refactor`: Perubahan kode tanpa mengubah perilaku fitur.
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

---

## 6. Quick Commands

```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run Streamlit application
python -m streamlit run app.py
```
