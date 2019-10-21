import requests, os, json, time, argparse, threading, urllib
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_job(result):
    from pandas.io.json import json_normalize
    try: 
        address = result['jobLocation']['address']['addressLocality']+' , '+result['jobLocation']['address']['addressRegion']
        return json_normalize({'title': result['title'], 'company': result['hiringOrganization']['name'], 'location': address, 'summary': result['description'], "link": result['FinalURL']})
    except:
        return json_normalize({'title': [''], 'company': [''], 'location': 'no city , no state', 'summary': [''], "link": result['FinalURL']})

def getListing(pages,job,level):
    import pandas as pd
    import time
    page = 1
    jobListings = []
    contentURL = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=' + job + "&jobType=" + level
    while (page <= pages): 
        jl = {}
        webPage = requests.get(contentURL, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
        if (page == 1):
            try:
                pageUrl = str(webPage.content.decode("utf-8").split("untranslatedUrl' : '")[1].split('.htm')[0])
            except:
                time.sleep(1000)
                pageUrl = str(webPage.content.decode("utf-8").split("untranslatedUrl' : '")[1].split('.htm')[0])
            
            
        contentURL = pageUrl +'_IP'+ str(page + 1) + '.htm?jobType=' + level
    
        soup = BeautifulSoup(webPage.content, 'html.parser')
        soup = soup.select('span[data-job-id]')
        for span in soup:
            jl = {"jobID":span['data-job-id']}
            jobListings.append(jl)
        
        page += 1
    results = getRealURL(jobListings)
    return pd.concat([create_job(x) for x in results])

def getRealURL(jobListings):
    for line in jobListings:
        jobID = line['jobID']
        line['url'] = "https://www.glassdoor.com/partner/jobListing.htm?jobListingId="+jobID
        try:
            page = requests.get(line['url'], headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
            line['FinalURL'] = page.url
        except:
            line['FinalURL'] = ""
        line['url'] = "https://www.glassdoor.com/job-listing/JV.htm?jl="+jobID
    
    return [gatherJob(jobListing) for jobListing in jobListings]

def gatherJob(listing):
    page = requests.get(listing['url'], headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}, verify=False)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        soup = str(soup).split('<script type="application/ld+json">')[1].split('</script>')[0].replace("&lt;","<").replace("&gt;",">").replace("\n","").replace("\r","")
        listingJSON = json.loads(soup)
        listingJSON['FinalURL'] = listing['FinalURL']
        return(listingJSON)
    except Exception:
        return {'FinalURL': listing['url'],'hiringOrganization':['None'],'title':['None'],'description':['None'],'jobLocation':['None']}

