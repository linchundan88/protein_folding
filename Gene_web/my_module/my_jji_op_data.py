import mysql.connector


db_conn = mysql.connector.connect(host="10.12.246.21", port=3306,
                                  user="dlp", password="dlp13502965818", db="GENES",
                                  autocommit=False, charset='utf8')


cursor = db_conn.cursor()
sql = "SELECT * FROM tb_phenotype_gene"
cursor.execute(sql)
results = cursor.fetchall()

for rs in results:
    print(rs)

db_conn.close()