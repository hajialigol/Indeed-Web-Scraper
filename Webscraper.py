import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Arrays needed for webscraping
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
        

# Finding job postings
def job_title(job_soup_object):
    for job in job_soup_object:
        potential_title = job.find("h2", class_="title")
        potential_link = potential_title.href
        if potential_title:
            title = potential_title.text.replace("\n", "")
        else:
            title = "N/A"
        title_list.append(title)
    
# Finding job link
def job_link(job_soup_object):
    for job in job_soup_object:
        potential_link = job.find_all("a", href=True)[0]
        if potential_link:
            link = "https://www.indeed.com" + potential_link["href"]
            url_list.append(link)
        else:
            url_list.append("N/A")
        
# Finding company name
def job_company(job_soup_object):
    for job in job_soup_object:
        potential_company_tag = job.find("span", class_="company")
        if potential_company_tag:
            company = potential_company_tag.text.replace("\n", "")
        else:
            company = "N/A"
        company_list.append(company)
    
# Find job locations
def job_location(job_soup_object):
    for job in job_soup_object:
        potential_location = job.find("div", class_="recJobLoc")["data-rc-loc"]
        if potential_location:
            location = potential_location
        else:
            location = "N/A"
        location_list.append(location)
    
# Find job ratings
def job_rating(job_soup_object):
    for job in job_soup_object:
        potential_rating = job.find("span", class_="ratingsContent")
        if potential_rating:
            rating = float(potential_rating.text.replace("\n", ""))
        else:
            rating = None
        ratings_list.append(rating)
    
# Find job summaries
def job_summaries(job_soup_object):
    for job in job_soup_object:
        job_summary_placeholder = []
        li_list = job.find_all("li")
        for li in li_list:
            job_summary_placeholder.append(li.text)
        job_summary.append("".join(job_summary_placeholder))  

# Create data frame
def create_dataframe(title_list=title_list, company_list=company_list,
                    job_summary=job_summary, ratings_list=ratings_list,
                    location_list=location_list, url_list=url_list):
    
    df = pd.DataFrame({'Job Title' : title_list, 'Company' : company_list, 
                              'Summary' : job_summary, 'Rating' : ratings_list,
                              'Location' : location_list, 'URL' : url_list}) 
    return df

# Create and save data frame
def clean_df_and_save(dataframe):
    df = dataframe.drop_duplicates(subset = ["Job Title", "Company", "Rating", "Location"],
                                    keep='first')
    df.to_excel("Job_Postings.xlsx")
    
# This method returns a data frame of all pages from a list of pages
def job_data_scrapper(page_list):
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

# Create data frame from list of pages 
dataframe = job_data_scrapper(page_list)

# Clean the data frame
clean_df_and_save(dataframe)    
