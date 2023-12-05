# app.py

import flask
import os,wget
from flask import Flask, render_template, request, jsonify
import instaloader
import wget
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep


app = Flask(__name__)
app.static_folder = 'static'

L = instaloader.Instaloader()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/Bot/<hashtag>/<limit>')
def scrape(hashtag,limit):

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(executable_path="./chromedriver.exe",options=chrome_options)
    driver.get("https://www.instagram.com")

    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="username"]'))).clear()
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]'))).clear()
    username.send_keys("your username")
    password.send_keys("your password")
    print("Successfully logged In")
    
    Login_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    alert = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    
    driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
    sleep(10)
    driver.execute_script("window.scrollTo(0,4000);")

    anchors = driver.find_elements_by_tag_name('a')
    anchors = [a.get_attribute('href') for a in anchors]
    anchors = [a for a in anchors if str(a).startswith("https://www.instagram.com/p/")]
    print("\nPreparing to download...")

    path = os.getcwd()+"\static\\"
    path = os.path.join(path, hashtag)
    os.makedirs(path,exist_ok=True)
    os.chdir(path)
    print("\nFolder created successfully")

    counter = 0
    res=[]
    for a in anchors:
        driver.get(a)
        sleep(5)
        
        detail=driver.find_elements_by_tag_name('a')
        user=detail[9].get_attribute('innerHTML')
        location=detail[10].get_attribute('innerHTML')
        
        date=driver.find_elements_by_tag_name('time')[0].get_attribute('innerHTML')
        
        img = driver.find_elements_by_tag_name('img')[3].get_attribute('src')
        save_as = os.path.join(path, str(counter) +'.jpg')
        wget.download(img, save_as)
        print("\nDownloaded ",counter,".jpg")
        res.append({
                'url': save_as,
                'target':img,
                'owner': user,
                'date': date,
                'location':location
            })
        
        counter += 1
        if(counter==limit):
            break

    res = jsonify(res)
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res




@app.route('/api/Module/<hashtag>/<limit>')
def get_posts(hashtag,limit):
    res = []
    count=0
    
    path=os.getcwd()+"\static\\"
    path=os.path.join(path,hashtag)
    os.makedirs(path,exist_ok=True)
    os.chdir(path)

    posts = instaloader.Hashtag.from_name(L.context, hashtag).get_all_posts()
    for post in posts:
        L.download_post(post, target=post.owner_username)
        folder_path=os.path.join(post.owner_username)
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))  and f.lower().endswith('.jpg') ]
        res.append({
            'url': "/static/"+hashtag+"/"+post.owner_username+"/"+files[0],
            'target':post.url,
            'owner': post.owner_username,
            'date': post.date_utc.strftime('%Y-%m-%d %H:%M:%S'),
            'location':post.location
        })
        
        count += 1
        if (count == limit):
            break
        
    res = jsonify(res)
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res



if __name__ == '__main__':
    app.run(debug=True)

