import logging
import argparse
import os
from time import time
from jobsearch.jobsearch.jobboard import pull_data

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
# Create target directory & all intermediate directories if don't exists
dirName = 'logs'
if not os.path.exists(dirName):
    os.makedirs(dirName)
    logger.debug("Directory created ")
else:    
    logger.debug("This directory already exists")    
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(module)s: %(message)s',
                                  datefmt='%m/%d/%Y %H:%M:%S'   )        
fh = logging.FileHandler('jobsearch/jobsearch/logs/jobsearch.log')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.INFO)


logger.info("The original code came from: https://github.com/msalmon00/Portfolio/blob/master/Indeed-Job-Scraper-Analysis-and-Salary-Predictions.ipynb")

def main():
    keywords = 'data%20python'
    cities = 'USA'
    jobboards= 'All'
    pages = 1
    logger.info('Keywords are %s',keywords)
    logger.info('Cities are %s',cities)
    logger.info('Pages value is %s',pages)
    logger.info('Jobboards to search are %s',jobboards)
    print(pull_data(keywords,cities,jobboards,pages))
    
if __name__ == '__main__':
    main()
