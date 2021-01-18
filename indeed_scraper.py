import requests
import pandas as pd
from datetime import date
from bs4 import BeautifulSoup as bs
from emailer import email_file

today = date.today()


def extract(start, location="Huntsville, AL", query="software engineer"):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/87.0.4280.141 Safari/537.36"
    }

    url = f"https://www.indeed.com/jobs?q={query}&l={location}&start={start}"
    r = requests.get(url, headers)
    soup = bs(r.content, "lxml")
    return soup


def transform(soup):
    divs = soup.find_all('div', class_="jobsearch-SerpJobCard")

    for job in divs:
        title = job.find('a').text.strip()
        company = job.find('span', class_="company").text.strip()
        summary = job.find('div', {'class': 'summary'}
                           ).text.strip().replace("\n", '')

        try:
            salary = job.find('span', class_="salaryText").text.strip()
        except:
            salary = "Not Listed"

        job = {
            "title": title,
            "company": company,
            "summary": summary,
            "salary": salary,
        }

        joblist.append(job)
    return


joblist = []

for i in range(0, 40, 10):
    print(f"Getting page {round((i / 10) + 1)}")
    c = extract(i)
    transform(c)

df = pd.DataFrame(joblist)

print(df.head())
df.to_csv('jobs.csv')

# Email list of jobs
options = {
    'attachments': ["jobs.csv"],
    'subject': f"List of jobs for {today}",
    'content': """
    Here is the list of jobs for today:
    
        - Python Bot 
    """,
}

email_file(options=options)
