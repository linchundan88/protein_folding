''' created by jji on 2021_9_10
iterating a directory containing docx files and converting every docx file into a fasta file.
'''

import os
from docx import Document
from shutil import move, copyfile, make_archive
import MySQLdb
import uuid
import json



def parse_docx(file_docx):
    document = Document(file_docx)
    content_text = ''
    for p in document.paragraphs:
        content_text += p.text

    content_text = content_text.replace('*', '')
    content_text = content_text.replace('_', '')
    content_text = content_text.replace('-', '')

    return content_text

def move_sq_docx():

    DIR_SOURCE = '\\\\sps\\生物信息\\geneai\\unpredicted'
    DIR_DEST = '\\\\sps\\生物信息\\geneai\\predicted\\alphafold'

    for root, dirs, files in os.walk(DIR_SOURCE):
        for file in files:


            if os.path.exists(DIR_DEST + '\\' + file.replace('.docx','').replace(' ', '')) == True:
                move(root + '\\' + file, DIR_DEST + '\\' + file.replace('.docx','').replace(' ', '') + '\\' + file)
                print(root, file)

            # os.rename(root + '\\' + file, root + '\\' + file + '.docx')

def get_fasta_alphafold():

    fasta_dir = 'D:\\gene_ai\\fasta\\alphafold'
    list_fasta = []
    for root, dirs, files in os.walk(fasta_dir):
        for file in files:
            # print(file)
            list_fasta.append(file)

    # exit(0)

    # DIR_SOURCE = '\\\\sps\\生物信息\\geneai\\unpredicted\\先'
    # DIR_SOURCE = 'D:\gene_ai\先天性白内障\先天性白内障 PHPV 氨基酸序列'
    DIR_SOURCE = 'D:\gene_ai\公为芬\\unpredicted'
    DIR_DEST = 'D:\\gene_ai\\pre_fasta_alphafold'
    # DIR_DEST = 'D:\gene_ai\β2-突变蛋白预测文档\\2021-09-28-1-liu'

    MAX_LENGTH = 2500

    for root, dirs, files in os.walk(DIR_SOURCE):
        for file in files:
            # print(file)
            full_filename = os.path.join(root, file)
            _, filename = os.path.split(full_filename)
            file_base, file_ext = os.path.splitext(filename)
            if file_ext.lower() not in ['.docx']:
                continue

            seq_text = parse_docx(full_filename)
            if len(seq_text) > MAX_LENGTH:
                # print(f'seq is too long:{len(seq_text)}, {full_filename}')
                continue

            file_base = file_base.replace(' ', '')
            filename_dest = os.path.join(DIR_DEST, f'{file_base}.fasta')

            if file_base + '.fasta' in list_fasta:
                continue

            print(f'seq_len:{len(seq_text)}, {filename_dest}, {full_filename}')
            with open(filename_dest, 'w+') as f:
                f.write(f'>{file_base}| \n{seq_text}')


    print('OK')

def get_fasta_rosetta():

    fasta_dir = 'D:\\gene_ai\\fasta\\rosetta'
    list_fasta = []
    for root, dirs, files in os.walk(fasta_dir):
        for file in files:
            # print(file)
            list_fasta.append(file)

    # exit(0)

    # DIR_SOURCE = '\\\\sps\\生物信息\\geneai\\predicted\\alphafold'
    # DIR_SOURCE = 'D:\gene_ai\β2-突变蛋白预测文档\\unpredicted\\2021-09-28'
    DIR_SOURCE = '\\\\sps\\生物信息\\geneai\\unpredicted\\先'
    DIR_DEST = 'D:\\gene_ai\\pre_fasta_rosetta'
    # DIR_DEST = 'D:\gene_ai\β2-突变蛋白预测文档\\2021-09-28-1-liu'
    MAX_LENGTH = 3000

    for root, dirs, files in os.walk(DIR_SOURCE):
        for file in files:
            # print(file)
            full_filename = os.path.join(root, file)
            _, filename = os.path.split(full_filename)
            file_base, file_ext = os.path.splitext(filename)
            if file_ext.lower() not in ['.docx']:
                continue

            seq_text = parse_docx(full_filename)
            if len(seq_text) > MAX_LENGTH:
                # print(f'seq is too long:{len(seq_text)}, {full_filename}')
                continue

            file_base = file_base.replace(' ', '')
            filename_dest = os.path.join(DIR_DEST, f'{file_base}.fasta')

            if file_base + '.fasta' in list_fasta:
                continue

            print(f'seq_len:{len(seq_text)}, {filename_dest}, {full_filename}')
            with open(filename_dest, 'w+') as f:
                f.write(f'>{file_base}| \n{seq_text}')


    print('OK')

