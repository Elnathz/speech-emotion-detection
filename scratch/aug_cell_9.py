# ── PATH ──────────────────────────────────────────────────────────────
BASE_DIR      = '/kaggle/working' if IS_KAGGLE else os.getcwd()
DATA_DIR      = os.path.join(BASE_DIR, 'data')
RAW_DIR       = os.path.join(DATA_DIR, 'raw')
AUG_DIR       = os.path.join(DATA_DIR, 'augmented')
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')
MODEL_DIR     = os.path.join(BASE_DIR, 'models')
LOG_DIR       = os.path.join(BASE_DIR, 'logs')
for d in [RAW_DIR, AUG_DIR, PROCESSED_DIR, MODEL_DIR, LOG_DIR]:
    os.makedirs(d, exist_ok=True)
# ── VERIFIKASI & PATH DATASET KAGGLE / LOKAL ──────────────────────────
DATASET_CANDIDATES = {
    'IndoWaveSentiment': [
        '/kaggle/input/datasets/elnathh/indowavesentiment/IndoWaveSentiment Indonesian Audio Dataset for Emotion Classification/IndoWaveSentiment',
        '/kaggle/input/indo-wave/IndoWaveSentiment',
        os.path.join(RAW_DIR, 'IndoWaveSentiment'),
        os.path.join(BASE_DIR, 'pipeline', 'Dataset', 'IndoWaveSentiment'),
    ],
    'RAVDESS': [
        '/kaggle/input/datasets/uwrfkaggler/ravdess-emotional-speech-audio',
        '/kaggle/input/ravdess-emotional-speech-audio',
        os.path.join(RAW_DIR, 'ravdess'),
    ],
    'EmoDB': [
        '/kaggle/input/datasets/piyushagni5/berlin-database-of-emotional-speech-emodb/wav',
        '/kaggle/input/berlin-database-of-emotional-speech-emodb/wav',
        os.path.join(RAW_DIR, 'emodb'),
    ],
    'CREMA-D': [
        '/kaggle/input/datasets/ejlok1/cremad/AudioWAV',
        '/kaggle/input/cremad/AudioWAV',
        os.path.join(RAW_DIR, 'cremad'),
    ],
    'E-SERAVD': [
        '/kaggle/input/datasets/ahmadnafibudianto/e-seravd-speech-emotion-recognition-av-dataset/E-SERAVD 1.1/E-SERAVD/02_Audio-Only',
        '/kaggle/input/datasets/ahmadnafibudianto/e-seravd-speech-emotion-recognition-av-dataset/E-SERAVD/E-SERAVD/02_Audio-Only',
        '/kaggle/input/datasets/ahmadnafibudianto/e-seravd-speech-emotion-recognition-av-dataset/E-SERAVD 1.2/E-SERAVD 1.2/E-SERAVD/02_Audio-Only',
        os.path.join(RAW_DIR, 'eseravd'),
    ]
}
DATASET_PATHS = {}
found_count = 0
print('[CHECK] Memeriksa keberadaan dataset...')
for ds_name, candidates in DATASET_CANDIDATES.items():
    detected_path = next((p for p in candidates if os.path.isdir(p)), None)
    if detected_path:
        DATASET_PATHS[ds_name] = detected_path
        found_count += 1
        print(f'  [OK] {ds_name:<18}: Ditemukan -> {detected_path}')
    else:
        DATASET_PATHS[ds_name] = None
        print(f'  [NOT FOUND] {ds_name:<18}: TIDAK DITEMUKAN')
# Mapping ke variabel legacy agar cell berikutnya tetap kompatibel
KAGGLE_INDOWAVE = DATASET_PATHS['IndoWaveSentiment'] or '/kaggle/input/indowave-placeholder'
KAGGLE_RAVDESS  = DATASET_PATHS['RAVDESS'] or '/kaggle/input/ravdess-placeholder'
KAGGLE_EMODB    = DATASET_PATHS['EmoDB'] or '/kaggle/input/emodb-placeholder'
KAGGLE_CREMAD   = DATASET_PATHS['CREMA-D'] or '/kaggle/input/cremad-placeholder'
KAGGLE_ESERAVD  = DATASET_PATHS['E-SERAVD'] or '/kaggle/input/e-seravd-placeholder'
if found_count == 0:
    print('\n[ERROR] ERROR KRITIS: Tidak ada satu pun dataset yang terdeteksi di sistem!')
    print('   Sistem menghentikan eksekusi cell untuk mencegah proses training sia-sia.')
    sys.exit('Eksekusi dihentikan: Dataset tidak ditemukan.')
