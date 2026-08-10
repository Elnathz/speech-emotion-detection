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
