
import os
import sys
import sqlite3
import json
import mysql.connector

import datetime
import string
import random

DB_TYPE = 'mysql'  # mysql

def get_db_conn():

    if DB_TYPE == 'sqlite':
        db_file = os.path.join(sys.path[0], 'database', 'rop.sqlite')
        db_conn = sqlite3.connect(db_file)

    if DB_TYPE == 'mysql':
        json_file_path = os.path.join(sys.path[0], 'database', 'db_config.json')
        json_file = open(json_file_path, 'r')
        data = json.load(json_file)
        json_file.close()

        # import MySQLdb
        # db_conn = MySQLdb.connect(data['host'], data['username'], data['password'],
        #                      data['database'], use_unicode=True, charset='utf8')
        db_conn = mysql.connector.connect(host=data['host'], port=data['port'],
            user=data['username'], password=data['password'], db=data['database'],
            autocommit=False, charset='utf8')

    return db_conn



def get_db_conn1():

    if DB_TYPE == 'sqlite':
        db_file = os.path.join(sys.path[0], 'database', 'rop.sqlite')
        db_conn = sqlite3.connect(db_file)

    if DB_TYPE == 'mysql':
        json_file_path = os.path.join(sys.path[0], 'database', 'db_config1.json')
        json_file = open(json_file_path, 'r')
        data = json.load(json_file)
        json_file.close()

        # import MySQLdb
        # db_conn = MySQLdb.connect(data['host'], data['username'], data['password'],
        #                      data['database'], use_unicode=True, charset='utf8')
        db_conn = mysql.connector.connect(host=data['host'], port=data['port'],
            user=data['username'], password=data['password'], db=data['database'],
            autocommit=False, charset='utf8')

    return db_conn


def login(username, password, account_list=None, write_log=True, source_ip='127.0.0.1'):
    db = get_db_conn()
    cursor = db.cursor()

    from my_module.my_compute_digest import CalcSha1_str
    password_encrypt = CalcSha1_str(password)

    if DB_TYPE == 'mysql':
        sql = "SELECT * FROM tb_account WHERE username=%s and password_encrypt=%s and enabled=1"
    if DB_TYPE == 'sqlite':
        sql = "SELECT * FROM tb_account WHERE username=? and password_encrypt=? and enabled=1"
    cursor.execute(sql, (username, password_encrypt))
    results = cursor.fetchall()

    if len(results) == 1:
        if write_log:
            if DB_TYPE == 'mysql':
                sql = "insert into tb_log(username,log_memo) values(%s,%s)"
            if DB_TYPE == 'sqlite':
                sql = "insert into tb_log(username,log_memo) values(?,?)"
            cursor.execute(sql, (username, 'login_successful, ip:' + source_ip))
            db.commit()

        if account_list is None:
            account_list = []
        account_list.append(results)

        return True
    else:
        if write_log:
            if DB_TYPE == 'mysql':
                sql = "insert into tb_log(username,log_memo) values(%s,%s)"
            if DB_TYPE == 'sqlite':
                sql = "insert into tb_log(username,log_memo) values(?,?)"
            cursor.execute(sql, (username, 'login_failure, ip:' + source_ip))
            db.commit()

        return False

    cursor.close()
    db.close()

def check_register(email):
    db = get_db_conn()
    cursor = db.cursor()

    if DB_TYPE == 'mysql':
        sql_check_email = "SELECT * FROM tb_account WHERE username=%s and enabled=1"
    if DB_TYPE == 'sqlite':
        sql_check_email = "SELECT * FROM tb_account WHERE username=? and enabled=1"

    cursor.execute(sql_check_email, (email,))
    rs = cursor.fetchall()

    cursor.close()
    db.close()

    return rs

def do_register(email, name, tel, company, title):
    db = get_db_conn()
    cursor = db.cursor()
    if DB_TYPE == 'mysql':
        sql_insert = 'insert into tb_register(email, password, name, tel, company, title) values(%s, %s, %s, %s, %s, %s)'
    if DB_TYPE == 'sqlite':
        sql_insert = 'insert into tb_register(email, password, name, tel, company, title) values(?, ?, ?, ?, ?, ?)'
    cursor.execute(sql_insert, (email, '', name, tel, company, title))
    db.commit()
    db.close()


def get_gene_main_detail(disease, initials, gene_name):

    db = get_db_conn()
    cursor = db.cursor()

    if DB_TYPE == 'mysql':
        sql = 'select * from v_get_gene_main_detail_web where 1=1 '

        if len(disease) > 0 and disease != 'All' and disease != '全部':
            sql = sql + ' and disease_type = "' + disease + '"'

        if len(initials) > 0 and initials != 'All' and initials != '全部':
            sql = sql + ' and upper(gene) like "' + initials + '%"'

        if len(gene_name) > 0 and gene_name != 'All' and gene_name != '全部':
            sql = sql + ' and ( upper(gene) like "%' + gene_name + '%" or upper(disease_en_1) like "%' + gene_name + '%" ) '


    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()

    return results

def get_gene_main_detail_one(id, pbd_link):

    db = get_db_conn()
    cursor = db.cursor()

    if DB_TYPE == 'mysql':
        sql = 'select * from v_get_gene_main_detail_web where 1=1 '

        if len(id) > 0:
            sql = sql + ' and id = ' + id + ' '

        if len(pbd_link) > 0:
            sql = sql + ' and dir_name = "' + pbd_link + '"'


    cursor.execute(sql)
    results = cursor.fetchone()
    db.close()

    return results

def get_gene_disease_type():

    db = get_db_conn()
    cursor = db.cursor()

    if DB_TYPE == 'mysql':
        sql = 'select distinct disease_type, web_sort from v_get_gene_main_detail_web order by web_sort'

    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()

    return results

def get_gene_name_initials():

    db = get_db_conn()
    cursor = db.cursor()

    if DB_TYPE == 'mysql':
        sql = 'select distinct left(upper(gene),1) from v_get_gene_main_detail_web order by left(upper(gene),1)'

    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()

    return results

def set_gene_request(str_uuid, gene_name,omim,gene_desc,wt_mutant,model,seq_text,seq_len,contact,email,purpose):

    db = get_db_conn()
    cursor = db.cursor()


    sql_insert = 'insert into tb_gene_request(str_uuid,gene_name,omim, gene_desc, wt_mutant,model,seq_text,seq_len,contact,email,purpose) values( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    cursor.execute(sql_insert, (str_uuid,gene_name,omim,gene_desc,wt_mutant,model,seq_text,seq_len,contact,email,purpose))

    db.commit()
    db.close()

def get_lpddt_from_pbd_json(base_dir):

    json_file = open(os.path.join(base_dir,'ranking_debug.json'),'r')
    data = json.load(json_file)
    json_file.close()

    dict_plddt = {}
    for i in range(len(data['plddts'])):
        dict_plddt['ranked_' + str(i) + '.pdb'] = round(float(data['plddts'][data['order'][i]]),4)

    return dict_plddt

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


if __name__ == '__main__':

    # json_file_path = os.path.join(os.path.abspath('..'), 'database', 'db_config.json')
    # json_file = open(json_file_path,'r')
    # data = json.load(json_file)
    # print(json_file, data['host'])
    # json_file.close()
    #
    # db_conn = mysql.connector.connect(host=data['host'], port=data['port'],
    #                                   user=data['username'], password=data['password'], db=data['database'],
    #                                   autocommit=False, charset='utf8')
    #
    # print(db_conn)
    # db_conn.close()

    aa = os.path.split(str('D:\\AI\\ROP\\1.jpg').replace('\\','/'))
    print(aa,os.pathsep)