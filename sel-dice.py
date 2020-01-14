from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import xlsxwriter
import random

urls = []
skill=input('Please enter the skill: ')
location = input('please enter the location: ')
noResume = input('please enter the number of consultants: ')
minExp = input('enter min experience: ')
maxExp = input('enter max experience: ')
visas = input('Please enter visa status (for two i.e need h1|employment auth document): ').split('|')
firstVisa = visas[0]
secVisa = ''
if len(visas) > 1:
    secVisa = '%7C'+visas[1]
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(executable_path='./chromedriver1',options=chrome_options)
driver.get('https://www.dice.com/employer/talent/search;q='+skill+';page=1;pageSize='+noResume+';location='+location+';sortBy=relevance;sortByDirection=desc;workPermits='+firstVisa+secVisa+';yOEMin='+minExp+';yOEMax='+maxExp+';excludeRecruiters=true;contactInfo=email;lastActive=90;profileSource=resumes')
WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.ID,'username'))) 
driver.find_element_by_id('username').send_keys('imran@prosistech.com')
driver.find_element_by_id('password').send_keys('Prosis2019')
driver.find_element_by_xpath("//button[@type='submit']").click() 
WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'search-results'))) 
a = driver.find_element_by_class_name('search-results').get_attribute('innerHTML')
soup = BeautifulSoup(a,features="html.parser")
for o in soup.find_all('a', attrs={'class': 'view-link ng-star-inserted'},href=True):
    urls.append('https://www.dice.com'+o['href'])

fileName = skill+str(random.randrange(1,100))+ '.xlsx'
workbook = xlsxwriter.Workbook(fileName)
worksheet = workbook.add_worksheet()
row = 0
for items in urls:
    driver.get(items)
    WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.ID,'profile-page-info-name'))) 
    name = driver.find_element_by_id('profile-page-info-name').text
    details = driver.find_elements_by_xpath("//a[@class='c-pointer text-primary']")
    print(name + ' '+ details[0].text)
    worksheet.write(row,0,name)
    worksheet.write(row,1,details[0].text)
    if len(details) > 1:
         worksheet.write(row,2,details[1].text)
         print(details[1].text)
    row = row +1

   

workbook.close()
print('DONE' + ' '+ fileName)
