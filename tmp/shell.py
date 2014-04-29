#!/usr/bin/python
import datetime
import re
import requests
import csv
import os
from pprint import pprint
from bs4 import BeautifulSoup, SoupStrainer

base_url = 'http://philadelphia.pa.gegov.com/philadelphia/' # base url for Philly inspection site.  
 
def calc_pg_num(resultsnum):
    ###converts results page number to search query num###
        return (1 if resultsnum == 1 else (resultsnum-1)*20+1)

def dict_to_txt(from_dict):
    ### Takes dictionary of restaurant inspection information and converts to 2 different CSV files: 1) Restuarant table (Fields: Name, Street, Zip) and 2)Inspections Table (Fields: Name, Date of insepction, comment, comment code )###
    
    # Create 'Restuarants' table#
    print "***Creating 'Restuarant' table***"
    resttbl_list = []
    for rest in from_dict:
        rest_row = [rest,from_dict[rest]['location']['street'],from_dict[rest]['location']['zip']]
        resttbl_list.append(rest_row) 

    with open('rest_tbl.csv','wb') as csvfile:
        w = csv.writer(csvfile, delimiter=',')
        w.writerows([i for i in resttbl_list])
    
    # Create 'Comments/Insepctions' table#
    print "***Creating 'Comments' table***"
    inspect_list = []
    for restnm in from_dict:
        for dated in from_dict[restnm]['inspections']:
            for comment in from_dict[restnm]['inspections'][dated]:
                m = re.search(r"(\d+)[-\s]+([\w\s]+)",comment) # Will need to test regex on more complete data set.  Sure there are still exceptions here
                
                if m is not None:
                    insp_str =  [restnm,datetime.datetime.strptime(dated.strip(),'%m/%d/%Y'),m.group(1),m.group(2)] #Name, Date,code,quote
                    inspect_list.append(insp_str)
        
    with open('comment_tbl.csv','wb') as csvfile:
        w = csv.writer(csvfile, delimiter=',')
        w.writerows([i for i in inspect_list])       

def scrape_html(base_url,url_ext='search.cfm?facType=7&subType=Any&',pg_num=2,num_of_pgs=1,zipcd='',filenm='rest_list.html'):
    ###Scrapes HTML pages based on search params and returns list of links to overview pages. 'facType=7&subType=Any' filters to restuarant subcat###
     
    for num in xrange(pg_num,pg_num+num_of_pgs):
        ###Scrape URL of list of restaurants associated with given search query params (resultspg and zip) and writes to html file###
        print '***Generating restuarant index results for page num {}***'.format(num)
        start_query = calc_pg_num(num) # converts page results num to search query param
        srch_query = '{}start={}&zc={}'.format(url_ext,start_query,zipcd)
        r = requests.get(base_url + srch_query)
        f = open(filenm,'w')
        print "***Writing index results to 'rest_list.html'***"
        f.write(r.text)
        f.close()    


        ###Takes an html file of restuarant lists and scrubs for relevant links to each restuarant's inpsection report history page 
        ###ie. 'estab.cfm?facilityID=77229900-DB52-36A2-8A651920C80A7A7B'###
        print '***Getting links to inspection overview pages for each restaurant in results list***'
        soup = BeautifulSoup(open('rest_list.html'))
        
        def a_scrub(href):
            return href is not None and 'estab' in href and 'inspection' not in href 

        listing = soup.find_all(href=a_scrub) 

        link_list = []
        for link in listing[3:6]: #!!!Remove SPlice once code is completed!!!
            link_list.append(str(link['href']))
        
        return link_list

def makeHtmlRepo (linkList):
        ###Takes url list and creates repo of all pages in list###
        print '***Scrubbing inspection data for each restaurant on list***'
        for linkExt in linkList:
            r = request.get(base_url+linkExt)
            
        
        
        
        
        
        
        
        
        Master_Rest_dict ={}
        
        for link in link_list:
            sngl_rest_dict = {}
            r = requests.get(base_url + link)


            inspect_soup = BeautifulSoup(r.text,"html.parser",parse_only=SoupStrainer('body')) #Strain to only take body of html and exclude opening JS
            Rest_nm = inspect_soup('b',style="font-size:14px;")[0].string #Restaurant Name
            
            
            Rest_st = inspect_soup('i')[0].contents[0].strip().encode('utf-8') #Restaurant Street
            Rest_zip = inspect_soup('i')[0].contents[2].strip().encode('utf-8')[-5:] #Restaurant zip
            sngl_rest_dict['location'] = {'street':Rest_st,'zip':Rest_zip}
            
            
            inspections =  inspect_soup.find_all('div',style='border:1px solid #003399;width:95%;margin-bottom:10px;')  #Main division for all inspect summary info 
            inspec_hist = {}
            for inspection in inspections:
                date = inspection.select('div[style="padding:5px;]')[0].contents[2].encode('utf-8')
                results =  inspection.find_all('div',style='background-color:#EFEFEF;padding:5px;')
                resultz = []
                for content in results:
                    for result in content.contents:
                        resultz.append(str(result.encode('utf-8').strip()).lower()) #Convert unicode to utf-8
                
                inspec_hist[date] = resultz          
             
            sngl_rest_dict['inspections'] = inspec_hist
            
            Master_Rest_dict[str(Rest_nm)] = sngl_rest_dict
        
        
            
    dict_to_txt(Master_Rest_dict)

if __name__ == "__main__":
    scrape_html(base_url)







