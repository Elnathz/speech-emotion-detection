import json
import os

with open('../pipeline/ver2-ser-pipeline.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

with open('nb_out.txt', 'w', encoding='utf-8') as out:
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            source = ''.join(cell.get('source', []))
            if 'HARD_NOISE_CONF_THRESH' in source or 'class SERDataset' in source or 'STAGE 2' in source or 'transform' in source.lower() or 'train_df' in source:
                out.write(f'\n--- Cell {i} (code) ---\n')
                out.write(source)
                out.write('\n')