def get_result_to_sps():

    DIR_SOURCE = '\\\\10.12.192.22\\geneai\\predicted\\alphafold'
    DIR_DEST = '\\\\sps\\生物信息\\geneai\\predicted\\alphafold'

    for root, dirs, files in os.walk(DIR_SOURCE):
        for file in files:

            full_filename = os.path.join(root, file)
            _, filename = os.path.split(full_filename)
            file_base, file_ext = os.path.splitext(filename)
            if file_ext.lower() not in ['.pdb', '.json']:
                continue

            if file_base.lower() not in ['ranked_0', 'ranked_1','ranked_2','ranked_3','ranked_4','ranking_debug']:
                continue

            sq_dir = root.split('\\')[-1]
            sps_dir = DIR_DEST + '\\' + sq_dir
            if os.path.exists(sps_dir) == False:
                os.mkdir(sps_dir)

            if os.path.exists(sps_dir + '\\' + file) == False:
                copyfile(root + '\\' + file, sps_dir + '\\' + file)

            print(root, sq_dir, file)

def inset_to_mysql():

    mysql_conn = MySQLdb.connect("10.12.192.21", "dlp", "dlp13502965818", "AI", charset='utf8')
    mysql_cursor = mysql_conn.cursor()

    DIR_SOURCE = '\\\\sps\\生物信息\\geneai\\predicted\\alphafold'

    for root, dirs, files in os.walk(DIR_SOURCE):
        for file in files:
            full_filename = os.path.join(root, file)
            _, filename = os.path.split(full_filename)
            file_base, file_ext = os.path.splitext(filename)
            if file_ext.lower() not in ['.docx']:
                continue

            gene = file_base.split(' ')[0]

            dir_name = root.split('\\')[-1]

            wt = 0
            if file_base.lower().find('wt') >= 0:
                wt = 1

            algorithm = root.split('\\')[6]

            seq_text = parse_docx(root + '\\' + file)
            seq_len = len(seq_text)

            print(gene, algorithm, wt, root, dir_name, file, seq_text, seq_len, 1)

            mysql_sql = "select count(*) from tb_gene_detail where dir_name = '" + dir_name + "'"
            mysql_cursor.execute(mysql_sql)
            mysql_count = mysql_cursor.fetchone()

            if mysql_count[0] <= 0:

                mysql_sql = " INSERT INTO tb_gene_detail(gene,algorithm,wt,dir_path,dir_name,docx_name,seq_text,seq_len,status) " \
                            " VALUES ('" + gene +  "','" + algorithm + "'," + str(wt) + ",'" + root.replace('\\', '\\\\') + "','" \
                            + dir_name + "','" + file + "','" + seq_text + "'," + str(seq_len) + ",1)"
                print(mysql_sql)
                mysql_cursor.execute(mysql_sql)
                mysql_conn.commit()

    mysql_cursor.close()
    mysql_conn.close()

def update_rosetta_to_mysql():

    mysql_conn = MySQLdb.connect("10.12.192.21", "dlp", "dlp13502965818", "AI", charset='utf8')
    mysql_cursor = mysql_conn.cursor()

    DIR_SOURCE = '\\\\sps\\生物信息\\geneai\\predicted\\rosetta'

    for root, dirs, files in os.walk(DIR_SOURCE):
        for file in files:
            full_filename = os.path.join(root, file)
            _, filename = os.path.split(full_filename)
            file_base, file_ext = os.path.splitext(filename)
            if file_ext.lower() not in ['.dat']:
                continue

            dir_name = root.split('\\')[-1]

            mysql_sql = " update tb_gene_detail set rosetta = 1 where dir_name = '" + dir_name + "' and rosetta is null"
            print(mysql_sql)
            mysql_cursor.execute(mysql_sql)
            mysql_conn.commit()

    mysql_cursor.close()
    mysql_conn.close()

def get_avg_b_factor(pdb_file):

    with open(pdb_file) as pdbfile:
        total_b_factor_mean = 0
        total_b_factor_rms = 0 #root mean squared
        atom_number = 0
        for line in pdbfile:
            list = line.split()
            # print(list)
            if list[0] == 'ATOM':
                atom_number += 1

                b_factor = float(list[-2])
                total_b_factor_mean +=b_factor
                total_b_factor_rms += b_factor ** 2
                # print(b_factor)
                # print(line)

    return round(total_b_factor_mean / atom_number, 4), round((total_b_factor_rms / atom_number)** 0.5, 4)

