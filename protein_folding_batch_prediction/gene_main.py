import os
from docx import Document
from shutil import move, copyfile
from Bio import SeqIO

def move_sq_docx():

    DIR_SOURCE = '/run/user/1000/gvfs/smb-share:server=10.12.192.22,share=geneai/unpredicted'
    DIR_DEST = '/run/user/1000/gvfs/smb-share:server=10.12.192.22,share=geneai/predicted/alphafold'

    for root, dirs, files in os.walk(DIR_SOURCE):
        for file in files:

            # print(file)

            if os.path.exists(DIR_DEST + '\\' + file.replace('.docx','').replace(' ', '')) == True:
                move(root + '\\' + file, DIR_DEST + '\\' + file.replace('.docx','').replace(' ', '') + '\\' + file)
                print(root, file)

            # os.rename(root + '\\' + file, root + '\\' + file + '.docx')

def parse_docx(file_docx):
    document = Document(file_docx)
    content_text = ''
    for p in document.paragraphs:
        content_text += p.text

    content_text = content_text.replace('*', '')
    content_text = content_text.replace('_', '')
    content_text = content_text.replace('-', '')

    return content_text

def count_sq_length():

    DIR_SOURCE = '/run/user/1000/gvfs/smb-share:server=10.12.192.22,share=geneai/unpredicted/先'
    MAX_LENGTH = 1500

    for root, dirs, files in os.walk(DIR_SOURCE):
        for file in files:
            full_filename = os.path.join(root, file)
            _, filename = os.path.split(full_filename)
            file_base, file_ext = os.path.splitext(filename)
            if file_ext.lower() not in ['.docx']:
                continue

            seq_text = parse_docx(full_filename)
            if len(seq_text) <= MAX_LENGTH:
                print(f'seq is too long:{len(seq_text)}, {full_filename}')


if __name__ == '__main__':

    count_sq_length()