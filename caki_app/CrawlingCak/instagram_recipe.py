from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


chrome_options = Options().add_experimental_option("detach",True)

# 브라우저 꺼짐 방지
driver = webdriver.Chrome(options=chrome_options) 

driver.get('https://www.instagram.com/proofnote/')
driver.implicitly_wait(10) # 10초 동안 대기

id = 'mount_0_0_pI'

for i in range (1,4):
    for j in range(1,5):
        post = driver.find_element(By.XPATH,f'//*[@id="{id}"]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div[4]/div/div[{j}]/div[{i}]')
        post.click()
        driver.implicitly_wait(10) # 10초 동안 대기
        
        post_close = driver.find_element(By.XPATH,'/html/body/div[8]/div[1]/div/div[2]/div/div/svg')
        post_close.click()
        
        
        post_text = driver.find_element(By.XPATH ,f'/html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[1]/li/div/div/div[2]/div[1]/h1')
        print(post_text.text)






