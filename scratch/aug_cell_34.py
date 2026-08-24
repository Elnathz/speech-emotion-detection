# [5.1] Fungsi Augmentasi & Eksekusi Khusus Data Train Indonesia
import librosa
import soundfile as sf
import pandas as pd
import os, glob
from tqdm import tqdm

def load_for_aug(path, sr=SAMPLE_RATE):
    try:
        y, _ = librosa.load(path, sr=sr, mono=True)
        y = np.nan_to_num(y.astype(np.float32))
        peak = np.max(np.abs(y))
        if peak > 1e-5: y = y / peak
        return y
    except: return None

def augment_offline(y, sr, mode):
    if mode == 'pitch_up2':     return librosa.effects.pitch_shift(y, sr=sr, n_steps=2)
    elif mode == 'pitch_down2': return librosa.effects.pitch_shift(y, sr=sr, n_steps=-2)
    elif mode == 'stretch_slow':
        y_aug = librosa.effects.time_stretch(y, rate=0.85)
        if len(y_aug)>len(y): y_aug=y_aug[:len(y)]
        elif len(y_aug)<len(y): y_aug=np.pad(y_aug,(0,len(y)-len(y_aug)))
        return y_aug
    elif mode == 'stretch_fast':
        y_aug = librosa.effects.time_stretch(y, rate=1.15)
        if len(y_aug)>len(y): y_aug=y_aug[:len(y)]
        elif len(y_aug)<len(y): y_aug=np.pad(y_aug,(0,len(y)-len(y_aug)))
        return y_aug
    elif mode == 'noise_light':
        return y + 0.004 * np.random.randn(len(y)).astype(np.float32)
    return y

def run_augmentasi_offline(df_src, sumber_tag, aug_dir, aug_modes):
    rows_aug = []
    df_target = df_src[df_src['sumber']==sumber_tag].copy()
    print(f'   Augmenting Train {sumber_tag}: {len(df_target)} file x {len(aug_modes)} mode = {len(df_target)*len(aug_modes)} file baru')
    for _, row in tqdm(df_target.iterrows(), total=len(df_target), desc=f'Aug {sumber_tag}'):
        y = load_for_aug(row['path'])
        if y is None or len(y) < MIN_SAMPLES: continue
        for mode in aug_modes:
            try:
                y_aug = np.clip(augment_offline(y, SAMPLE_RATE, mode), -1.0, 1.0).astype(np.float32)
                fname = f"aug_{mode}_{os.path.splitext(os.path.basename(row['path']))[0]}.wav"
                out_path = os.path.join(aug_dir, sumber_tag, fname)
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                sf.write(out_path, y_aug, SAMPLE_RATE)
                rows_aug.append({
                    'path': out_path, 'emosi': row['emosi'], 'label': row['label'],
                    'sumber': f'{sumber_tag}_aug', 'bahasa': row['bahasa'], 'file': fname,
                    'bobot': BOBOT_SUMBER.get(f'{sumber_tag}_aug', 2.0)
                })
            except: pass
    return pd.DataFrame(rows_aug)

df_aug_parts = []
if DO_AUGMENT:
    print('[AUGMENT] Memulai augmentasi offline HANYA pada data latih Indonesia...')
    for tag in ['indowavesentiment', 'eseravd']:
        if tag in df_train_orig['sumber'].values:
            tmp = run_augmentasi_offline(df_train_orig, tag, AUG_DIR, AUG_MODES)
            if len(tmp): df_aug_parts.append(tmp)
    print('[OK] Augmentasi data latih selesai.')

if df_aug_parts:
    df_train_augmented = pd.concat(df_aug_parts, ignore_index=True)
    df_train = pd.concat([df_train_orig, df_train_augmented], ignore_index=True).reset_index(drop=True)
else:
    df_train = df_train_orig.copy()

# Finalize split dataframes & Export Metadata
df_train['split'] = 'train'
df_val['split'] = 'val'
df_test['split'] = 'test'
df_split = pd.concat([df_train, df_val, df_test], ignore_index=True)
df_split.to_csv(SPLIT_PATH, index=False)

print('='*70)
print('  [FINAL SPLIT SUMMARY - NO LEAKAGE GUARANTEED]')
print('='*70)
print(f'  Train Final    : {len(df_train)} file (Termasuk {len(df_train_augmented) if df_aug_parts else 0} file aug)')
print(f'  Validation     : {len(df_val)} file (100% Murni Asli)')
print(f'  Test           : {len(df_test)} file (100% Murni Asli)')
print('='*70)
