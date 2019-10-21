from jobsearch.jobsearch.searchurl import search_url
import logging
import json

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(module)s: %(message)s',
                                  datefmt='%m/%d/%Y %H:%M:%S'   )        
fh = logging.FileHandler('jobsearch/jobsearch/logs/jobsearch.log')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.INFO)

with open('config.json') as config_file:
    credentials = json.load(config_file)

def get_html(url): 
        from bs4 import BeautifulSoup
        import requests
        global credentials
        """Issue a get request on the inputted URL and parse the results.  
        Issue a get request on the inputted `url`, and then parse the content using
        BeautifulSoup. 
        Args: 
        ----
            url: str

        Returns: 
        ------
            soup: bs4.BeautifulSoup object
        """

        try: 
            if 'monster' in url:
                response = requests.get(url,auth=(credentials['Monster']['username'], credentials['Monster']['password']))
            else:
                response = requests.get(url)
            good_response = check_response_code(response)
            if not good_response: 
                logging.debug('Bad URL: {}'.format(url))
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        except Exception as e: 
            print(e)
            error = "Error in contacting the URL - check that it is a valid URL!"
            raise RuntimeError(error)

def check_response_code(response): 

    """Check the response status code. 
        Args: 
        ----
            response: requests.models.Response
        Returns: bool
        """

    status_code = response.status_code
    if status_code == 200: 
        return True
    else: 
        logging.debug("Status code is not 200, it's {}".format(status_code))
        return False