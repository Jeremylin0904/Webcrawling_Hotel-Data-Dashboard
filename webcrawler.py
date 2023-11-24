from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import pandas as pd
from selenium.webdriver.chrome.options import Options
import time


def webcrawler(location, checkin, checkout):
    hnames = []
    hlocations = []
    hdist = []
    hprice = []
    hcomments = []
    hrating = []
    
    chrome_options = Options()

    # 启用无头模式
    chrome_options.add_argument("--headless")

    # 创建WebDriver时传递chrome_options
    driver = webdriver.Chrome(options=chrome_options)
    

    # 要访问的URL
    url = f'https://www.booking.com/searchresults.en-us.html?ss={location}&checkin={checkin}&checkout={checkout}'

    # 使用Selenium打开网页
    driver.get(url)


    accept = '//*[@id="onetrust-accept-btn-handler"]'

    accept_button = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, accept)))

    # 點擊下一頁
    accept_button.click()
    page_source = driver.page_source
    #updated_url = driver.current_url

    

    # 解析HTML
    soup = BeautifulSoup(page_source, 'html.parser')

    pages = soup.find_all('button', class_='a83ed08757 a2028338ea')
    instances = soup.find_all('h1',class_= 'f6431b446c d5f78961c3')
    pagenum = []
    for page in pages:
        pagenum.append(int(page.text))
    for instance in instances:
        number = instance.text

    maxpagenum = np.max(pagenum)
    '''
    print(number)
    print(f'Number of Pages: {maxpagenum}')
    print(f'At Page: 1')
    '''

    # 找到所有具有特定类的元素
    properties = soup.find_all('div', {'class': 'c82435a4b8 a178069f51 a6ae3c2b40 a18aeea94d d794b7a0f7 f53e278e95 c6710787a4', 'data-testid':'property-card'})
    for k, property in enumerate(properties):
        names = property.find('div', {'class':'f6431b446c a15b38c233', 'data-testid':'title'})
        locations = property.find('span', {'class':'aee5343fdb def9bc142a', 'data-testid':'address'})
        distances = property.find('span',{'data-testid':"distance"})
        rating = property.find('div', {'class': 'a3b8729ab1 d86cee9b25'})
        price = property.find('span', {'class': 'f6431b446c fbfd7c1165 e84eb96b1f', 'data-testid':"price-and-discounted-price"})
        comments = property.find('div', {'class': 'a3b8729ab1 e6208ee469 cb2cbb3ccb'})
        if names == None:
            names = []
            
            hnames.append(np.nan)
        if locations == None:
            locations = []
            
            hlocations.append(np.nan)
        if distances == None:
            distances = []
           
            hdist.append(np.nan)
        if rating == None:
            rating = []
            
            hrating.append(np.nan)
        if price == None:
            price = []
            
            hprice.append(np.nan)
        if comments == None:
            comments = []
            
            hcomments.append(np.nan)

        for element in names:
            hnames.append(element.text)
            
        for element in locations:
            hlocations.append(element.text)
            
        for element in distances:
            dist = float(element.text.split(' ')[0])
            if dist>99.9:
                dist = dist/1000
            hdist.append(dist)
            
        for element in rating:
            hrating.append(float(element.text))
            
        for element in price:
            p = element.text
            hprice.append(int(p.split()[1].replace(',','')))
            
        for element in comments:
            comment = element.text
            if comment == 'Review score ':
                    comment = 'Rating under 7'
            hcomments.append(comment)
            

    i = 1
    while i < maxpagenum:
        i = i+1
        #print(f'At Page: {i}')
        '''
        chrome_options = Options()

        # 启用无头模式
        chrome_options.add_argument("--headless")

        # 创建WebDriver时传递chrome_options
        driver = webdriver.Chrome()

        url = updated_url

        # 使用Selenium打开网页
        driver.get(url)


        accept = '//*[@id="onetrust-accept-btn-handler"]'

        accept_button = WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, accept)))

        # 點擊下一頁
        accept_button.click()
        '''


        nextapgexpath ='//*[@id="bodyconstraint-inner"]/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[4]/div[2]/nav/nav/div/div[3]/button'

        nextapge_button = WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, nextapgexpath)))

        # 點擊下一頁
        nextapge_button.click()
        time.sleep(2)
        
        #updated_url = driver.current_url
        page_source = driver.page_source

        

        # 解析HTML
        soup = BeautifulSoup(page_source, 'html.parser')
        properties = soup.find_all('div', {'class': 'c82435a4b8 a178069f51 a6ae3c2b40 a18aeea94d d794b7a0f7 f53e278e95 c6710787a4', 'data-testid':'property-card'})
        for k, property in enumerate(properties):
            names = property.find('div', {'class':'f6431b446c a15b38c233', 'data-testid':'title'})
            locations = property.find('span', {'class':'aee5343fdb def9bc142a', 'data-testid':'address'})
            distances = property.find('span',{'data-testid':"distance"})
            rating = property.find('div', {'class': 'a3b8729ab1 d86cee9b25'})
            price = property.find('span', {'class': 'f6431b446c fbfd7c1165 e84eb96b1f', 'data-testid':"price-and-discounted-price"})
            comments = property.find('div', {'class': 'a3b8729ab1 e6208ee469 cb2cbb3ccb'})
            if names == None:
                names = []
                
                hnames.append(np.nan)
            if locations == None:
                locations = []
                
                hlocations.append(np.nan)
            if distances == None:
                distances = []
                
                hdist.append(np.nan)
            if rating == None:
                rating = []
                
                hrating.append(np.nan)
            if price == None:
                price = []
                
                hprice.append(np.nan)
            if comments == None:
                comments = []
                
                hcomments.append(np.nan)

            for element in names:
                hnames.append(element.text)
                
            for element in locations:
                hlocations.append(element.text)
                
            for element in distances:
                dist = float(element.text.split(' ')[0])
                if dist>99.9:
                    dist = dist/1000
                hdist.append(dist)
                
            for element in rating:
                hrating.append(float(element.text))
                
            for element in price:
                p = element.text
                hprice.append(int(p.split()[1].replace(',','')))
                
            for element in comments:
                comment = element.text
                if comment == 'Review score ':
                        comment = 'Rating under 7'
                hcomments.append(comment)
                

    driver.quit()
    data = pd.DataFrame({'name':hnames,'location':hlocations,'price':hprice,'ratings':hrating,'distance':hdist,'comments':hcomments})
    data.to_csv(f'Hotel_{location}_{checkin}_{checkout}.csv')
    return data