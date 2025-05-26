from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time

all_tweets = []

e_mail = ""
kullanici_adi = ""
kullanici_sifre = ""
hashtag = ""

browser = webdriver.Chrome()
browser.get("https://x.com/?lang=tr")
browser.fullscreen_window()

wait = WebDriverWait(browser, 10)

login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[4]/a")))
login_button.click()

username = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input")))
username.send_keys(e_mail)

next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]")))
next_button.click()

try:
    second_username = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input")))
    second_username.send_keys(kullanici_adi)

    next_button2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button")))
    next_button2.click()
except Exception as e:
    print("Kullanıcı adı istenmedi, doğrudan şifre ekranına geçiliyor...")

password = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input")))
password.send_keys(kullanici_sifre)

login = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button")))
login.click()

search = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/div/div[2]/div/input")))
search.send_keys(hashtag)
search.send_keys(Keys.RETURN)

lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight); return document.body.scrollHeight;")
match = False

while not match:
    lastCount = lenOfPage
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    lenOfPage = browser.execute_script("return document.body.scrollHeight")
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    tweets = soup.select("[data-testid='tweetText']")
    for tweet in tweets:
        if tweet.get_text() not in all_tweets:
            all_tweets.append(tweet.get_text())
    if lastCount == lenOfPage:
        match = True
sayac = 1
with open("tweet.txt", "w", encoding="utf-8") as file:
    for i in all_tweets:
        file.write(str(sayac) + "." + i + "\n")
        file.write("***************************************\n")
        sayac += 1

browser.close()