def get_rosetta_b_factor_from_dir():

    base_dir = '\\\\sps\生物信息\\geneai\\predicted\\rosetta'

    list_dir = os.listdir(base_dir)

    for r in list_dir:

        str_result = r + '\t'

        is_print = 0

        for i in range(1,6):
            pbd_file = os.path.join(base_dir, r, 'model_' + str(i) + '.crderr.pdb')

            b_factor_mean, b_factor_rms = get_avg_b_factor(pbd_file)

            if str(b_factor_mean) == 'nan':
                str_result = str_result + str(b_factor_mean)  + '\t' + str(b_factor_rms) + '\t'
                is_print = 1

            # print(r, i, b_factor_mean, b_factor_rms)

        if is_print == 1:
            print(str_result)

def move_pbd_to_web():

    mysql_conn = MySQLdb.connect("10.12.192.21", "dlp", "dlp13502965818", "AI", charset='utf8')
    mysql_cursor = mysql_conn.cursor()

    save_dir = '\\\\10.12.246.10\\人工智能\\192_18\\gene_web\\pbd_files'

    mysql_sql = " SELECT * from tb_gene_detail where upload_web = 0 "

    mysql_cursor.execute(mysql_sql)
    mysql_results = mysql_cursor.fetchall()

    for r in mysql_results:

        dir_path = str(r[3])
        dir_name = str(r[4])
        rosetta = str(r[9])
        if rosetta == 'None':
            rosetta = '0'
        str_uuid = str(r[10])
        print(dir_path, dir_name, rosetta,  str_uuid)

        my_save_dir = os.path.join(save_dir, str_uuid)
        if os.path.exists(my_save_dir) == False:
            os.makedirs(my_save_dir)

        my_save_dir = os.path.join(my_save_dir, dir_name)
        if os.path.exists(my_save_dir) == False:
            os.makedirs(my_save_dir)

        root_dir = my_save_dir

        my_save_dir_alphafold = os.path.join(my_save_dir, 'alphafold')
        if os.path.exists(my_save_dir_alphafold) == False:
            os.makedirs(my_save_dir_alphafold)

        for f in ['ranked_0.pdb','ranked_1.pdb','ranked_2.pdb','ranked_3.pdb','ranked_4.pdb','ranking_debug.json']:
            alphafold_file = dir_path + '\\' + f
            if os.path.exists(alphafold_file) == True and os.path.exists(my_save_dir_alphafold + '\\' + f) == False:
                copyfile(alphafold_file, my_save_dir_alphafold + '\\' + f)
        # make_archive(base_name=root_dir + '\\' + dir_name + '_alphafold', format='zip', base_dir='alphafold',
        #              root_dir=root_dir)


        if rosetta == '1':
            my_save_dir_rosetta = os.path.join(my_save_dir, 'rosetta')
            if os.path.exists(my_save_dir_rosetta) == False:
                os.makedirs(my_save_dir_rosetta)

            for f in ['model_1.crderr.pdb', 'model_2.crderr.pdb', 'model_3.crderr.pdb', 'model_4.crderr.pdb', 'model_5.crderr.pdb','modelQ.dat']:
                rosetta_file = dir_path.replace('alphafold','rosetta') + '\\' + f
                if os.path.exists(rosetta_file) == True and os.path.exists(my_save_dir_rosetta + '\\' + f) == False:
                    copyfile(rosetta_file, my_save_dir_rosetta + '\\' + f)

            # make_archive(base_name=root_dir + '\\' + dir_name + '_rosetta', format='zip', base_dir='rosetta',
            #              root_dir=root_dir)


    mysql_cursor.close()
    mysql_conn.close()

def get_plddt_json(base_dir):

    # base_dir = '\\\\sps\生物信息\geneai\predicted\\alphafold\PRPF31R354X'

    json_file = open(os.path.join(base_dir,'ranking_debug.json'),'r')
    data = json.load(json_file)
    json_file.close()

    # print(data['plddts'])
    # print(data['order'])
    #
    # print('0', data['plddts'][data['order'][0]])
    # print('1', data['plddts'][data['order'][1]])
    # print('2', data['plddts'][data['order'][2]])
    # print('3', data['plddts'][data['order'][3]])
    # print('4', data['plddts'][data['order'][4]])

    list_plddt = []
    for i in range(len(data['plddts'])):
        list_plddt.append(str(round(float(data['plddts'][data['order'][i]]),4)))

    return '_'.join(list_plddt)

def set_plddts_to_mysql():

    mysql_conn = MySQLdb.connect("10.12.192.21", "dlp", "dlp13502965818", "AI", charset='utf8')
    mysql_cursor = mysql_conn.cursor()

    mysql_sql = " SELECT * from tb_gene_detail where alphafold_plddt is null "

    mysql_cursor.execute(mysql_sql)
    mysql_results = mysql_cursor.fetchall()

    for r in mysql_results:

        dir_path = str(r[3])
        str_uuid = str(r[10])

        print(dir_path, str_uuid)

        str_plddt = get_plddt_json(dir_path)

        print( str_plddt)

        mysql_sql = " update tb_gene_detail set alphafold_plddt = %s where str_uuid = %s and alphafold_plddt is null "
        # print(mysql_sql)
        mysql_cursor.execute(mysql_sql, (str_plddt, str_uuid))
        mysql_conn.commit()


    mysql_cursor.close()
    mysql_conn.close()

