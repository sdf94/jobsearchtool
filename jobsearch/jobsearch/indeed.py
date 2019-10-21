def indeed(base_url,job_location,job_title,page):
    import pandas as pd
    from jobsearch.jobsearch.searchurl import search_url
    from jobsearch.jobsearch.html import get_html
    """Issue a get request on the inputted URL and parse the results from indeed.com.  
        Args: 
        ----
            base_url: str
            job_location: str
            job_title: str
            page: int

        Returns: 
        ------
            dataframe: list of jobs
        """
    url = search_url(base_url,job_location,job_title,page).indeed_url()
    soup = get_html(url)
    results = soup.find('table', id="pageContent")
    jobs = results.findAll('div', class_="row", attrs={'data-tn-component': 'organicJob'})
    jobs_list = []

    for job in jobs:

        # Each posting can have some missing fields, which leads to attribute errors when parsing that field
        # Catch on a case-by-case basis so we don't discard the entire posting
        try:
            title = job.find('a', attrs={'data-tn-element': 'jobTitle'}).text.strip()
        except AttributeError:
            title = 'Unknown'
        try:
            company = job.find('a', attrs={'data-tn-element': 'companyName'}).text.strip()
        except AttributeError:
            company = 'Unknown'
        try:
            location = job.find('span', class_='location').text.strip()
        except AttributeError:
            location = 'Unknown'
        try:
            summary = job.find('div', attrs={'class': 'summary'}).text.strip()
        except AttributeError:
            summary = 'Unknown'
        try:
            link = "https://www.indeed.com" + job.find('a', attrs={'data-tn-element': 'jobTitle'}).get('href')
        except AttributeError:
            link = 'Unknown'

        jobs_list.append({'title': title, 'company': company, 'location': location, 'summary': summary, "link": link})

    return pd.DataFrame.from_records(jobs_list)
    