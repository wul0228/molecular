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

def extractDate(new_file_path):

    # filename = psplit(new_file_path)[1].strip().split('.xml.zip')[0].strip()
    # # gunzip file
    # filedir = new_file_path.split('.zip')[0].strip()

    # unzip = 'unzip {} -d {}'.format(new_file_path,drugbank_raw)

    # os.popen(unzip)

    # # raname
    # command = 'mv  {}/"full database.xml"  {}/full_database.xml'.format(drugbank_raw,drugbank_raw)

    # os.popen(command)
    #--------------------------------------------------------------------------------------------------------
    # parser tree
    tree = et.parse(open(pjoin(drugbank_raw,'full_database.xml')))

    root = tree.getroot()

    n = 0

    print len(root.getchildren())

    for child in root.getchildren()[:1]:
        parseDrug(child)



        # f = open(pjoin(drugbank_store,'tree_{}.txt'.format(n)),'w')
        
        # drug_dict = parseNode(child)
        
        # f.write(str(drug_dict))

        # f.close()

        # n += 1
def parseDrug(node):

    tree = dict()

    for child in node.getchildren():

        tag = child.tag.split('{http://www.drugbank.ca}')[1].strip()

        text = child.text

        if tag not in tree:

            tree[tag] = text

        else:
            tag_val = tree[tag]
            if not isinstance(tag_val,list):
                tree[tag] = [tag_val]
            tree[tag].append(text)


    with open('./test.json','w') as wf:
        json.dump(tree,wf,indent=2)
    print len(tree.keys())

def parseNode(node):

    tree = {}

    for child in node.getchildren():

        child_tag = child.tag .split('{http://www.drugbank.ca}')[1].strip()
        child_attr = child.attrib
        child_text = child.text.strip() if child.text is not None else ''  
        child_tree = parseNode(child)

        if not child_tree:
            child_dict = createDict(child_tag,child_text,child_attr)
        else:
            child_dict = createDict(child_tag,child_tree,child_attr)

        if child_tag not in tree:
            tree.update(child_dict)
            continue

        atag = '@' + child_tag
        atree = tree[child_tag]
   
        if not isinstance(atree,list):
            if not isinstance(atree,dict):
                atree = {}
            if atag  in tree:
                atree['#' + child_tag] = tree[atag]
                del tree[atag]

            tree[child_tag] = [atree]

        if child_attr:
            child_tree['#' +child_tag] = child_attr

        tree[child_tag].append(child_tree)

    return tree

def createDict(tag,value,attr=None):

    dic = {tag : value}

    if attr:

        atag = '@' + tag

        aattr = {}

        for key,val in attr.items():

            aattr[key] = val

        dic[atag] = aattr

        del atag
        del aattr

    return dic

def deblank(dic):

    for key,val in dic.items():

        if not val:

            dic.pop(key)

        elif isinstance(val,dict) and len(val.keys()) ==1:


            val_key = val.keys()[0]

            val_val = val[val_key]
            dic.pop(key)

            dic.update({val_key:val_val})

    return dic

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
    extractDate('/home/user/project/molecular/mymol/dataraw/drugbank/drugbank_5-0-9_171102161331.xml.zip')

    # f = eval(open(os.path.join(drugbank_store,'tree_0.txt')).read())

    # dic = dict()

    # for key,val in f.items():

    #     dic[key] = val

    # with open(os.path.join(drugbank_store,'dic_0.json'),'w') as wf:
    #     json.dump(dic,wf,indent=2)