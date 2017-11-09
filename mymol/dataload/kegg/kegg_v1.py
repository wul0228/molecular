#!/usr/bin/env python
# --coding:utf-8--
# date:20171109
# author:wuling
# emai:ling.wu@myhealthgene.com

'''
this model setted  to download, extract and update chebi data automatically
'''
import sys
sys.path.append('..')
sys.setdefaultencoding = ('utf-8')
import  requests 
from share.share_v1 import *
from share.config_v1 import *
from bs4 import BeautifulSoup as bs

version = '1.0'

model_name = psplit(os.path.abspath(__file__))[1]

# buid directory to store raw an extracted data
(kegg_load,kegg_raw,kegg_store,kegg_db) = buildSubDir('kegg')

# main code
def getOneMol(href):
    '''
    this function is to crawling a compound infos from kegg  Compund
    '''
    mol_web = requests.get(href)

    print 'mol_web'

    mol_soup = bs(mol_web.text,'lxml')

    print 'mol_soup'

    form = mol_soup.find('form')

    print 'form'
    # table = form.find(name='table',attrs={'cellpadding':'2','border':'0'})
    table = form.select('table > tr > td > table')

    print 'table'

    trs = table.select('tr')

    for tr in trs:
        th = tr.select('th')[0]
        td = tr.select('td')[0]
        print th.text
        print td.text
        print '-'*50

    pass
def downloadData(redownload = False):
    '''
    this function is to connect kegg web  site to crawling the compound data
    paras:
    redownload-- default False, check to see if exists an old edition before download
                       -- if set to true, download directly with no check
    download process
    1. get release and entries
    2. get all href of compound
    3. get compound infos one by one
    '''
    if  not redownload:

     # check  to see if there have been an edition

        (choice,existKeggFile) = lookforExisted(kegg_raw,'kegg_compound')

        if choice != 'y':
            return

    if redownload or not existKeggFile or  choice == 'y':

        # 1. get  the release and entries
        dbget_page = requests.get(kegg_dbget_url)

        dbget_soup = bs(dbget_page.text,'lxml')

        divs = dbget_soup.find_all('div')

        for div in divs:

            if div.text.count('Release'):

                release = div.text.split('Release')[1].strip().split('\n',1)[0].strip()

                entries = div.text.split('entries')[0].strip().rsplit('\n',1)[1].strip()

                break

        # 2. get all href of compound
        comphref_page = 'http://www.kegg.jp/dbget-bin/www_bfind_sub?dbkey=compound&keywords=c&mode=bfind&max_hit=nolimit'
        
        comphref_page = requests.get(comphref_page)
       
        comphref_soup = bs(comphref_page.text,'lxml')

            # divs = comphref_soup.select('body > form > div')  #18112 (head contained)
        comp_divs = comphref_soup.find_all(name='div',attrs = {'style':'width:600px'})

            # create a dict to store compound id and its href
        id_href = dict()

        for  comp in comp_divs:

            a_tag = comp.select('a')[0]

            kegg_id  = a_tag.text

            kegg_href = 'http://www.kegg.jp' + a_tag['href']

            id_href[kegg_id] = kegg_href

        # get compound infos one by one

def extractData():
    pass
def insertData():
    pass
def selectData():
    pass
def updateData():
    pass

def main():
    downloadData(redownload=True)

if __name__ == '__main__':
    # main()
    href = 'http://www.kegg.jp/dbget-bin/www_bget?cpd:C00002'
    getOneMol(href)
    # pass