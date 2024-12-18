import pandas as pd
import numpy as np
import bs4
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib import request
import datetime
import requests
from datetime import datetime 
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import seaborn as sns


# Setting browser's options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--start-maximized")
options.add_argument("--disable-popup-blocking")

# Path to the installed compatible chromedriver
path = 'Your_chromedriver_path'
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)


# Access to Glints website
driver.get('https://glints.com/vn/opportunities/jobs/explore')
print('-- Glints accessed')

# Wait for 2 second for the site to load
sleep(2)
# Get html content
res = requests.get(driver.current_url)
soup2 = BeautifulSoup(res.text, 'html.parser')
page_source = BeautifulSoup(driver.page_source)



# Close pop-up. Pop-up will appear only if the page was scrolled down (took a long time to figure out tho)
html = driver.find_element(By.TAG_NAME, 'html')
html.send_keys(Keys.DOWN)
sleep(1)
html.send_keys(Keys.ESCAPE)
html.send_keys(Keys.UP)
driver.implicitly_wait(1)


#Send job search keyword:
#key_word = input('Input keyword: ') 
keyword = 'Data Analyst'
job_input = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/div/input')
sleep(1)
job_input.send_keys(Keys.CONTROL + "a")
job_input.send_keys(Keys.DELETE)
job_input.send_keys(keyword)
job_input.send_keys(Keys.RETURN)

#Click search
search_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/div[2]/div[2]/div[2]/div[2]/div/div/div[3]/button')
search_button.send_keys(Keys.ENTER)
print('-- Start searching...')

#Infinite scroll so instead of define Next button
#But scroll fairly to the bottom and wait until the very last page loaded
while True:
    page_height = driver.execute_script("return document.body.scrollHeight")
    target_height = page_height - 1220
    driver.execute_script("window.scrollTo(0, %s);" %target_height )
    sleep(2)
    try:
        state = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/div[2]/div[2]/div[2]/div[4]/div[2]/div[2]/span')
        if state.text == 'Đã tải lên tất cả cơ hội việc làm': 
            print('-- All page loaded') 
            break
    except:
        continue 
        
job_id = BeautifulSoup(driver.page_source).find_all('a', class_='CompactOpportunityCardsc__CardAnchorWrapper-sc-1y4v110-18 iOjUdU job-search-results_job-card_link')
print("-- Found {} jobs.".format(len(job_id)))
print("-- Start crawling job's detailed information")


#Get link for each job
job_url = []
for i in job_id:
    link = i.get('href')
    url = 'https://glints.com'+link
    job_url.append(url)


#Export job_url list to file in order to prevent data loss due to sudden termination of the program
today = datetime.today().strftime('%y%m%d')
with open(f'Glints_joburl_{today}.txt', 'w') as f:
    for line in job_url:
        f.write("%s\n" % line)


#Define the DataFrame structure
df = pd.DataFrame(columns = ["job_title", 'job_link', "company_name", "company_link", "salary", "currency",
                           "category", "contract", "experience", "benefit", "requirement",'industry',
                           "company_size", "company_location", "job_location", "posted", "updated"])
# Add job_url to the DataFrame
df['job_link'] = job_url

# Define a dict which will be appended to the df after each link being crawled
crawl_set = {}


for link in job_url:
    driver.get(link)
