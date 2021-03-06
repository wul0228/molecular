#!/usr/bin/env python
# --coding:utf-8--
# date:20171107
# author:wuling
# emai:ling.wu@myhealthgene.com

#+++++++++++++++++++++++++ packages ++++++++++++++++++++++++++++++++++++++#
import os , sys, tsv, json, time, rdkit, MySQLdb
from ftplib import FTP
from rdkit import Chem
from rdkit.Chem import AllChem
from datetime import datetime
from selenium import webdriver
from pymongo import MongoClient

#+++++++++++++++++++++++++ simplify  method+++++++++++++++++++++++++++++++++#
listdir = os.listdir

pjoin = os.path.join

psplit = os.path.split

mfsma = Chem.MolFromSmarts

mtsma = Chem.MolToSmarts

mfsmi = Chem.MolFromSmiles

mtsmi = Chem.MolToSmiles

 #++++++++++++++++++++++++universal consttant +++++++++++++++++++++++++++++++++#

mymol_path = os.path.split(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])[0]

datadirs= ['dataraw','datastore','database']

dataload = pjoin(mymol_path,'dataload')

dataraw = pjoin(mymol_path,'dataraw')

datastore = pjoin(mymol_path,'datastore')

database = pjoin(mymol_path,'database')

now  = datetime.now().strftime('%y%m%d')

today = datetime.now().strftime('%y%m%d%H%M%S')

#~~~~~~~~~~~~~~~~~~~PubChem~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
pubchem_ftp_infos = {
    'host' : 'ftp.ncbi.nlm.nih.gov' ,
    'user':'anonymous',
    'passwd' : '',
    'logdir' : '/pubchem/Compound/CURRENT-Full/SDF/'
    }

pubchem_compound_path = '/pubchem/Compound/CURRENT-Full/SDF/'

#~~~~~~~~~~~~~~~~~~~CheEBI~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
chebi_ftp_infos = {
    'host' : 'ftp.ebi.ac.uk',
    'user':  '',
    'passwd': '',
    'logdir':  '/pub/databases/chebi/SDF/'
    }

chebi_compound_path = '/pub/databases/chebi/SDF/'

chebi_compound_filename =  'ChEBI_complete.sdf.gz'

chebi_compound_filepath =  '/pub/databases/chebi/SDF/ChEBI_complete.sdf.gz'

#~~~~~~~~~~~~~~~~~~~DrugBank~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

drugbank_homepage = 'https://www.drugbank.ca'

drugbank_start_url = 'https://www.drugbank.ca/releases/latest'

drugbank_log_user = 'myhealthgene@163.com'

drugbank_log_passwd = 'myhealthgene@408'

#++++++++++++++++++++++++init file and directory ++++++++++++++++++++++++++++++++++#




