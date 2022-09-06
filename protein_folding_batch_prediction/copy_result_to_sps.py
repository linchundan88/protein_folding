''' created by jji on 2021_9_10
iterating a directory containing docx files and converting every docx file into a fasta file.
'''

import os
from shutil import copyfile

DIR_SOURCE = '/protein_folding/results/alphafold/2022-06-30-0-clp'
#DIR_DEST = '/run/user/1000/gvfs/smb-share:server=10.12.193.4,share=生物信息/geneai/predicted/alphafold'
DIR_DEST = '/protein_folding/geneai/alphafold/2022-06-30-0-clp'

if os.path.exists(DIR_DEST) == False:
    os.mkdir(DIR_DEST)

for root, dirs, files in os.walk(DIR_SOURCE):
    for file in files:

        full_filename = os.path.join(root, file)
        _, filename = os.path.split(full_filename)
        file_base, file_ext = os.path.splitext(filename)
        if file_ext.lower() not in ['.pdb', '.json']:
            continue

        if file_base.lower() not in ['ranked_0', 'ranked_1', 'ranked_2', 'ranked_3', 'ranked_4', 'ranking_debug']:
            continue

        sq_dir = root.split('/')[-1]
        sps_dir = DIR_DEST + '/' + sq_dir
        if os.path.exists(sps_dir) == False:
            os.mkdir(sps_dir)

        if os.path.exists(sps_dir + '/' + file) == False:
            copyfile(root + '/' + file, sps_dir + '/' + file)

        print(root, sq_dir, file)


