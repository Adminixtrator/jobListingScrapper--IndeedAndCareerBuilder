import requests
import bs4
from bs4 import BeautifulSoup

# a = input('Job description: ')
# b = input('Location: ')

# URL = "https://www.indeed.com/jobs?q="+str(a.split(' ')[0])+"+"+str(a.split(' ')[1])+"&l="+str(b.split(' ')[0])+"+"+str(b.split(' ')[1])+"&start="
URL = "https://www.indeed.com/jobs?q=data+scientist&l=New+York&start="

def main(URL):
    p = 0
    responseJson = []
    while True and p < 30:
        try: 
            URL = URL + str(p)
            page = requests.get(URL)
            soup = BeautifulSoup(page.text, "html.parser")

            jobs = []
            urls = []
            companies = []
            json = []
            locations = []
            jobPolicy = []
            descriptions = []

            for div in soup.find_all(name="div", attrs={"class": "row"}):
                for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
                    jobs.append(a["title"])
                    urls.append(a['href'])
                company = div.find_all(name="span", attrs={"class": "company"})
                if len(company) > 0:
                    for b in company:
                        companies.append(b.text.strip())
                else:
                    sec_try = div.find_all(name="span", attrs={"class": "result-link-source"})
                    for span in sec_try:
                        companies.append(span.text.strip())
            for div in soup.find_all(name="div", attrs={"class": "sjcl"}):
                for a in div.find_all(name="div", attrs={"class": "recJobLoc"}):
                    locations.append(a['data-rc-loc'].strip())
                for a in div.find_all(name="span", attrs={"class": "remote"}), div.find_all(name="div", attrs={"class": "recJobLoc"}):
                    if a == []:
                        jobPolicy.append(' ')
                    else:
                        try:
                            junk = a[0]['data-rc-loc']
                        except:
                            jobPolicy.append(a[0].text.strip())
            spans = soup.findAll("div", attrs={"class": "summary"})
            for span in spans:
                descriptions.append(span.text.strip())
            cnt = 0
            while cnt < len(jobs):
                json.append({"title": jobs[cnt], "company": companies[cnt], "refUrl": urls[cnt], "location": locations[cnt], "jobPolicy": jobPolicy[cnt], "description": descriptions[cnt]})
                cnt+=1
        except:
            return []
        p+=10
        json = responseJson + json
        print(json)

  
json = main(URL)
print(json)