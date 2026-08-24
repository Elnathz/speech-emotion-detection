import json

notebook_path = '../pipeline/ver2-ser-pipeline.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

found_aug = False
found_noise = False

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell.get('source', []))
        if 'def run_augmentasi_offline' in source:
            found_aug = True
            if '[MODIFIKASI]' not in source:
                cell['source'].append('\n# [MODIFIKASI] Oversampling ekstrim untuk IndoWaveSentiment\n')
                cell['source'].append('indo_mask = df_train[\'sumber\'].str.contains(\'indowavesentiment\')\n')
                cell['source'].append('if indo_mask.sum() > 0:\n')
                cell['source'].append('    df_indo = df_train[indo_mask]\n')
                cell['source'].append('    print(f\'[OVERSAMPLING] Menggandakan {len(df_indo)} sampel IndoWaveSentiment sebanyak 4x...\')\n')
                cell['source'].append('    df_train = pd.concat([df_train] + [df_indo]*4, ignore_index=True).sample(frac=1, random_state=SEED).reset_index(drop=True)\n')
                
                cell['source'].append('\n# [MODIFIKASI] Augmentasi khusus kelas lemah pada CREMA-D (sedih, senang, takut, jijik)\n')
                cell['source'].append('if \'cremad\' in df_train_orig[\'sumber\'].values:\n')
                cell['source'].append('    df_cremad_weak = df_train_orig[(df_train_orig[\'sumber\'] == \'cremad\') & (df_train_orig[\'label\'].apply(lambda x: IDX2LABEL[x] if isinstance(x, int) else x).isin([\'sedih\', \'senang\', \'takut\', \'jijik\']))].copy()\n')
                cell['source'].append('    if len(df_cremad_weak) > 0:\n')
                cell['source'].append('        df_cremad_weak[\'sumber\'] = \'cremad_weak\'\n')
                cell['source'].append('        tmp = run_augmentasi_offline(df_cremad_weak, \'cremad_weak\', AUG_DIR, [\'pitch_up2\', \'pitch_down2\', \'stretch_slow\'])\n')
                cell['source'].append('        if len(tmp):\n')
                cell['source'].append('            tmp[\'sumber\'] = \'cremad\'\n')
                cell['source'].append('            df_train = pd.concat([df_train, tmp], ignore_index=True).reset_index(drop=True)\n')
                
        if 'hard_noisy_paths = set(noise_candidates[' in source:
            found_noise = True
            if 'label_asli' not in source:
                new_source = source.replace(
                    "(noise_candidates['sumber'] == 'cremad')\n    ]['path'].values)",
                    "(noise_candidates['sumber'] == 'cremad') &\n        (~noise_candidates['label_asli'].isin(['sedih', 'senang', 'takut', 'jijik']))\n    ]['path'].values)"
                )
                cell['source'] = [line + '\n' for line in new_source.split('\n')]
                cell['source'] = [l.replace('\n\n', '\n') for l in cell['source']]

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Modifikasi selesai. Augmentasi: {found_aug}, Noise: {found_noise}")
