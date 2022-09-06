CREATE DATABASE `GENES` /*!40100 DEFAULT CHARACTER SET utf8 */;


CREATE TABLE `tb_gene` (
  `gene` varchar(20) NOT NULL,
  `omim` varchar(20) DEFAULT NULL,
  `memo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`gene`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `tb_gene_detail` (
  `gene` varchar(255) DEFAULT NULL,
  `algorithm` varchar(255) DEFAULT NULL,
  `wt` int(2) unsigned zerofill DEFAULT NULL,
  `dir_path` varchar(1024) DEFAULT NULL,
  `dir_name` varchar(255) DEFAULT NULL,
  `docx_name` varchar(255) DEFAULT NULL,
  `seq_text` text,
  `seq_len` int(5) DEFAULT NULL,
  `status` int(2) DEFAULT NULL COMMENT '1=''已预测''',
  `rosetta` int(2) unsigned zerofill DEFAULT NULL,
  `str_uuid` varchar(64) DEFAULT NULL,
  `upload_web` int(2) DEFAULT '0',
  `insert_date_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `alphafold_plddt` varchar(100) DEFAULT NULL,
  `rosetta_b_factor` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `tb_gene_disease_type` (
  `disease_type_cn` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `disease_type_en` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `web_sort` int(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `tb_gene_seq_structure` (
  `gene` varchar(255) DEFAULT NULL,
  `algorithm` varchar(255) DEFAULT NULL,
  `wt` int(2) unsigned zerofill DEFAULT NULL,
  `dir_path` varchar(1024) DEFAULT NULL,
  `dir_name` varchar(255) DEFAULT NULL,
  `docx_name` varchar(255) DEFAULT NULL,
  `seq_text` text,
  `seq_len` int(5) DEFAULT NULL,
  `status` int(2) DEFAULT NULL COMMENT '1=''已预测''',
  `rosetta` int(2) unsigned zerofill DEFAULT NULL,
  `str_uuid` varchar(64) DEFAULT NULL,
  `upload_web` int(2) DEFAULT '0',
  `insert_date_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `alphafold_plddt` varchar(100) DEFAULT NULL,
  `rosetta_b_factor` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `tb_phenotype` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `phenotype` varchar(50) DEFAULT NULL,
  `phenosubtype` varchar(128) DEFAULT NULL,
  `phenotype_cn` varchar(50) DEFAULT NULL,
  `web_sort` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1254 DEFAULT CHARSET=utf8;

CREATE TABLE `tb_phenotype_gene` (
  `gene` varchar(50) DEFAULT NULL,
  `phenosubtype_id` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


SELECT `v_by_gene`.`gene`,
    `v_by_gene`.`omim`,
    `v_by_gene`.`phenosubtype`
FROM `GENES`.`v_by_gene`;

SELECT `v_by_phenotype`.`phenosubtype`,
    `v_by_phenotype`.`gene`
FROM `GENES`.`v_by_phenotype`;

SELECT `v_gene_sequence`.`gene`,
    `v_gene_sequence`.`wt`,
    `v_gene_sequence`.`seq_text`,
    `v_gene_sequence`.`seq_len`,
    `v_gene_sequence`.`rosetta`,
    `v_gene_sequence`.`dir_name`,
    `v_gene_sequence`.`str_uuid`,
    `v_gene_sequence`.`alphafold_plddt_0`,
    `v_gene_sequence`.`alphafold_plddt`,
    `v_gene_sequence`.`rosetta_b_factor_1`,
    `v_gene_sequence`.`rosetta_b_factor`,
    `v_gene_sequence`.`omim`
FROM `GENES`.`v_gene_sequence`;

SELECT `view_gene_phenotype`.`gene`,
    `view_gene_phenotype`.`phenosubtype_id`,
    `view_gene_phenotype`.`phenotype`,
    `view_gene_phenotype`.`phenosubtype`,
    `view_gene_phenotype`.`omim`
FROM `GENES`.`view_gene_phenotype`;