print(f'\n[NOTE] Total dataset terdeteksi: {found_count}/{len(DATASET_CANDIDATES)}')
# ── MODEL ─────────────────────────────────────────────────────────────
PRETRAINED_MODEL = 'microsoft/wavlm-base-plus'   # T4/P100 tidak cukup utk wavlm-large
LOCAL_PRETRAINED = None
MODEL_SOURCE = LOCAL_PRETRAINED if LOCAL_PRETRAINED and os.path.isdir(LOCAL_PRETRAINED) else PRETRAINED_MODEL
# ── AUDIO ─────────────────────────────────────────────────────────────
SAMPLE_RATE = 16000
MAX_SECONDS = 4.0          # ↓ dari 6.0 - emosi terkonsentrasi di awal ucapan
MIN_SECONDS = 0.35
MIN_DURATION_SEC = MIN_SECONDS
MAX_DURATION_SEC = MAX_SECONDS
MIN_SNR_DB = 3.0
HARD_NOISE_CONF_THRESH = 0.85
FOCAL_GAMMA = 2.0
MAX_SAMPLES = int(SAMPLE_RATE * MAX_SECONDS)
MIN_SAMPLES = int(SAMPLE_RATE * MIN_SECONDS)
AUDIO_EXTS  = ('.wav','.mp3','.flac','.ogg','.m4a','.mp4')
# ── LABEL ─────────────────────────────────────────────────────────────
EMOSI_LIST  = ['netral','senang','sedih','marah','takut','jijik']
LABEL2IDX   = {e:i for i,e in enumerate(EMOSI_LIST)}
IDX2LABEL   = {i:e for e,i in LABEL2IDX.items()}
NUM_CLASSES = len(EMOSI_LIST)
EMOJI_MAP   = {'netral':'😐','senang':'😊','sedih':'😢','marah':'😡','takut':'😨','jijik':'🤢'}
# ── BOBOT SUMBER DASAR ────────────────────────────────────────────────
BOBOT_SUMBER = {
    'indowavesentiment'    : 3.0,
    'indowavesentiment_aug': 2.0,
    'eseravd'              : 3.0,
    'eseravd_aug'          : 2.0,
    'ravdess'              : 0.7,
    'emodb'                : 0.7,
    'cremad'                : 0.7,   # dasar - akan di-modifikasi per-kelas di bawah
}
# ── BOBOT CREMA-D PER-KELAS (dari riset CHUCKLE 2024, audio-only agreement) ──
# Agreement rendah → bobot rendah (label kemungkinan noise)
CREMAD_AGREEMENT = {
    'netral' : 0.957,   # 95.7% agreement → bobot tinggi, dipertahankan
    'marah'  : 0.606,   # 60.6%
    'jijik'  : 0.300,   # 30.0%
    'takut'  : 0.320,   # 32.0%
    'senang' : 0.260,   # 26.0%
    'sedih'  : 0.164,   # 16.4% ← hampir random, downweight ekstrem
}
# Skala bobot: clip minimum 0.10 supaya tidak hilang total (masih ada sinyal)
CREMAD_BOBOT_PER_KELAS = {e: max(0.35, agree * 1.0) for e, agree in CREMAD_AGREEMENT.items()}
print('Bobot CREMA-D per kelas (dari agreement rate):')
for e, w in CREMAD_BOBOT_PER_KELAS.items():
    print(f'   {EMOJI_MAP[e]} {e:<8}: {w:.3f}')
