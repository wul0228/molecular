#!/usr/bin/env python
# --coding:utf-8--
# date:20171102
# author:wuling
# emai:ling.wu@myhealthgene.com

'''
this model setted  to download, extract and update drugbank data automatically
'''
import sys
reload(sys)
sys.path.append('..')
sys.setdefaultencoding = ('utf-8')
import copy
import requests
import xmltodict
from share.config_v1 import *
from share.share_v1 import *
from bs4 import BeautifulSoup as bs
from lxml import etree as et
from xmltodict import parse

version = '1.0'

model_name = psplit(os.path.abspath(__file__))[1]

# buid directory to store raw an extracted data
(drugbank_load,drugbank_raw,drugbank_store,drugbank_db) = buildSubDir('drugbank')

# main code
def getWebPage():
    '''
    this function is to get the download web page of drugbank by python crawler
    '''
    # get responce from drug bank
    web = requests.get(drugbank_start_url)

    # parser html with lxml
    soup = bs(web.text,'lxml')

    # get  content with link
    all_a = soup.select('#full > table > tbody > tr > td > a')

    for a in all_a:

        # get  the download href
        if a.get_text().strip() == 'Download':

            download_url = drugbank_homepage + a.attrs.get('href')

            releases = download_url.split('/releases/')[1].strip().split('/',1)[0].strip()

    return (download_url,releases)

def downloadData():
    '''
    this function is to connect drugbanek web  site and log in to download zip file
    '''

    #because the data keep update ,so the url would change frequently, but the website frame remain, 
    #so we get download url with web crawler

    (download_url,releases) = getWebPage()

    command = 'wget    -P {}  --http-user={}  --http-password={}  {}'.format(drugbank_raw,drugbank_log_user,drugbank_log_passwd,download_url)

    os.popen(command)

    # rename
    save_file_name = 'drugbank_{}_{}.xml.zip'.format(releases,today)

    old_file_path = pjoin(drugbank_raw,'all-full-database')

    new_file_path =  pjoin(drugbank_raw,save_file_name)

    os.rename(old_file_path,new_file_path)

    # # initialiaze log file
    if not os.path.exists(pjoin(drugbank_load,'drugbank.log')):

        initLogFile('drugbank',model_name,drugbank_load,mt=releases)

    return  new_file_path

def extractData(new_file_path):

    filename = psplit(new_file_path)[1].strip().split('.xml.zip')[0].strip()
    # gunzip file
    # filedir = new_file_path.split('.zip')[0].strip()

    unzip = 'unzip {} -d {}'.format(new_file_path,drugbank_raw)

    os.popen(unzip)

    # raname

    filepath = pjoin(drugbank_raw,'{}.xml'.format(filename))

    command = 'mv  {}/"full database.xml"  {}'.format(drugbank_raw,filepath)

    os.popen(command)
   
    # parse tree
    tree = parse(open(filepath))

    # the only key in tree dict is drugbank
    db = tree["drugbank"]

    version = db["@version"]

    exported = db["@exported-on"]

    drugs = db['drug']

    drug_store = pjoin(drugbank_store,filename)

    createDir(drug_store)

    n = 0

    for drug in drugs:

        stand_drug = standarData(drug)

        with open(pjoin(drug_store,'drug_{}.json'.format(str(n))),'w') as wf:

            json.dump(stand_drug,wf,indent=2)

        n += 1
        print n 

    return drug_store

def standarData(drug):

    equal = False

    start = drug

    while not equal :

        a = deBlankDict(start)

        b = deBlankDict(a)

        if b == a:
            equal = True 
            end = b
        else:
            start = b

    return end

def insertData(storedir):

    conn = MongoClient('127.0.0.1',27017)

    db = conn.DrugBank

    collection_name = psplit(storedir)[1].strip().replace('-','')

    collection = db.collection_name
    
    for filename in listdir(storedir):

        filepath = pjoin(storedir,filename)

        drug = json.load(open(filepath))

        drug['CREATED_TIME'] = datetime.now()

        collection.insert(drug)

    db.collection_name.rename(collection_name )

    print 'insertData completed !'

def selectData():
    '''
    this function is set to select data from mongodb
    '''
    conn = MongoClient('127.0.0.1',27017)

    db = conn.DrugBank

    colnamehead = 'drugbank'

    querykey = 'name'

    dataFromDB(db,colnamehead,querykey,queryvalue=None)
    
def updateData():
    '''
    this function is to check the edition existed and update or not
    '''
    latest_edition = json.load(open(pjoin(drugbank_load,'drugbank.log')))[-1][0].strip()

    (download_url,releases) = getWebPage()

    if releases != latest_edition:

        choseDown(choice = 'download')

        drugbank_log .append((releases,today,os.path.abspath(__file__)))

        with open(pjoin(dataload,'drugbank.log'),'w') as wf:
            json.dump(drugbank_log,wf,indent=2)
        
        print  'dataupdate completed !'

    else:

        print 'remote latest edition is %s ' % latest_edition 

        print 'local is the latest edition!'


def choseDown(choice = 'update'):
    
    if choice == 'update':

        updateData()

    elif choice == 'download':

        save = downloadData()

        store  = extractData(save)

        insertData(store)

    elif choice == 'select':

        selectData()
    else:
        pass

def main():

    tips = '''
    Download : 1
    Update : 2
    Select : 3
    '''
    index = raw_input(tips)

    chose = {'1':'download','2':'update','3':'select'}

    choseDown(choice =chose[index])

if __name__ == '__main__':
    main()
