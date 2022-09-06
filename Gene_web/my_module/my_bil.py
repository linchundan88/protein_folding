
from my_module.my_db_helper import get_db_conn1


def get_phenotype():
    list_result = []
    list_genes = []
    list_omim = []

    db = get_db_conn1()
    cursor = db.cursor()
    sql = "SELECT phenosubtype_id, phenotype, phenosubtype, gene, omim  from view_gene_phenotype order by phenotype, phenosubtype"
    cursor.execute(sql)
    results = cursor.fetchall()

    phenosubtype_id_old = -1
    for rs in results:
        phenosubtype_id_new = rs[0]
        if (phenosubtype_id_new != phenosubtype_id_old) and (phenosubtype_id_old != -1):
            list_result.append((phenosubtype_id_old, phenotype_old, phenosubtype_old, list_genes, list_omim))
            list_genes = []
            list_omim = []

        phenosubtype_id_old, phenotype_old, phenosubtype_old = rs[0], rs[1], rs[2]
        list_genes.append(rs[3])
        list_omim.append(rs[4])

    list_result.append((phenosubtype_id_old, phenotype_old, phenosubtype_old, list_genes, list_omim))

    db.close()


    return list_result


def get_gene():
    list_result = []
    list_phenosubtype = []

    db = get_db_conn1()
    cursor = db.cursor()
    sql = "SELECT gene, omim, phenosubtype_id, phenotype, phenosubtype from view_gene_phenotype order by gene"
    cursor.execute(sql)
    results = cursor.fetchall()

    gene_old = ""
    for rs in results:
        gene_new = rs[0]

        if (gene_new != gene_old) and (gene_old != ""):
            list_result.append((gene_new, rs[1], list_phenosubtype))
            list_phenosubtype = []

        gene_old, omim_old = rs[0], rs[1]
        list_phenosubtype.append(rs[4])

    list_result.append((gene_old, omim_old, list_phenosubtype))

    db.close()


    return list_result


def get_gene_detail(gene):
    db = get_db_conn1()
    cursor = db.cursor()

    sql = 'select gene, omim from tb_gene where gene=%s'
    cursor.execute(sql, (gene,))
    results_gene = cursor.fetchone()

    sql = 'select gene, algorithm, seq_len, seq_text ,dir_name,  docx_name  from tb_gene_detail where gene=%s'
    cursor.execute(sql, (gene,))
    results_gene_detail = cursor.fetchall()

    db.close()

    return results_gene, results_gene_detail