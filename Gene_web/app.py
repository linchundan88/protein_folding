from flask import Flask, request, render_template, session

import os
import uuid
import pickle
from my_module import my_db_helper
import my_config
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xca\x5c\x86\x94\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'


@app.template_filter("my_round")
def do_round(num):
    return round(num, 2)


@app.route('/', methods=["GET", "POST"])
def homepage():

    my_disease = ''
    if request.method == 'GET':
        my_disease = str(request.args.get('disease'))
    if my_disease == 'None':
        my_disease = ''
    # print(my_disease)

    my_initials = ''
    if request.method == 'GET':
        my_initials = str(request.args.get('initials'))
    if my_initials == 'None':
        my_initials = ''
    # print(my_initials)

    my_gene_name = ''
    if request.method == 'GET':
        my_gene_name = str(request.args.get('gene_name'))
    if my_gene_name == 'None':
        my_gene_name = ''
    print('gene name: ', my_gene_name)


    results = my_db_helper.get_gene_main_detail(my_disease,my_initials,my_gene_name)

    result_list = []
    for row in results:
        result_list.append(row)

    results = my_db_helper.get_gene_disease_type()
    disease_type = [['All']]
    for row in results:
        disease_type.append(row)

    results = my_db_helper.get_gene_name_initials()
    gene_name_initials = [['All']]
    for row in results:
        gene_name_initials.append(row)


    file_view = 'gene.html'

    return render_template(file_view, result_list=result_list, disease_type=disease_type, gene_name_initials=gene_name_initials, gene_name=my_gene_name)


@app.route('/phenotype', methods=["GET", "POST"])
def phenotype():
    from my_module.my_bil import get_phenotype
    results = get_phenotype()
    file_view = 'phenotype.html'
    return render_template(file_view, result_phenotype=results)


@app.route('/gene', methods=["GET", "POST"])
def gene():
    from my_module.my_bil import get_gene
    results = get_gene()
    file_view = 'gene_jji.html'

    return render_template(file_view, result_gene=results)

@app.route('/gene_detail_jji/<string:gene>', methods=["GET", "POST"])
def gene_detail_jji(gene):
    from my_module.my_bil import get_gene_detail
    (results_gene, results_gene_detail) = get_gene_detail(gene)
    file_view = 'gene_detail_jji.html'

    return render_template(file_view,  results_gene=results_gene, results_gene_detail=results_gene_detail)


@app.route('/gene_detail', methods=["GET", "POST"])
def gene_detail():

    my_id = ''
    if request.method == 'GET':
        my_id = str(request.args.get('id'))
    if my_id == 'None':
        my_id = ''

    my_pbd_link = ''
    if request.method == 'GET':
        my_pbd_link = str(request.args.get('pbd_link'))
    if my_pbd_link == 'None':
        my_pbd_link = ''


    result_one = my_db_helper.get_gene_main_detail_one(my_id,my_pbd_link)

    baseDir = os.path.dirname(os.path.abspath(__name__))

    alphafold_dir = os.path.join(baseDir, 'static', 'pbd_files', result_one[10],result_one[9],'alphafold')
    dict_plddt = my_db_helper.get_lpddt_from_pbd_json(alphafold_dir)
    # print(dict_plddt)


    dict_b_factor = {}
    rosetta_dir = os.path.join(baseDir, 'static', 'pbd_files', result_one[10], result_one[9], 'rosetta')
    for i in range(1, 6):
        file_key = 'model_' + str(i) + '.crderr.pdb'
        rosetta_file = os.path.join(rosetta_dir,file_key)
        if os.path.exists(rosetta_file) == True:
            dict_b_factor[file_key],_ = my_db_helper.get_avg_b_factor(rosetta_file)

    # print(dict_b_factor)



    file_view = 'gene_detail.html'

    return render_template(file_view, result_one=result_one, dict_plddt = dict_plddt, dict_b_factor = dict_b_factor)


@app.route('/gene_main_list', methods=["GET", "POST"])
def gene_main_list():


    data = json.loads(request.form.get('data'))


    my_disease = data['disease_name']
    if my_disease == 'None':
        my_disease = ''
    print('disease: ', my_disease)

    my_gene_name = data['gene_name']
    if my_gene_name == 'None':
        my_gene_name = ''
    print('gene name: ', my_gene_name)

    my_initials = data['initials']
    if my_initials == 'None':
        my_initials = ''
    print('initials: ', my_initials)



    results = my_db_helper.get_gene_main_detail(my_disease, my_initials, my_gene_name)

    result_list = []
    for row in results:
        result_list.append(row)

    file_view = 'gene_main_list.html'

    return render_template(file_view, result_list=result_list)

