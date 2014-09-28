#!/usr/bin/python
import datetime
import re
import requests
import csv
import os
from pprint import pprint
from bs4 import BeautifulSoup, SoupStrainer
from app import db
from app.models import Rest, Comment
from app.helper import makeSlug, get_grade
from math import ceil

base_url = 'http://philadelphia.pa.gegov.com/philadelphia/' 

def getLatestDate():
    latestDate = db.session.query(Comment.date).order_by(Comment.date.desc()).first()[0]
    return latestDate.strftime('%m/%d/%Y')

def scrapeHTMLinks(startdate,enddate):
    ###Scrapes HTML pages based on search params and returns list of links to search results pgs. ###
    print '####   Entering scrapehtml   ####'
    url_ext='search.cfm?facType=7&subType=Any&'
    init_query = '{}start=1&sd={}&ed={}&dtRng=YES'.format(url_ext,startdate,enddate)
    print 'start, end dates are {} and {}, respectively'.format(startdate,enddate)
    print 'query is {}'.format(init_query)
    init_url = base_url + init_query
    
    r = requests.get(init_url)
    match = re.search(u'(\d+) Facilities matched', r.text)
    totsresults = float(match.group(1))
    pgresults_num = int(ceil(totsresults / 20))
    print 'There are {} results pgs'.format(pgresults_num)
    
    linkext_list = [] 
    for num in xrange(1,1+pgresults_num):
        print 'Preparing results page {}'.format(num)
        if not startdate and enddate:
            print "start and end dates must be specified"
        else:
             #'facType=7&subType=Any' filters to restuarant subcat
            start_query = (1 if num == 1 else (num-1)*20+1) # converts page results num to search query param
            srch_query = '{}start={}&sd={}&ed={}&dtRng=YES'.format(url_ext,start_query,startdate,enddate)
     
        try:
            r = requests.get(base_url + srch_query)
            soup = BeautifulSoup(r.text)
            def a_scrub(href):
                return href is not None and 'estab' in href and 'inspection' not in href 
            listing = soup.find_all(href=a_scrub) 
            for link in listing:
                linkext_list.append(str(link['href']))
        except:
            continue
	
	print '####   Exiting scrapehtml   ####'
    return (linkext_list)

def makeHtmlRepo (ext_list):
    ### Returns python list of htmlresults pages as text###
    html_list = []
    lnk_ct = len(ext_list)
    print '####  Entering makeHTMLRepo.  There are {} links  ####'.format(lnk_ct)
    i = 1
    for ext in ext_list:
        try:
            r = requests.get(base_url+ext)
            html_list.append(r.text.encode('utf-8','ignore').strip())
            print 'got link {} of {}'.format(i,lnk_ct)+base_url+ext
            i+=1    
        except:
            continue
    
    print '####   Exiting makehtmlrepo   ####'	
    return (html_list)
                     
def Make_rest_rows(html,startdt,enddt):
    #returns tuple of 1 rest row [name,street,zip], and all comment rows [name,date,code,quote] after the start date param#    
    print '####   Entering Make_rest_rows   ####'
    startdt= datetime.datetime.strptime(startdt.strip(),'%m/%d/%Y')
    enddt= datetime.datetime.strptime(enddt.strip(),'%m/%d/%Y')      
    sngl_rest_dict = {}
    inspect_soup = BeautifulSoup(html,"html.parser",parse_only=SoupStrainer('body')) #Strain to body          
    rest_row =[]
    Rest_nm = inspect_soup('b',style="font-size:14px;")[0].string
    print 'parsing info for {}'.format(Rest_nm)
    
    try:
        Rest_st = inspect_soup('i')[0].contents[0].encode('utf-8','ignore').strip()
        Rest_zip_temp = inspect_soup('i')[0].contents[2].encode('utf-8','ignore').strip()[-5:]
        Rest_zip = (int(Rest_zip_temp) if len(Rest_zip_temp)==5 else "") #verify zip is 5 digit int
        rest_row = [Rest_nm,Rest_st,Rest_zip]
    except:
        return([],[])
            
    inspections =  inspect_soup.find_all('div',style='border:1px solid #003399;width:95%;margin-bottom:10px;')  #Main division for all inspect summary info 
    inspect_hist = [ ]
    for inspection in inspections:# loops over each date on rest profile page#
        date = inspection.select('div[style="padding:5px;]')[0].contents[2].encode('utf-8','ignore').strip()
        try:
            date = datetime.datetime.strptime(date,'%m/%d/%Y')
            results =  inspection.find_all('div',style='background-color:#EFEFEF;padding:5px;')
            for content in results:
                if date >= startdt and date <= enddt and content.contents:
                    for result in content.contents:
                        newComment = str(result.encode('utf-8','ignore').strip()) #Convert unicode to utf-8
                        m = re.search(r"(\d+)[-\s]+([\w\W]+)",newComment)
                        if m is not None:
                            comment_row = [Rest_nm,date,m.group(1),m.group(2)]
                            inspect_hist.append(comment_row)
        except:
            continue
   
    print '####   Entering Make_rest_rows   ####'
    return(rest_row,inspect_hist)
    