# ── SPLIT ─────────────────────────────────────────────────────────────
VAL_SPLIT  = 0.15
TEST_SPLIT = 0.15
SEED       = 42
# ── AUGMENTASI OFFLINE ────────────────────────────────────────────────
DO_AUGMENT = True
AUG_MODES  = ['pitch_up2','pitch_down2','stretch_slow','stretch_fast','noise_light']
# pitch_up1 dihapus - terlalu mirip pitch_up2, mengurangi diversity riil
# ── HYPERPARAMETER v7 (dikoreksi utk base-plus) ───────────────────────
BATCH_SIZE        = 6
GRAD_ACCUM_STEPS  = 2
EPOCHS            = 22
FREEZE_EPOCHS     = 2
UNFREEZE_LAST_N   = 6          # ← balik ke gradual (v5 style), bukan full unfreeze
BACKBONE_LR       = 1e-5       # ← naik dikit dari v6 (8e-6), krn cuma 6 layer
HEAD_LR           = 3e-4
WEIGHT_DECAY      = 1e-2
WARMUP_RATIO      = 0.10
EARLY_STOP        = 6
MIN_DELTA         = 0.001
GRAD_CLIP         = 1.0
DROPOUT           = 0.30       # ↓ dari 0.50
LABEL_SMOOTHING   = 0.10       # ↓ dari 0.15
USE_MIXUP         = True
MIXUP_ALPHA       = 0.2        # ↓ dari 0.3
MIXUP_PROB        = 0.25       # ↓ dari implisit 0.5
USE_SPECAUGMENT   = True
SPEC_TIME_MASK_P  = 0.3        # ↓ dari 0.5
SPEC_TIME_MAX     = int(0.08 * MAX_SAMPLES)   # ↓ dari 0.15
USE_AMP           = True
USE_GRAD_CKPT     = True
NUM_WORKERS       = 2 if IS_KAGGLE else 0
# ── LABEL NOISE DETECTION (otomatis setelah training awal) ────────────
DO_NOISE_DETECTION = True
NOISE_CONF_THRESHOLD = 0.40    # confidence di bawah ini + salah prediksi = kandidat noise
NOISE_DOWNWEIGHT = 0.3         # bobot file yang dicurigai noise
BEST_MODEL_PATH      = os.path.join(MODEL_DIR, 'ser_wavlm_v7_best.pt')
BEST_MODEL_PATH_STG2 = os.path.join(MODEL_DIR, 'ser_wavlm_v7_stage2_best.pt')
HISTORY_PATH    = os.path.join(LOG_DIR,   'history_v7.json')
SPLIT_PATH      = os.path.join(DATA_DIR,  'metadata_split_v7.csv')
print(f'\n[OK] Konfigurasi v7 siap')
print(f'   Model         : {MODEL_SOURCE}')
print(f'   Audio durasi  : {MAX_SECONDS}s (dipotong dari 6.0s)')
print(f'   Dropout       : {DROPOUT}')
print(f'   Unfreeze      : {UNFREEZE_LAST_N} layer (gradual)')
print(f'   Mixup         : prob={MIXUP_PROB}, alpha={MIXUP_ALPHA}')
print(f'   SpecAugment   : prob={SPEC_TIME_MASK_P}, max_dur=8%')
print(f'   Label smooth  : {LABEL_SMOOTHING}')
print(f'   Noise detect  : {DO_NOISE_DETECTION}')
print(f'   Device        : {device}')
# ── CANDIDATE PATH CHECKPOINT V7 (Kaggle Input / Local) ─────────────────
V7_CHECKPOINT_CANDIDATES = [
    "/kaggle/input/datasets/elnathh/ser-wavlm-v7-checkpoint/ser_wavlm_v7_best.pt",
    "/kaggle/input/ser-wavlm-v7-best/ser_wavlm_v7_best.pt",
    "/kaggle/input/ser-wavlm-v7/ser_wavlm_v7_best.pt",
    os.path.join(MODEL_DIR, "ser_wavlm_v7_best.pt"),
]
INIT_CHECKPOINT_PATH = next((p for p in V7_CHECKPOINT_CANDIDATES if os.path.isfile(p)), None)
if INIT_CHECKPOINT_PATH:
    print(f"[CHECK] Detected v7 pre-trained checkpoint at: {INIT_CHECKPOINT_PATH}")
else:
    print("[NOTE] No existing v7 checkpoint found in Kaggle input. Will train from base weights.")
