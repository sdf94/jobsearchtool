import logging

# create logger
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(module)s: %(message)s',
                                  datefmt='%m/%d/%Y %H:%M:%S'   )        
fh = logging.FileHandler('jobsearch/jobsearch/logs/jobsearch.log')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.INFO)

class search_url():
    def __init__(self,base_url,city,job,page):
        self.base_url = base_url
        self.city = city
        self.job = job
        self.page = page
        self.logger = logging.getLogger('jobsearch.search_url')
        fh = logging.FileHandler('logs/jobsearch.log')
        self.logger.addHandler(fh)
        
    def indeed_url(self):
        self.url = str(self.base_url+self.job+'&l='+self.city+'&start='+str(self.page))
        self.logger.info(self.url)
        return self.url
    
    def monster_url(self):
        self.url = str(self.base_url+'q='+self.job+'&where='+self.city+'&page='+str(self.page))
        self.logger.info(self.url)
        return self.url
    
    def ziprecruiter_url(self):
        self.url = str(self.base_url+'search='+self.job+'&location='+self.city+'&page='+str(self.page))
        self.logger.info(self.url)
        return self.url