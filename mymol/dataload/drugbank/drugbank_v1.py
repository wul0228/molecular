#!/usr/bin/env python
# --coding:utf-8--
# date:20171102
# author:wuling
# emai:ling.wu@myhealthgene.com

'''
this model setted  to download, extract and update drugbank data automatically
'''

import requests
from share.config_v1 import *
from share.share_v1 import *
from bs4 import BeautifulSoup as bs
from lxml import etree as et
import xmltodict

version = '1.0'

model_name = psplit(os.path.abspath(__file__))[1]

# buid directory to store raw an extracted data
(drugbank_load,drugbank_raw,drugbank_store,drugbank_db) = buildDir('drugbank')

# create a log file (json) , to record the data edition and update date
if not os.path.exists(pjoin(drugbank_load,'drugbank.log')):

    with open(pjoin(drugbank_load,'drugbank.log'),'w') as wf:

        json.dump([
            ('edition','update date','drugbank_v*'),
            ('5-0- 9-20171002',today,model_name),],wf,indent=2)

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

# main code
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

    return  new_file_path

def extractDate(new_file_path):

    # gunzip file
    # filedir = new_file_path.split('.zip')[0].strip()

    # unzip = 'unzip {} -d {}'.format(new_file_path,drugbank_raw)

    # os.popen(unzip)

    # # raname
    # name = [i for i in listdir(drugbank_raw) if i.startswith('full')][0]

    # old = pjoin(drugbank_raw,name)

    # new = pjoin(drugbank_raw,'full_database.xml')

    # os.rename(old,new)

    # load xml file
    # filepath = pjoin(drugbank_raw,'full_database.xml') 

    # database = xmltodict(open(filepath))

    database = json.load(pjoin(drugbank_raw,'full_database.json'))


def deblank(dic):
    pass
    if len(dic.keys()) == 1:
        return (dic.keys()[0],)

def standarData():
    pass

def insertData():
    pass

def selectData():
    pass

def updateData():
    '''
    this function is to check the edition existed and update or not
    '''
    latest_edition = json.load(open(pjoin(drugbank_load,'drugbank.log')))[-1][0].rsplit('-',1)[0].strip()

    (download_url,releases) = getWebPage()

    if releases != latest_edition:

        choseDown(choice = 'download')

        drugbank_log .append((latest_edition,today,os.path.abspath(__file__)))

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

        save_file_path = downloadData()

        store_file_path  = extractData(save_file_path)

        insertData(str(store_file_path))

    elif choice == 'select':

        selectData()
    else:
        pass

def main():

    tips = '''
    Download : 1
    Update : 2def insertData():
    Select : 3
    '''
    index = raw_input(tips)

    chose = {'1':'download','2':'update','3':'select'}

    choseDown(choice =chose[index])

if __name__ == '__main__':
    # main()
    pass
    new_file_path = '/home/user/project/molecular/mymol/dataraw/drugbank/drugbank_5-0-9_171102161331.xml.zip'
    extractDate(new_file_path)
    # for name in listdir(drugbank_raw):
    #     print name



