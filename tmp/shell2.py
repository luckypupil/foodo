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

def scrape_html(base_url,url_ext='search.cfm?facType=7&subType=Any&',pg_num=1,num_of_pgs=50,zipcd='',filenm='rest_list.html'):#'facType=7&subType=Any' filters listing to restuarant subcategory
    ###Given key search parameters and the number of pages to scrape, this program looks up the appropriate result(s) pages for inspection listings, goes to each of the restaurants on that page and compiles a dictionary of all the pertinent inspection information in the format {'Name': {'Inspections': {Date: [comments,]}},{'location':{'street':address},{'zip':zipcode}}}###
    
    Master_Rest_dict ={}
          
    mydir =  os.getcwd()
    inspect_file_list = os.listdir(mydir+'/htmlArchive')
        
    for html in inspect_file_list:
        sngl_rest_dict = {}
        inspect_soup = BeautifulSoup(open('htmlArchive/'+html),"html.parser",parse_only=SoupStrainer('body')) #Strain to only take body of html and exclude opening JS
          

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







