''' created by jji on 2021_9_10
iterating a directory containing docx files and converting every docx file into a fasta file.
'''

import os
from docx import Document

def parse_docx(file_docx):
    document = Document(file_docx)
    content_text = ''
    for p in document.paragraphs:
        content_text += p.text

    content_text = content_text.replace('*', '')
    content_text = content_text.replace('_', '')
    content_text = content_text.replace('-', '')

    return content_text



if __name__ == '__main__':

    DIR_SOURCE = os.path.join(os.path.abspath('.'), 'src_docx')
    DIR_DEST = os.path.join(os.path.abspath('.'), 'dest_fasta')
    MAX_LENGTH = 1500

    for root, dirs, files in os.walk(DIR_SOURCE):
        for file in files:
            full_filename = os.path.join(root, file)
            _, filename = os.path.split(full_filename)
            file_base, file_ext = os.path.splitext(filename)
            if file_ext.lower() not in ['.docx']:
                continue

            seq_text = parse_docx(full_filename)
            if len(seq_text) > MAX_LENGTH:
                print(f'seq is too long:{len(seq_text)}, {full_filename}')
                continue

            file_base = file_base.replace(' ', '')
            filename_dest = os.path.join(DIR_DEST, f'{file_base}.fasta')
            with open(filename_dest, 'w+') as f:
                f.write(f'>{file_base}| \n{seq_text}')
            print(f'seq_len:{len(seq_text)}, {filename_dest}')

    print('OK')