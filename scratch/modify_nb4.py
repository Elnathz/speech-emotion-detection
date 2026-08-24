import json

notebook_path = '../pipeline/ver2-ser-pipeline.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell.get('source', []))
        
        # 1. Modifikasi Augmentasi Offline & Oversampling
        if 'def run_augmentasi_offline' in source and 'df_train_orig' in source and 'df_aug_parts = []' in source:
            source += "\n# [MODIFIKASI] Oversampling ekstrim untuk IndoWaveSentiment\n"
            source += "indo_mask = df_train['sumber'].str.contains('indowavesentiment')\n"
            source += "if indo_mask.sum() > 0:\n"
            source += "    df_indo = df_train[indo_mask]\n"
            source += "    print(f'[OVERSAMPLING] Menggandakan {len(df_indo)} sampel IndoWaveSentiment sebanyak 4x...')\n"
            source += "    df_train = pd.concat([df_train] + [df_indo]*4, ignore_index=True).sample(frac=1, random_state=SEED).reset_index(drop=True)\n"
            
            source += "\n# [MODIFIKASI] Augmentasi khusus kelas lemah pada CREMA-D (sedih, senang, takut, jijik)\n"
            source += "if 'cremad' in df_train_orig['sumber'].values:\n"
            source += "    df_cremad_weak = df_train_orig[(df_train_orig['sumber'] == 'cremad') & (df_train_orig['label'].apply(lambda x: IDX2LABEL[x] if isinstance(x, int) else x).isin(['sedih', 'senang', 'takut', 'jijik']))].copy()\n"
            source += "    if len(df_cremad_weak) > 0:\n"
            source += "        df_cremad_weak['sumber'] = 'cremad_weak'\n"
            source += "        tmp = run_augmentasi_offline(df_cremad_weak, 'cremad_weak', AUG_DIR, ['pitch_up2', 'pitch_down2', 'stretch_slow'])\n"
            source += "        if len(tmp):\n"
            source += "            tmp['sumber'] = 'cremad'\n"
            source += "            df_train = pd.concat([df_train, tmp], ignore_index=True).reset_index(drop=True)\n"
            
            cell['source'] = [line + '\n' for line in source.split('\n')]
            
        # 2. Modifikasi Noise Filter
        if "hard_noisy_paths = set(noise_candidates[" in source:
            new_source = source.replace(
                "(noise_candidates['sumber'] == 'cremad')",
                "(noise_candidates['sumber'] == 'cremad') &\n        (~noise_candidates['label_asli'].isin(['sedih', 'senang', 'takut', 'jijik']))"
            )
            cell['source'] = [line + '\n' for line in new_source.split('\n')]

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
