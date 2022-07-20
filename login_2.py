from time import sleep
import os
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests

# ローカル上のChrome Driverを指定(※デプロイするときはコメントする)
# driver_path = '/Users/beezow/heroku_pro/chromedriver'

# Heroku上のChrome Driverを指定(※デプロイするときはコメントを外す)
driver_path = '/app/.chromedriver/bin/chromedriver'

options = webdriver.ChromeOptions()
options.add_argument('--headless') #これを設定すると見えなくなる

#クローラーを起動
driver = webdriver.Chrome(options=options, executable_path=driver_path)

#図書館にアクセス
url = 'https://www.library.city.nagoya.jp/licsxp-opac/WOpacMnuTopInitAction.do?WebLinkFlag=1&moveToGamenId=mylibrary'
username = '0594466575',
password = 'pokemonda0526' 
driver.get(url) #urlに移動
soup = BeautifulSoup(driver.page_source, 'html.parser')

driver.find_element_by_xpath("//input[@id='usrcardnumber']").send_keys(username)
sleep(3)
driver.find_element_by_xpath("//input[@id='password']").send_keys(password)
sleep(3)
driver.find_element_by_xpath("//input[@accesskey='x']").send_keys(Keys.ENTER)
sleep(5)
#予約ページに飛ぶ
driver.find_element_by_xpath("//ul[@class='blist']/li/a").send_keys(Keys.ENTER)
sleep(5)

title_list = []
rank_list = []

for titles in driver.find_elements_by_xpath("//strong/a[@tabindex='201']"):
    title = titles.text
    title_list.append(title)
for ranks in driver.find_elements_by_xpath("//td[contains(@id,'ItemDeta0105h')]"):
    rank = ranks.text
    rank_list.append(rank)

list = title_list + rank_list

driver.quit()

def send_line(list):
    # ブラウザを終了する
    #localだとこっち
    # acc_token = 'qBFToRqB2zMCgeXNYChw3GBeEUoXdV3V1dPZAqMenGJ'
    acc_token = os.environ['ACC_TOKEN']
    line_api = 'https://notify-api.line.me/api/notify'
    payload = {'message':list}
    headers = {'Authorization': 'Bearer ' + acc_token}
    requests.post(line_api, data=payload, headers=headers)

#LINEに通知
send_line(list)