@app.route('/embedded', methods=["GET", "POST"])
def embedded():

    my_str_uuid = ''
    if request.method == 'GET':
        my_str_uuid = str(request.args.get('str_uuid'))
    if my_str_uuid == 'None':
        my_str_uuid = ''

    my_dir_name = ''
    if request.method == 'GET':
        my_dir_name = str(request.args.get('dir_name'))
    if my_dir_name == 'None':
        my_dir_name = ''

    my_algorithm = ''
    if request.method == 'GET':
        my_algorithm = str(request.args.get('algorithm'))
    if my_algorithm == 'None':
        my_algorithm = ''

    my_model_name = ''
    if request.method == 'GET':
        my_model_name = str(request.args.get('model_name'))
    if my_model_name == 'None':
        my_model_name = ''



    file_view = 'embedded.html'

    return render_template(file_view, str_uuid=my_str_uuid, dir_name=my_dir_name, algorithm=my_algorithm, model_name=my_model_name)

@app.route('/gene_request', methods=["GET", "POST"])
def gene_request():

    my_gene_name = ''
    my_omim = ''
    my_describe = ''
    my_wt_mutant = ''
    my_model = ''
    my_sequence = ''
    my_contact = ''
    my_email = ''
    my_purpose = ''
    my_tip = ''

    if request.method == 'POST':

        my_gene_name = str(request.form.get('gene'))
        if my_gene_name == 'None':
            my_gene_name = ''

        my_omim = str(request.form.get('omim'))
        if my_omim == 'None':
            my_omim = ''

        my_describe = str(request.form.get('describe'))
        if my_describe == 'None':
            my_describe = ''

        my_wt_mutant = str(request.form.get('wt_mutant'))
        if my_wt_mutant == 'None':
            my_wt_mutant = ''

        my_model_alphafold = str(request.form.get('model_alphafold'))
        if my_model_alphafold == 'None':
            my_model_alphafold = ''

        my_model_rosetta = str(request.form.get('model_rosetta'))
        if my_model_rosetta == 'None':
            my_model_rosetta = ''

        my_model = my_model_alphafold +'_'+ my_model_rosetta


        my_sequence = str(request.form.get('sequence'))
        if my_sequence == 'None':
            my_sequence = ''

        my_contact = str(request.form.get('contact'))
        if my_contact == 'None':
            my_contact = ''

        my_email = str(request.form.get('email'))
        if my_email == 'None':
            my_email = ''

        my_purpose = str(request.form.get('purpose'))
        if my_purpose == 'None':
            my_purpose = ''

        my_str_uuid = str(uuid.uuid1())
        my_seq_len = str(len(my_sequence))


        my_db_helper.set_gene_request(my_str_uuid, my_gene_name, my_omim, my_describe, my_wt_mutant, my_model,
                                      my_sequence, my_seq_len, my_contact, my_email, my_purpose)

        my_tip = "Submitted successfully! The predicted results will be send to your Email ( " + my_email + " ) within one week!"




    dict_data = {
        'gene_name' : my_gene_name,
        'omim' : my_omim,
        'describe' : my_describe,
        'wt_mutant' : my_wt_mutant,
        'model' : my_model,
        'sequence' : my_sequence,
        'contact' : my_contact,
        'email' : my_email,
        'purpose' : my_purpose,
    }



    file_view = 'gene_request.html'

    return render_template(file_view, dict_data = dict_data, tip = my_tip)

#region login, logout, register
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        lang = request.args.get('lang')
        session['lang'] = lang
        if lang == 'en':
            return render_template('login.html')
        else:
            return render_template('login_cn.html')

    if request.method == 'POST':
        lang = request.form['lang']
        username = request.form['username']
        password = request.form['password']

        account_list = []
        login_OK = my_db_helper.login(username, password, account_list, write_log=True,
                                      source_ip=request.remote_addr)
        if login_OK:
            session['username'] = username
            session['lang'] = lang
            if len(account_list) > 0:
                session['hospital'] = str(account_list[0][0][5])

            if lang == 'en':
                return render_template('uploadfile.html')
            else:
                return render_template('uploadfile_cn.html')
        else:
            if lang == 'en':
                error_msg = 'username or password error!'
                return render_template('login.html', error_msg=error_msg)
            else:
                error_msg = '账号或者密码错误!'
                return render_template('login_cn.html', error_msg=error_msg)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('homepage.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        if session.get('lang') is not None:
            if session.get('lang') == 'en':
                return render_template('register.html')

        return render_template('register_cn.html')

    if request.method == 'POST':
        lang = session.get('lang', 'en')

        email = request.form['email']
        name = request.form['name']
        tel = request.form['tel']
        company = request.form['company']
        title = request.form['title']

        if not '@' in email or email == '' or name == '' or company == '' or title == '':
            if lang == 'en':
                return render_template(request, 'register.html', error_msg='Please fill in the form correctly!')
            else:
                return render_template(request, 'register_cn.html', error_msg= '请按照规范填写表单')

        from my_module import my_db_helper
        results = my_db_helper.check_register(email)

        if len(results) > 0:  # 邮件账号已经使用
            if lang == 'en':
                return render_template('register.html', error_msg='This email has been used!')
            else:
                return render_template('register_cn.html', error_msg='该电子邮件已经被使用!')
        else:
            my_db_helper.do_register(email, name, tel, company, title)

            if lang == 'en':
                return render_template('register_ok.html')
            else:
                return render_template('register_ok_cn.html')

#endregion







if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=my_config.PORT_Web,
        debug=True
    )
