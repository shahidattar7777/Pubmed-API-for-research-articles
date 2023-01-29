# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import xml.etree.ElementTree as et
import pandas as pd

import ssl
import urllib.request, urllib.parse, urllib.error
import numpy as np

#strid =''
df = pd.DataFrame(columns=['id', 'doi', 'keywords', 'journaltitle', 'Abstract', 'ArticleTitle','volume', 'issue', 'publication_date', 'authdetails' ])


# for i in range(300000):
#     print(i)

................................................
#THIS PART IS TO DOWNLOAD THE PUBMED IDS

#UNCOMMENT TO DOWNLOAD THE IDS FIRST 
#AFTER DOWNLOADING THE IDS DOWNLOAD THE DATA
......................................................
#     response = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&api_key=cb261cb142b6b0ca2eaae19a102da3716608&term=covid&retstart="+str(i)+"&retmax="+str(1))
#     #tree = ET.fromstring(response.content)
#     d = xmltodict.parse(response.content)
#     #print(d)
#     result =  d['eSearchResult']

#     idlist = result['IdList']
    
#     id = idlist['Id']
#     #print(id)
# #####
#     #row_each.append(id)

#     #print(df)
# #####   
#     strid = ''
#     strid += str(id)
#     strid = strid.replace(" ", "")
#     strid = strid.replace("'", "")
#     strid = strid.replace("[", "")
#     strid = strid.replace("]", "")
#     print(strid)
    
    
    

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE




##for i in range(1,300100,1000):
##    try:
##        address = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&api_key=cb261cb142b6b0ca2eaae19a102da3716608&term=covid&retstart="+str(i)+"&retmax="+str(999)
##        uh = urllib.request.urlopen(address, context = ctx)
##        data = uh.read()
##    except urllib.error.HTTPError:
##        pass
##        
##    root = et.fromstring(data)
##    
##    for id in root.iter('Id'):
##        idlist = np.append(idlist, int(id.text))

......................................................................................................

#IGNORE THIS PART AS I THOUGHT IT WAS BETTER TO DOWNLOAD THE IDS ONCE AND DOWNLOAD THE DATA IN BATCHES
......................................................................................................
ids = pd.read_csv('idlist2.csv')
idlist = ids.values.tolist()
del idlist[250001 : len(idlist)]
del idlist[0:236555]
i = -1
...................................................................................................


#THE FOLLOWING PART IS TO DOWNLOAD THE DATA





for strid in idlist:
    i += 1
    root = ''
    abstract = ''
    keywords = []
    row_each = {}
    authdetails = {}
    print(strid)
    row_each['id'] = strid
    strid = urllib.request.quote(str(strid))
    try:
        address = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&api_key=cb261cb142b6b0ca2eaae19a102da3716608&id="+ strid +"&retmode=xml"
        uh = urllib.request.urlopen(address, context = ctx)
        data = uh.read()
    except urllib.error.HTTPError:
        pass
        
    root = et.fromstring(data)
    
    #print(data)
    
#extraction of doi from the xml doc
    try:
        for id in root.iter(tag = 'ELocationID'):
            if id.get('EIdType') == "doi":
                DOI = id.text
                row_each['doi'] = DOI
                #print(df)
        
        #row_each.append(DOI)
        #print(row_each)
    except:
        DOI = ''
        row_each.append(DOI)
        row_each['doi'] = DOI
        #print(row_each)
        
#extraction of keywords from the xml doc
    try:
        for kw in root.iter('Keyword'):
            keywords.append(kw.text)
        
        #row_each.append(keywords)
        row_each['keywords'] = str(keywords)
        
        #print(df)
    except:
        keywords = []    
        #row_each.append(keywords)
        row_each['keywords'] = keywords

#journal title
    try:
        for jt in root.iter('Title'):
            journal_title = jt.text
        
        #row_each.append(journal_title)
        row_each['journaltitle'] = journal_title
        #print(row_each)
    except:
        row_each['journaltitle'] = ''

#Abstract
    try:    
        for abst in root.iter(tag = 'AbstractText'):
            abstract += abst.text
        
        #row_each.append(abstract)
        row_each['Abstract'] = abstract
        #print(row_each)
    except:
        abstract = ''
        #row_each.append(abstract)
        row_each['Abstract'] = abstract

#ArticleTitle  
    try:
        
        for t in root.iter('ArticleTitle'):
            article_title = t.text
            #row_each.append(article_title)
            #print(row_each)
            row_each['ArticleTitle'] = article_title
    
    except:
        row_each['ArticleTitle'] = ''

#Article ID
    # try:
    #     for pubmedarticle in root.iter(tag = 'ArticleId'):
    #         text = pubmedarticle.text
    #         attrib = pubmedarticle.attrib
            
    #         #print(text, attrib)
    # except:
    #     text = ''
    #     attrib = ''

#Volume Issue and Publication Date
    for j_issue in root.iter(tag = 'JournalIssue'):
        try:
            volume = j_issue.find('Volume').text
        except:
            volume = ''
        
        try:
            issue = j_issue.find('Issue').text
        except:
            issue = ''
        
        try:
            for date1 in j_issue.iter(tag = 'PubDate'):
                year = date1.find('Year').text
                month = date1.find('Month').text
        except:
            year = ''
            month =''
        #print(volume, issue, year, month)
        #row_each.append(volume)
        row_each['volume'] = volume
        #row_each.append(issue)
        row_each['issue'] = issue
        #row_each.append(month+year)
        row_each['publication_date'] = month+year
        #print(row_each)


#Author and Affiliation    
    try:
        for auth in root.iter(tag = 'Author'):
            fname = auth.find('ForeName').text
            lname = auth.find('LastName').text
            name = fname + lname
            for affn in auth.iter('AffiliationInfo'):
                affiliation = affn.find('Affiliation').text
            authdetails[name] = affiliation
            
        #row_each.append(authdetails)
        row_each['authdetails'] = str(authdetails)
        #print(authdetails)
    except:
        fname = ''
        lname = ''
        affiliation = ''
        row_each['authdetails'] = str(authdetails)

    df = pd.concat([df, pd.DataFrame(row_each, index = [i])], ignore_index=True)

    
    

    
    

    

        

    


    
    
    

    
