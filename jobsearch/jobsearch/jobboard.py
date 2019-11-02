import pandas as pd
from jobsearch.jobsearch.searchurl import search_url
from jobsearch.jobsearch.indeed import indeed
from jobsearch.jobsearch.glassdoor import getListing
import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(module)s: %(message)s',
                                  datefmt='%m/%d/%Y %H:%M:%S')        
fh = logging.FileHandler('jobsearch/jobsearch/logs/jobsearch.log')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.INFO)

def pull_data(job_title, job_location, job_site,pages):
    """Issue a get request on the inputted URL and parse the results.  
        Args: 
        ----
            job_location: str
            job_title: str
            pages: int

        Returns: 
        ------
            dataframe: a concatenated list of jobs from various jobboards including indeed, monster,ziprecruiter, and glassdoor
        """

    if job_site == 'Indeed':
        base_url = 'http://www.indeed.com/jobs?q='
        results = [indeed(base_url,job_location,job_title,page) for page in range(pages)]
        logger.info(results)
        return results
    elif job_site == 'Glassdoor':
        results = getListing(pages,job_title,'All')
        logger.info(results)
        return results
    else:
        logger.info('Running all jobboards')
        logger.info('Starts with Indeed jobs')
        base_url = 'http://www.indeed.com/jobs?q='
        indeed_results = [indeed(base_url,job_location,job_title,page) for page in range(pages)]
        logger.info('Finally we have glassdoor jobs')
        glassdoor_results = getListing(pages,job_title,'All')
        return pd.concat(indeed_results +[glassdoor_results])