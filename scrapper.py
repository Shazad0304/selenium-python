from selenium import webdriver
from bs4 import BeautifulSoup
import xlsxwriter
import time
import random

skill = input('please enter the skill: ')
pages = int(input('please enter the pages: '))
print('starting headless chrome')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(executable_path='./chromedriver1',chrome_options=chrome_options)
driver.get("http://desiopt.com/login/")
print('logging')
driver.find_element_by_class_name('username').send_keys("raj.kumar")
driver.find_element_by_class_name('password').send_keys("prosis123")
driver.find_element_by_xpath("//input[@value='Login']").click() 
driver.get('http://desiopt.com/search-resumes/')
driver.find_element_by_id('Title').send_keys(skill)
driver.find_element_by_xpath("//input[@value='Search']").click()
print('Searching') 
workbook = xlsxwriter.Workbook(skill+ str(random.randrange(1,100))+'.xlsx')
worksheet = workbook.add_worksheet()
row = 0
load = '#'
time.sleep(4)
for iter in range(0, pages):

    html5 = driver.current_url
#html = driver.execute_script("return document.body.outerHTML;;")
    html = driver.find_element_by_class_name('ResumeResults').get_attribute('innerHTML')
#print(html)
    soup = BeautifulSoup(html,"html5lib")
    urls = []
    for a in soup.find_all('a', href=True):
    #print("Found the URL:", a['href'])
        if "display" in a['href']:
            urls.append(a['href'])
            

    urls = list(set(urls))
    print('fetching results')
    for ur in urls:
        
        driver.get(ur)
        time.sleep(2)
        print(load)
        html1 = driver.find_element_by_class_name('comp-profile-content').get_attribute('innerHTML')
        soup1 = BeautifulSoup(html1,"html5lib")
        email= soup1.find('span', attrs={'class': 'longtext-150 tooltip-counter-4'}).text
        worksheet.write(row,2,email)
        phone = soup1.find('span', attrs={'class': 'longtext-26 tooltip-counter-3'}).text
        worksheet.write(row,1,phone)
        name = soup1.find('span', attrs={'class': 'longtext-50 tooltip-counter-1'}).text
        name= name + " " + soup1.find('span', attrs={'class': 'longtext-50 tooltip-counter-2'}).text
        worksheet.write(row,0,name)
        row = row + 1
        load = load + '#'
    
    driver.get(html5)
    time.sleep(5)
    driver.find_element_by_class_name('nextBtn').click() 
workbook.close()
print('done')

