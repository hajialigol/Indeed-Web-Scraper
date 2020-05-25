from bs4 import BeautifulSoup
import requests

# Define internship urls per page (10 per page)
page_one_job_url = "https://www.indeed.com/jobs?q=Data%20Science%20Intern&jt=internship&vjk=fb4fccb032904ab4"

# Create BeautifulSoup objects of each of the urls
page_one_job_soup = BeautifulSoup(requests.get(page_one_job_url).content)

# Get the Internship Title
h2 = page_one_job_soup.find("h2", class_="title")
dirty_title = h2.a.text
clean_title = dirty_title.replace("\n", "")

# Get the Company Name
sjcl = page_one_job_soup.find("div", class_="sjcl")
company_name = sjcl.span.text.replace("\n", "")

# Find the Rating
ratingsDisplay = sjcl.find("span", "ratingsDisplay")
rating = float(ratingsDisplay.span.text.replace("\n", ""))

# Find the Location 
job_location = sjcl.find("div", class_="location accessible-contrast-color-location")
location = job_location.text