from bs4 import BeautifulSoup
import requests

title_list = []
company_name_list = []
ratings_list = []
location_list = []
description_list = []

# Define internship urls per page (10 per page)
page_one_job_url = "https://www.indeed.com/jobs?q=Data%20Science%20Intern&jt=internship&vjk=fb4fccb032904ab4"

# Create BeautifulSoup objects of each of the urls
page_one_job_soup = BeautifulSoup(requests.get(page_one_job_url).content)

# Create column section
column_data = page_one_job_soup.find("td", id="resultsCol")

# Find Internship Titles
titles = column_data.find_all("h2", class_="title")
for title in titles:
    dirty_title = title.a.text
    clean_title = dirty_title.replace("\n", "")
    title_list.append(clean_title)

# Get the Company Name
company_data_list = column_data.find_all("div", class_="sjcl")
for company_data in company_data_list:
    company_name = company_data.span.text.replace("\n", "")
    company_name_list.append(company_name)

# Find the Rating
ratingsDisplay_list = column_data.find_all("span", "ratingsDisplay")
for ratingsDisplay in ratingsDisplay_list:
    rating = float(ratingsDisplay.span.text.replace("\n", ""))
    ratings_list.append(rating)


# Find the Location
job_location_list = column_data.find_all("span", class_="location accessible-contrast-color-location")
for job_location in job_location_list:
    location = job_location.text
    location_list.append(location)

# Find the Summary
summary_list = column_data.find_all("div", class_="summary")
for summary in summary_list:
    single_summary_description_list = []
    list_item_list = summary.find_all("li")
    for list_item in list_item_list:
        single_summary_description_list.append(list_item.text)
    description_list.append(" ".join(single_summary_description_list))
