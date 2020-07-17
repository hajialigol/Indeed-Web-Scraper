import re
import requests
import pandas as pd
from bs4 import BeautifulSoup


# List of urls to extract data science positions froms
page_list = ["https://www.indeed.com/jobs?q=Data%20Science%20Intern&jt=internship&vjk=fb4fccb032904ab4",
             "https://www.indeed.com/jobs?q=Data%20Science%20Intern&jt=internship&start=10&vjk=af46ec7e37987830",
             "https://www.indeed.com/jobs?q=Data%20Science%20Intern&jt=internship&start=20&vjk=37f09b7cb7585a5e",
             "https://www.indeed.com/jobs?q=Data%20Science%20Intern&jt=internship&start=30&vjk=ddeea8ed81dd7ece",
             "https://www.indeed.com/jobs?q=Data%20Science%20Intern&jt=internship&start=40&vjk=4afb64094060284a",
             "https://www.indeed.com/jobs?q=Data%20Science%20Intern&jt=internship&start=50&vjk=3cdcec6ed30005be"]
title_list = []
company_list = []
ratings_list = []
location_list = []
job_summary = []
url_list = []
        


def job_title(job_soup_object):
    '''
    Desc:
        Given a BeautifulSoup object, this method webscrapes job titles and adds the information to a list of titles.
    Inpt:
        job_soup_object [BeautifulSoup]: BeautifulSoup object that has access to information about job postings.
    '''
    for job in job_soup_object:
        potential_title = job.find("h2", class_="title")
        potential_link = potential_title.href
        if potential_title:
            title = potential_title.text.replace("\n", "")
        else:
            title = "N/A"
        title_list.append(title)
    
    

def job_link(job_soup_object):
    '''
    Desc:
        This method finds the urls of job openings and appends it to a list of urls.
    Inpt:
        job_soup_object [BeautifulSoup]: BeautifulSoup object that has access to information about job postings.
    '''
    for job in job_soup_object:
        potential_link = job.find_all("a", href=True)[0]
        if potential_link:
            link = "https://www.indeed.com" + potential_link["href"]
            url_list.append(link)
        else:
            url_list.append("N/A")


        
def job_company(job_soup_object):
    '''
    Desc:
        Given a BeautifulSoup object, this method extracts the company name. Afterwards, the information is appended
        to a list repesenting company names.
    Inpt:
        job_soup_object [BeautifulSoup]: BeautifulSoup object that has access to information about job postings
    '''
    for job in job_soup_object:
        potential_company_tag = job.find("span", class_="company")
        if potential_company_tag:
            company = potential_company_tag.text.replace("\n", "")
        else:
            company = "N/A"
        company_list.append(company)
    


def job_location(job_soup_object):
    '''
    Desc:
        job_location() appends the location of a list of jobs to a list of locations
    Inpt:
        job_soup_object [BeautifulSoup]: BeautifulSoup object that has access to information about job postings.
    '''
    for job in job_soup_object:
        potential_location = job.find("div", class_="recJobLoc")["data-rc-loc"]
        if potential_location:
            location = potential_location
        else:
            location = "N/A"
        location_list.append(location)
    


def job_rating(job_soup_object):
    '''
    Desc:
        Most of the times, there are ratings for jobs. This method extracts those ratings and appends them to a list.
    Inpt:
        job_soup_object [BeautifulSoup]: BeautifulSoup object that has access to information about job postings.
    '''
    for job in job_soup_object:
        potential_rating = job.find("span", class_="ratingsContent")
        if potential_rating:
            rating = float(potential_rating.text.replace("\n", ""))
        else:
            rating = None
        ratings_list.append(rating)


    
def job_summaries(job_soup_object):
    '''
    Desc:
        job_summaries() webscrapes the description of each job, adding it to a list.
    Inpt:
        job_soup_object [BeautifulSoup]: BeautifulSoup object that has access to information about job postings.
    '''
    for job in job_soup_object:
        job_summary_placeholder = []
        li_list = job.find_all("li")
        for li in li_list:
            job_summary_placeholder.append(li.text)
        job_summary.append("".join(job_summary_placeholder))  



def create_dataframe(title_list=title_list, company_list=company_list,
                    job_summary=job_summary, ratings_list=ratings_list,
                    location_list=location_list, url_list=url_list):
    '''
    Desc:
        This method creates a dataframe given job information.
    Inpt:
        title_list [list]: List of job titles.
        company_list [list]: List of companies of each job.
        job_summary [list]: List of job descriptions.
        ratings_list [list]: List of each job's rating.
        location_list [list]: List of job locations.
        url_list [list]: List of each job's url.
    Oupt:
        A dataframe that contains information about job postings. The information is determined
        by the input lists.

    '''
    
    df = pd.DataFrame({'Job Title' : title_list, 'Company' : company_list, 
                              'Summary' : job_summary, 'Rating' : ratings_list,
                              'Location' : location_list, 'URL' : url_list}) 
    return df



def clean_df_and_save(dataframe, save):
    '''
    Desc:
        This method cleans a given dataframe and saves it to the local directory.
    Inpt:
        dataframe [df]: Dataframe to clean and save.
        save [str]: String dictating if to save the dataframe. To save the dataframe, set 'save = yes'.
    '''
    df = dataframe.drop_duplicates(subset = ["Job Title", "Company", "Rating", "Location"],
                                    keep='first')
    if tolower(save) == 'yes':
        df.to_excel("Job_Postings.xlsx")
    


def job_data_scrapper(page_list):
    '''
    Desc:
        This method performs all operations starting from requesting the data to creating the dataframe.
        It covers most of the functionality of the program.
    Inpt:
        page_list [list]: List of Indeed pages of job postings to webscrape from.

    '''
    for url in page_list:
        title_list = []
        company_list = []
        ratings_list = []
        location_list = []
        job_summary = []
        url_list = []
        url_soup = BeautifulSoup(requests.get(url).content)
        column_data = url_soup.find("td", id="resultsCol")
        job_soup_object = column_data.find_all("div", class_=re.compile("jobsearch-SerpJobCard unifiedRow row"))
        job_title(job_soup_object)
        job_link(job_soup_object)
        job_company(job_soup_object)
        job_location(job_soup_object)
        job_rating(job_soup_object)
        job_summaries(job_soup_object)
        dataframe = create_dataframe()
    return dataframe



if __name__ == '__main__':
    dataframe = job_data_scrapper(page_list)
    clean_df_and_save(dataframe)    
