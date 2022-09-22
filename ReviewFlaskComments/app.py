from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
import mysql.connector as msq
import downloadVideo
#import fifth
import extractComments


import os
import time
import requests
from selenium import webdriver
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
def searchTrainer():
    if request.method == 'POST':
        inputValueTrainer = request.form["content"].replace(" ","")
        if inputValueTrainer == "krishna":
            inputValueTrainer =  "user/krishnaik06"
        elif inputValueTrainer == "Telusko":
            inputValueTrainer = "c/Telusko"


        noOfVideos=10
        driver = webdriver.Chrome(r'C:\Users\shind\ChromeDriver\chromedriver.exe')
        #search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

        search_url=('https://www.youtube.com/{q}/videos')

        # load the page
        driver.get(search_url.format(q=inputValueTrainer))

        time.sleep(0.5)

        listOfLinks = []
        listOfHeader = []
        indexOfVideo = []
        #noOfVideos = 50

        driver.maximize_window()

        #noOfVideos = 50

        # url = '//*[@id="video-title"]'
        for i in range(10, noOfVideos, 10):
            url1 = '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer[' + str(
                i) + ']/div[1]/div[1]/div[1]/h3/a'
            flag = driver.find_element(by=By.XPATH, value=url1)

            # driver.execute_script("window.scrollBy(0,1000)","")
            driver.execute_script("arguments[0].scrollIntoView();", flag)
            time.sleep(3)

        for i in range(1, noOfVideos+1):
            path = '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer[' + str(
                i) + ']/div[1]/div[1]/div[1]/h3/a'
            theUrl = driver.find_element(by=By.XPATH, value=path)
            theUrl = theUrl.get_attribute("href")
            listOfLinks.append(theUrl)

            videoHeader = driver.find_element(by=By.XPATH, value=path)
            videoHeader = videoHeader.get_attribute("text")
            listOfHeader.append(videoHeader)


        #li = {'Fruit': listOfHeader, 'State': listOfLinks}
        #data = pd.DataFrame(li)
        #print(data)

        insertFirstDatatoSql(listOfHeader1=listOfHeader, listOfLinks1=listOfLinks)
        extractComments.extactComments(listOfLinks1=listOfLinks)
        downloadVideo.downloadVideosAndThumbNail(listOfLinks1=listOfLinks)




def insertFirstDatatoSql(listOfHeader1:list,listOfLinks1:list):

    conn=msq.connect(host="localhost",database="videoScrapperDB",user="root",passwd="Ashiv@0511")

    #cursor.execute("create database videoScrapperDB")
    #cursor.execute("create table videoScrapperDB.FruitTable(Fruits varchar(50),State varchar(80))")
    myc = conn.cursor()
    myc.execute('Delete from videoScrapperDB.FruitTable')
    conn.commit()
    param = {}

    for i in range(0,len(listOfHeader1)):
        param = {'Fruits':listOfHeader1[i],'State': listOfLinks1[i]}
        sql = 'INSERT INTO FruitTable(Fruits,State) VALUES(%(Fruits)s,%(State)s)'
        myc.execute(sql,param)
        conn.commit()

#noOfVideos1 = int(input("enter No Videos: "))

#inputValueTrainer1 = str(input("enter Trainer: "))

#searchTrainer(inputValueTrainer=inputValueTrainer1,noOfVideos=noOfVideos1)

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True)

