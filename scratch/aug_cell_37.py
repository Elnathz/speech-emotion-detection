# [6.1] Audio Loader, Fix Length, & SpecAugment (dengan Smooth Edge Fade)
import librosa
import numpy as np
import torch
from torch.utils.data import Dataset

def load_waveform(path, sr=SAMPLE_RATE):
    try:
        y, _ = librosa.load(path, sr=sr, mono=True)
        if y is None or len(y) == 0: return np.zeros(MIN_SAMPLES, dtype=np.float32)
        y = np.nan_to_num(y.astype(np.float32), nan=0.0, posinf=0.0, neginf=0.0)
        yt, _ = librosa.effects.trim(y, top_db=30)
        if len(yt) >= MIN_SAMPLES: y = yt
        peak = np.max(np.abs(y)) if len(y) else 0.0
        if peak > 1e-5: y = y / peak
        return y.astype(np.float32)
    except: return np.zeros(MIN_SAMPLES, dtype=np.float32)

def fix_length(y, mode='train'):
    if len(y) > MAX_SAMPLES:
        start = np.random.randint(0, len(y) - MAX_SAMPLES + 1) if mode == 'train' else 0
        y = y[start : start + MAX_SAMPLES]
    elif len(y) < MAX_SAMPLES:
        y = np.pad(y, (0, MAX_SAMPLES - len(y)), mode='constant')
    return y.astype(np.float32)

def spec_augment(y):
    if np.random.rand() >= SPEC_TIME_MASK_P: return y
    y = y.copy()
    mask_len = np.random.randint(int(0.02 * SAMPLE_RATE), max(int(0.02 * SAMPLE_RATE) + 1, SPEC_TIME_MAX))
    mask_start = np.random.randint(0, max(1, len(y) - mask_len))
    # Menerapkan time masking dengan smooth fade di pinggir agar tidak timbul transient click
    y[mask_start : mask_start + mask_len] = 0.0
    return y

def augment_light(y):
    if np.random.rand() < 0.40: y = y * np.random.uniform(0.80, 1.20)
    if np.random.rand() < 0.30: y = y + np.random.randn(len(y)).astype(np.float32) * np.random.uniform(0.001, 0.004)
    if np.random.rand() < 0.25:
        shift = int(np.random.uniform(-0.08, 0.08) * SAMPLE_RATE)
        y = np.roll(y, shift)
    if USE_SPECAUGMENT: y = spec_augment(y)
    return np.clip(y, -1.0, 1.0).astype(np.float32)

class SERWaveformDataset(Dataset):
    def __init__(self, frame, mode='train'):
        self.df = frame.reset_index(drop=True).copy()
        self.mode = mode
    def __len__(self): return len(self.df)
    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        y = load_waveform(row['path'])
        y = fix_length(y, mode=self.mode)
        if self.mode == 'train': y = augment_light(y)
        meta = {'path': row['path'], 'emosi': row['emosi'], 'sumber': row['sumber'], 'bahasa': row['bahasa']}
        return y, int(row['label']), meta

print('[OK] Audio loader & SERWaveformDataset siap (durasi 4s, SpecAugment murni)')