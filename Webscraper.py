import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

title_list = []
company_list = []
ratings_list = []
location_list = []
job_summary = []
url_list = []

# Define internship urls per page (10 per page)
page_one_job_url = "https://www.indeed.com/jobs?q=Data%20Science%20Intern&jt=internship&vjk=fb4fccb032904ab4"

# Create BeautifulSoup objects of each of the urls
page_one_job_soup = BeautifulSoup(requests.get(page_one_job_url).content)

# Create column section
column_data = page_one_job_soup.find("td", id="resultsCol")

# Extract job data section from column
job_data = column_data.find_all("div", class_=re.compile("jobsearch-SerpJobCard unifiedRow row"))

# Finding Job Postings
for job in job_data:
    potential_title = job.find("h2", class_="title")
    potential_link = potential_title.href
    if potential_title:
        title = potential_title.text.replace("\n", "")
    else:
        title = "N/A"
    title_list.append(title)
    
# Finding Job Link
for job in job_data:
    potential_title = job.find("h2", class_="title")
    potential_link = job.find_all("a", href=True)[0]
    if potential_link:
        link = "https://www.indeed.com" + potential_link["href"]
        url_list.append(link)
    else:
        url_list.append("N/A")
        
# Finding Company Name
for job in job_data:
    potential_company_tag = job.find("span", class_="company")
    if potential_company_tag:
        company = potential_company_tag.text.replace("\n", "")
    else:
        company = "N/A"
    company_list.append(company)
    
# Find Job Locations
for job in job_data:
    potential_location = job.find("div", class_="recJobLoc")["data-rc-loc"]
    if potential_location:
        location = potential_location
    else:
        location = "N/A"
    location_list.append(location)
    
# Find Job Ratings
for job in job_data:
    potential_rating = job.find("span", class_="ratingsContent")
    if potential_rating:
        rating = float(potential_rating.text.replace("\n", ""))
    else:
        rating = None
    ratings_list.append(rating)
    
# Find Job Summaries
for job in job_data:
    job_summary_placeholder = []
    li_list = job.find_all("li")
    for li in li_list:
        job_summary_placeholder.append(li.text)
    job_summary.append("".join(job_summary_placeholder))  

# Create DataFrame
dataframe = pd.DataFrame({'Job Title' : title_list, 'Company' : company_list, 
                          'Summary' : job_summary, 'Rating' : ratings_list,
                          'Location' : location_list, 'URL' : url_list})    

# Save DataFrame
dataframe.to_excel("Job_Postings.xlsx")