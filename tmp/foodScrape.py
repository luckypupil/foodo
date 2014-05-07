#!/usr/bin/python
import datetime
import re
import requests
import csv
import os
from pprint import pprint
from bs4 import BeautifulSoup, SoupStrainer

base_url = 'http://philadelphia.pa.gegov.com/philadelphia/' 

def scrapeHTMLinks(base_url,pg_num=1,num_of_pgs=302):
    ###Scrapes HTML pages based on search params and returns list of links to overview pages. ###
    url_ext='search.cfm?facType=7&subType=Any&' #'facType=7&subType=Any' filters to restuarant subcat
     
    link_list = []
    for num in xrange(pg_num,pg_num+num_of_pgs):
        ###Scrape URL of list of restaurants associated with given search query params (resultspg and zip) and writes to html file###
        print 'Generating restaurant index results for page num {}'.format(num)
        start_query = (1 if num == 1 else (num-1)*20+1) # converts page results num to search query param
        srch_query = '{}start={}'.format(url_ext,start_query)
         
        try:
            r = requests.get(base_url + srch_query)
            with open('tmp.html','w') as f:
                f.write(r.text)
        except:
            with open('ErrorLog.txt', 'w') as myfile:
                myfile.write('couldnt create tmp file for results page {}'.format(num))
            continue
             
        soup = BeautifulSoup(open('tmp.html'))
         
        def a_scrub(href):
            return href is not None and 'estab' in href and 'inspection' not in href 
         
        listing = soup.find_all(href=a_scrub) 
         
        for link in listing:
            link_list.append(str(link['href']))
        
    try:
        with open('linkList.txt', 'w') as f:
            for link in link_list: 
                f.write(link)
    except:
        pass
    
    return (link_list)

def makeHtmlRepo (linkList):
        ###Takes url list and creates repo of all pages in list###
        print 'Creating html Repo'
        for linkExt in linkList:
            try:
                r = requests.get(base_url+linkExt)
                flname = linkExt+'.html'
                with open('htmlArchive/' + flname, 'wb') as html:
                    html.write(r.text.encode('utf-8','ignore').strip())
                print linkExt+'added to Repo'    
            except:
                with open('ErrorLog.txt', 'w') as myfile:
                    myfile.write('Couldnt create html file for {}'.format(linkExt))
                continue
            
def Make_master_dict():    
    Master_Rest_dict ={}
    mydir =  os.getcwd()
    inspect_file_list = os.listdir(mydir+'/htmlArchive')
        
    for html in inspect_file_list:
        sngl_rest_dict = {}
        inspect_soup = BeautifulSoup(open('htmlArchive/'+html),"html.parser",parse_only=SoupStrainer('body')) #Strain to body          
        
        try:
            Rest_nm = inspect_soup('b',style="font-size:14px;")[0].string
        except:
            with open('ErrorLog.txt', 'w') as myfile:
                    myfile.write('{} did not parse properly'.format(html))
            continue
        
        try:
            Rest_st = inspect_soup('i')[0].contents[0].encode('utf-8','ignore').strip()
            Rest_zip_temp = inspect_soup('i')[0].contents[2].encode('utf-8','ignore').strip()[-5:]
            Rest_zip = (int(Rest_zip_temp) if len(Rest_zip_temp)==5 else "") #verify zip is 5 digit int
             
            sngl_rest_dict['location'] = {'street':Rest_st,'zip':Rest_zip} 
            inspections =  inspect_soup.find_all('div',style='border:1px solid #003399;width:95%;margin-bottom:10px;')  #Main division for all inspect summary info 
            inspec_hist = {}
            for inspection in inspections:
                date = inspection.select('div[style="padding:5px;]')[0].contents[2].encode('utf-8','ignore').strip()
                results =  inspection.find_all('div',style='background-color:#EFEFEF;padding:5px;')
                resultz = []
                for content in results:
                    for result in content.contents:
                        newComment = str(result.encode('utf-8','ignore').strip()) #Convert unicode to utf-8
                        if newComment not in resultz:
                            resultz.append(newComment) 
                     
                inspec_hist[date] = resultz          
                  
            sngl_rest_dict['inspections'] = inspec_hist
            print 'done with {}'.format(Rest_nm)
        except:
            with open('ErrorLog.txt', 'w') as myfile:
                    myfile.write('{} did not parse properly'.format(Rest_nm))
            continue  
          
            
        Master_Rest_dict[str(Rest_nm)] = sngl_rest_dict
        
                    
    return (Master_Rest_dict)

def dict_to_txt(restInspectDict):
    ###converts dict to 2 CSVs: 1) Rest table (Fields: Name, Street, Zip) & 2) Comments Table (Fields: Name, Date, comment,code )###
    
    # Create Rest table#
    print "Creating 'Restuarant' table"
    resttbl_list = []
    for rest in restInspectDict:
        try:
            rest_row = [rest,restInspectDict[rest]['location']['street'],restInspectDict[rest]['location']['zip']]
            resttbl_list.append(rest_row) 
        except:
            with open('ErrorLog.txt', 'w') as myfile:
                    myfile.write('{} was not added to Rest Table'.format(rest))
            continue
        
    with open('csv/rest_tbl.csv','wb') as csvfile:
        w = csv.writer(csvfile, delimiter=',')
        w.writerows([i for i in resttbl_list])
    
    # Create Comments table#
    print "Creating 'Comments' table"
    inspect_list = []
    for restnm in restInspectDict:
        try:
            for dated in restInspectDict[restnm]['inspections']:
                for comment in restInspectDict[restnm]['inspections'][dated]:
                    m = re.search(r"(\d+)[-\s]+([\w\W]+)",comment) # Will need to test regex on more complete data set.  Sure there are still exceptions here
                    
                    if m is not None:
                        insp_str =  [restnm,datetime.datetime.strptime(dated.strip(),'%m/%d/%Y'),m.group(1),m.group(2)] #Name, Date,code,quote
                        inspect_list.append(insp_str)
        except:
            with open('ErrorLog.txt', 'w') as myfile:
                    myfile.write('{} was not added to Comments Table'.format(restnm))
            continue
            
    with open('csv/comment_tbl.csv','wb') as csvfile:
        w = csv.writer(csvfile, delimiter=',')
        w.writerows([i for i in inspect_list])       
        
        
if __name__ == "__main__":
    
    #makeHtmlRepo(scrapeHTMLinks(base_url))
    dict_to_txt(Make_master_dict())
  






