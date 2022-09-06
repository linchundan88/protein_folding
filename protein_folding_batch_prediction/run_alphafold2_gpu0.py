''' created by jji on 2021_9_10

I write this script because I do not want to modify run_docker.py too much and do not like linux shell.

run docx_2_fasta.py first to generate fasta files, and then run this file.
execute run_docker.py will activate a docker container and execute the entrypoint /app/run_alphafold.sh,
 and then run_alphafold.sh will call run_alphafold.py

The following parameters are set in run_docker.py
DOWNLOAD_DIR = '/devdata_b/data/Alphafold/dataset'

# Name of the AlphaFold Docker image.
docker_image_name = 'alphafold'

# Path to a directory that will store the results.
output_dir = '/devdata_b/data/Alphafold/outputs_tmp'

# Names of models to use.
model_names = [
    'model_1',
    'model_2',
    'model_3',
    'model_4',
    'model_5',
]

Moreover, I added the following line 'entrypoint='/app/run_alphafold.sh',  #jji add' in container = client.containers.run(
because I will modify predict_structure in run_alphafold.py in order to seperate data processing and models prediction.

change the number of cpus in script "alphafold/data/tools/hhblits.py" n_cpu: int = 4   modified to 8
and "alphafold/data/tools/jackhmmer.py" n_cpu: int = 8    modified to 16


cmd:
python3 /protein_folding/alphafold/docker/run_docker.py --fasta_paths=/protein_folding/dir_fasta/2022-2-5/EPHA2D943N.fasta  --max_template_date=2021-08-14 --preset=full_dbs --use_gpu=True  --gpu_devices=1


originaal docker_name:alphafold,
/app/alphafold/run_alphafold.py
'''

import os
import argparse
import subprocess
import time
from Bio import SeqIO

parser = argparse.ArgumentParser()
parser.add_argument('--use_gpu', default=True)
# in 19 and 26,  /home/ubuntu/protein_folding/alphafold/
parser.add_argument('--dir_alphafold', default='/protein_folding/alphafold/')
parser.add_argument('--dir_fasta', default='/protein_folding/dir_fasta/2022-06-30-0-clp')
parser.add_argument('--gpu_device', default='0')
parser.add_argument('--preset', default='full_dbs') #'reduced_dbs', 'full_dbs', 'casp14'
parser.add_argument('--max_template_date', default='2021-08-14') #2020-05-14
args = parser.parse_args()


list_file_paths = []
for root, dirs, files in os.walk(args.dir_fasta):
    for file in files:
        full_filename = os.path.join(root, file)
        _, filename = os.path.split(full_filename)
        file_base, file_ext = os.path.splitext(filename)
        if file_ext.lower() not in ['.fasta']:
            continue
        list_file_paths.append(full_filename)


for file_paths in list_file_paths:
    file_exe = os.path.join(args.dir_alphafold, 'docker', 'run_docker.py')
    cmd = f'python3 {file_exe} --fasta_paths={file_paths}  --max_template_date={args.max_template_date} --preset={args.preset} --use_gpu={args.use_gpu}  --gpu_devices={args.gpu_device}'
    print(f'Starting execute:{file_paths} at {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')

    fasta_sequences = SeqIO.parse(open(file_paths), 'fasta')
    for fasta in fasta_sequences:
        name, sequence2 = fasta.id, str(fasta.seq)
        print(f'the length of this sequence:{len(str(fasta.seq))}')

    returned_value = subprocess.call(cmd, shell=True)
    print(f'Complete execute:{file_paths} at {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')


print('OK')
