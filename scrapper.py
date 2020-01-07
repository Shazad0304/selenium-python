from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome('./chromedriver1')
driver.get("http://desiopt.com/login/")
driver.find_element_by_class_name('username').send_keys("raj.kumar")
driver.find_element_by_class_name('password').send_keys("prosis123")
driver.find_element_by_xpath("//input[@value='Login']").click() 
driver.get('http://desiopt.com/search-resumes/')
driver.find_element_by_id('Title').send_keys("java")
driver.find_element_by_xpath("//input[@value='Search']").click() 
time.sleep(4)
#html = driver.execute_script("return document.body.outerHTML;;")
html = driver.find_element_by_class_name('ResumeResults').get_attribute('innerHTML')
#print(html)
soup = BeautifulSoup(html,"html5lib")
urls = []
for a in soup.find_all('a', href=True):
    #print("Found the URL:", a['href'])
    if "display" in a['href']:
        urls.append(a['href'])
        print(a['href'])

urls = list(set(urls))
for ur in urls:

    driver.get(ur)
    time.sleep(2)

    html1 = driver.find_element_by_class_name('comp-profile-content').get_attribute('innerHTML')
    soup1 = BeautifulSoup(html1,"html5lib")
    email= soup1.find('span', attrs={'class': 'longtext-150 tooltip-counter-4'}).text
    print(email)
    phone = soup1.find('span', attrs={'class': 'longtext-26 tooltip-counter-3'}).text
    print(phone)
    name = soup1.find('span', attrs={'class': 'longtext-50 tooltip-counter-1'}).text
    name= name + " " + soup1.find('span', attrs={'class': 'longtext-50 tooltip-counter-2'}).text
    print(name)
    
    
    
    