def set_b_factor_to_mysql():

    mysql_conn = MySQLdb.connect("10.12.192.21", "dlp", "dlp13502965818", "AI", charset='utf8')
    mysql_cursor = mysql_conn.cursor()

    mysql_sql = " SELECT * from tb_gene_detail where rosetta_b_factor is null "

    mysql_cursor.execute(mysql_sql)
    mysql_results = mysql_cursor.fetchall()

    for r in mysql_results:

        dir_path = str(r[3]).replace('alphafold','rosetta')
        str_uuid = str(r[10])

        print(dir_path, str_uuid)

        list_b_factor = []
        for i in range(1, 6):
            pdb_file = 'model_' + str(i) + '.crderr.pdb'
            pdb_path = os.path.join(dir_path, pdb_file)
            if os.path.exists(pdb_path) == True:
                aa, _ = get_avg_b_factor(pdb_path)
                list_b_factor.append(str(aa))

        str_b_factor = '_'.join(list_b_factor)
        print(str_b_factor)


        # str_plddt = get_plddt_json(dir_path)
        #
        # print( str_plddt)

        mysql_sql = " update tb_gene_detail set rosetta_b_factor = %s where str_uuid = %s and rosetta_b_factor is null "
        mysql_cursor.execute(mysql_sql, (str_b_factor, str_uuid))
        mysql_conn.commit()


    mysql_cursor.close()
    mysql_conn.close()

def add_pbd_to_web():

    mysql_conn = MySQLdb.connect("10.12.192.21", "dlp", "dlp13502965818", "AI", charset='utf8')
    mysql_cursor = mysql_conn.cursor()

    save_dir = '\\\\10.12.246.10\\人工智能\\192_18\\gene_web\\pbd_files'

    mysql_sql = " SELECT * from tb_gene_detail where upload_web = 1 "

    mysql_cursor.execute(mysql_sql)
    mysql_results = mysql_cursor.fetchall()

    for r in mysql_results:

        dir_path = str(r[3])
        dir_name = str(r[4])
        rosetta = str(r[9])
        if rosetta == 'None':
            rosetta = '0'
        str_uuid = str(r[10])


        my_save_dir = os.path.join(save_dir, str_uuid)
        if os.path.exists(my_save_dir) == False:
            os.makedirs(my_save_dir)

        my_save_dir = os.path.join(my_save_dir, dir_name)
        if os.path.exists(my_save_dir) == False:
            os.makedirs(my_save_dir)



        # my_save_dir_alphafold = os.path.join(my_save_dir, 'alphafold')
        # if os.path.exists(my_save_dir_alphafold) == False:
        #     os.makedirs(my_save_dir_alphafold)
        #
        # for f in ['ranked_0.pdb','ranked_1.pdb','ranked_2.pdb','ranked_3.pdb','ranked_4.pdb','ranking_debug.json']:
        #     alphafold_file = dir_path + '\\' + f
        #     if os.path.exists(alphafold_file) == True and os.path.exists(my_save_dir_alphafold + '\\' + f) == False:
        #         copyfile(alphafold_file, my_save_dir_alphafold + '\\' + f)



        if rosetta == '1':
            my_save_dir_rosetta = os.path.join(my_save_dir, 'rosetta')
            if os.path.exists(my_save_dir_rosetta) == False:
                print(dir_path, dir_name, rosetta, str_uuid)
                os.makedirs(my_save_dir_rosetta)

            for f in ['model_1.crderr.pdb', 'model_2.crderr.pdb', 'model_3.crderr.pdb', 'model_4.crderr.pdb', 'model_5.crderr.pdb','modelQ.dat']:
                rosetta_file = dir_path.replace('alphafold','rosetta') + '\\' + f
                if os.path.exists(rosetta_file) == True and os.path.exists(my_save_dir_rosetta + '\\' + f) == False:

                    print(rosetta_file, my_save_dir_rosetta + '\\' + f)

                    copyfile(rosetta_file, my_save_dir_rosetta + '\\' + f)




    mysql_cursor.close()
    mysql_conn.close()

if __name__ == '__main__':


    add_pbd_to_web()

    # move_pbd_to_web()

    # set_plddts_to_mysql()

    # set_b_factor_to_mysql()

    # get_rosetta_b_factor_from_dir()

    # get_fasta_alphafold()

    # get_fasta_rosetta()

    # move_sq_docx()

    # inset_to_mysql()

    # update_rosetta_to_mysql()