#     sleep(3)
    try:
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="GlintsContainer-sc-ap1z3q-0 iUnyrV"]')))
        html_of_interest = driver.execute_script('return arguments[0].innerHTML',element)
        soup = BeautifulSoup(html_of_interest, 'lxml')
    except:
        print('Error orcurred at url: {}'.format(link))
        continue
        
    #Job title
    try:
        crawl_set['job_title'] = soup.select('div[class="TopFoldsc__JobOverviewHeader-sc-kklg8i-24 gfOGEj"]')[0].text
    except:
        crawl_set['job_title'] = None
        
    #Company name
    try:
        crawl_set['company_name'] = soup.select('div[class ="TopFoldsc__JobOverViewCompanyName-sc-kklg8i-5 eLQvRY"]>a')[0].text
    except:
        crawl_set['company_name'] = None
        
    #Company profile
    try:
        crawl_set['company_link'] = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/div[2]/div[2]/div[2]/div/main/div[1]/div[2]/div/div[2]/div/a').get_attribute('href')
    except:
        crawl_set['company_link'] = None
        
    #salary
    try:
        crawl_set['salary'] = soup.select('span[class="TopFoldsc__BasicSalary-sc-kklg8i-15 lolAnb"]')[0].text
        ##soup.select('.TopFoldsc__JobOverViewInfo-sc-kklg8i-9.EWOdY')[0].text
    except:
        crawl_set['salary'] = None
        
    #currency 
    try:
        crawl_set['currency'] = soup.select('span[class="TopFoldsc__CurrencyCode-sc-kklg8i-30 eCrNiw"]')[0].text
    except:
        crawl_set['currency'] = None
        
    #category
    try:
        crawl_set['category'] = soup.select('div[class="TopFoldsc__JobOverViewInfo-sc-kklg8i-9 EWOdY"]>a')[0].text
        ##soup.select('.TopFoldsc__JobOverViewInfo-sc-kklg8i-9.EWOdY')[1].text
    except:
        crawl_set['category'] = None
        
    #contract
    try:
        crawl_set['contract'] = soup.select('div[class="TopFoldsc__JobOverViewInfo-sc-kklg8i-9 EWOdY"]')[1].text
        ##soup.select('.TopFoldsc__JobOverViewInfo-sc-kklg8i-9.EWOdY')[2].text
    except:
        crawl_set['contract'] = None

    #experience
    try:
        crawl_set['experience'] = soup.select('div[class="TopFoldsc__JobOverViewInfo-sc-kklg8i-9 EWOdY"]')[2].text
        ##soup.select('.TopFoldsc__JobOverViewInfo-sc-kklg8i-9.EWOdY')[3].text
    except:
        crawl_set['experience'] = None

    #requirement
    requirement = soup.select('.TagStyle__TagContent-sc-66xi2f-0.bxpfKm.tag-content')
    req_list = []
    for i in range(len(requirement)):
        req_list.append(requirement[i].text)
    crawl_set['requirement'] = ','.join(req_list)

    #benefit packages
    try:
        benefit = soup.select('ul[class="Benefitssc__BenefitList-sc-10xec8z-1 iCclQu"]>li>div>h3')
        benefit_list = []
        if len(benefit_list)!=0:
            for i in benefit:
                benefit_list.append(i.text)
            crawl_set['benefit'] = ','.join(benefit_list)
        else:
            crawl_set['benefit'] = None
    except:
        crawl_set['benefit'] = None


    #industry
    try:
        crawl_set['industry'] = soup.select('div[class="AboutCompanySectionsc__CompanyIndustryAndSize-sc-7g2mk6-7 iGZjWK"]>span')[0].text
    except:
        crawl_set['industry'] = None


    #Company size
    try:
        crawl_set['company_size'] = soup.select('div[class="AboutCompanySectionsc__CompanyIndustryAndSize-sc-7g2mk6-7 iGZjWK"]>span')[1].text
    except:
        crawl_set['company_size'] = None

    #company_location
    try:
        crawl_set['company_location'] = soup.select('div[class="AboutCompanySectionsc__AddressWrapper-sc-7g2mk6-14 bBEGUc"]')[0].text
    except:
        crawl_set['company_location'] = None

    #job location
    try:
        crawl_set['job_location'] = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/div[2]/div[2]/div[1]/div/label[3]/a').text.lstrip('Việc Làm Tại')
    except:
        crawl_set['job_location'] = None

    #post
    try:
        posted = soup.select('span[class="TopFoldsc__PostedAt-sc-kklg8i-13 vnaHT"]')
        posted = posted[0].text.split(' ',1)[1]
        crawl_set['posted'] = posted
    except:
        crawl_set['posted'] = None

    #update
    try:
        updated = soup.select('span[class="TopFoldsc__UpdatedAt-sc-kklg8i-14 kjxTBC"]')
        updated = updated[0].text.split(' ',1)[1]
        crawl_set['updated'] = updated
    except:
        crawl_set['updated'] = None
        
    #job_link
    try:
        crawl_set['job_link'] = link
    except:
        crawl_set['job_link'] = 'Error'

    #crawled time
    crawl_set['scrapped_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    df=df.append(crawl_set, ignore_index = True)
    
    if len(df) == len(job_url):
        print('--Finish scrapping')
    elif len(df)%20 == 0:
        print('--There are {} links scraped as {}% of total. {} to go. Continue...'.format(len(df), round(len(df)/len(job_url)*100,2), len(job_url)-len(df)))


# Export crawl data to csv file
df.to_csv(f"Glintsdata_{today}.csv")