def geoCode(rest):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
    if rest.street:
            street = rest.street.replace('#','')
            geo_str = makeSlug(street)    
            address = geo_str+"+Philadelphia,+PA+"+str(rest.zipcd)
            key = "AIzaSyDZTlXL-J2h0DQO0CVDpXbtKOtn_TTCZTU"
            final_url = base_url+"sensor=false"+"&address="+address+"&key="+key    
            try:
                r = requests.get(final_url) 
                myobject =  r.json()
                numResults = len(myobject["results"])        
                if myobject['status'] == "OK" and numResults <= 4:
    #               print 'pulled succesfully from goog with {} elements - thx Serg!'.format(numResults)
                    rest.lat = myobject["results"][0]["geometry"]["location"]["lat"]
                    rest.lng = myobject["results"][0]["geometry"]["location"]["lng"]
            except:
                rest.lat,rest.lng = '0','0'
    return(rest.lat,rest.lng)
  
def addtodb(table_tup):
   ###Copies CSV files to create resturant and comment tables###
   print '####   Entering addtodb   ####'
   if table_tup[0]:
        try:
            rest_row = table_tup[0]
            name, street, zipcd = str(rest_row[0]), str(rest_row[1]), rest_row[2]
            if not db.session.query(Rest).filter(Rest.name==name).first():
                try:
                    newRest = Rest(name=name,street=street,zipcd=zipcd)
                    newRest.lat,newRest.lng = geoCode(newRest)
                    db.session.add(newRest)
                    db.session.commit()
                    print '{} added to Rest table'.format(name)
                except:
                    print '{} not added to Rest Table'.format(name)
                    db.session.rollback()
                    
            else:
                print '{} already in rest table'.format(name)    
                
        except:
            print "rest _row for {} didnt work".format(rest_row[0])
   else:
       print 'nothing in current rest_row'         
   
   if table_tup[1]:# accoutn for inspection listings with no data
        try:
            for comment_row in table_tup[1]:
                restnm, date, code, quote = str(comment_row[0]), comment_row[1], int(comment_row[2]),str(comment_row[3])
                if not db.session.query(Comment).filter(Comment.restnm==restnm,Comment.date==date,Comment.quote==quote).first():
                    try:
                        newComm = Comment(restnm=restnm,date=date,code=code,quote=quote)
                        db.session.add(newComm)
                        db.session.commit()
                        print '{} comment w/ code:{} added to Comment Table!'.format(restnm,code)
                    except:
                        print 'comment for {} not added.'.format(restnm,code)
                        db.session.rollback()

            rest = db.session.query(Rest).filter(Rest.name == restnm).first()
            grade = get_grade(rest.getPts())
            rest.grade = grade
            db.session.add(rest)
            db.session.commit()
            print 'Grade for {} updated'.format(restnm)


        except:
            pprint ("comment for {} didnt work".format(rest_row[0]))
        
   else:
       print 'nothing in current Comment_hist'           

   print '####   Exiting addtodb   ####'
def main():
    ###Need to enter number of page results matching start/end dates specified###
    startdate = getLatestDate()
    startdate = '08/07/2014'
    enddate = datetime.date.today().strftime('%m/%d/%Y')
    for html in makeHtmlRepo(scrapeHTMLinks(startdate,enddate)):
        addtodb(Make_rest_rows(html,startdate,enddate))

if __name__ == "__main__":
    main()
    




