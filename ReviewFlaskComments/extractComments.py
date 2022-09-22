# Extract Comments
import mysql.connector as msq
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import io
import sys




def extactComments(listOfLinks1:list):

    driver = webdriver.Chrome(r'C:\Users\shind\ChromeDriver\chromedriver.exe')

    conn=msq.connect(host="localhost",database="videoScrapperDB",user="root",passwd="Ashiv@0511")
    #cursor.execute("create database videoScrapperDB")
    #conn.execute("create table videoScrapperDB.CommentsTable(Links varchar(200),Commenter varchar(200),commentss varchar(MAX))")
    myc = conn.cursor()
    myc.execute('Delete from videoScrapperDB.CommentsTable')
    conn.commit()


    for link in listOfLinks1:
        listOfComments = []
        listOfCommenters = []
        driver.get(link)
        #comment_section = driver.find_element_by_xpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[1]/ytd-comment-renderer/div[3]/div[2]/div[2]/ytd-expander/div/yt-formatted-string')

        driver.maximize_window()
        time.sleep(2)


        comment_section = driver.find_element_by_xpath('//*[@id="comments"]')
        driver.execute_script("arguments[0].scrollIntoView();", comment_section)

        time.sleep(2)
        try:
            noOfComments = driver.find_element_by_xpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/h2/yt-formatted-string/span[1]').text
            noOfComments = int(noOfComments)
        except Exception:
            driver.execute_script("window.scrollBy(0,1000)", "")
            time.sleep(5)
            noOfComments = driver.find_element_by_xpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/h2/yt-formatted-string/span[1]').text
            noOfComments = int(noOfComments)

        i = 1
        for i in range(1, noOfComments, 4):
            time.sleep(0.5)
            try:
                url1 = '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer['+str(i)+']/ytd-comment-renderer/div[3]/div[2]/div[1]/div[2]/h3/a/span'
                flag = driver.find_element(by=By.XPATH, value=url1)
                driver.execute_script("arguments[0].scrollIntoView();", flag)
            except Exception:
                time.sleep(4)
                driver.execute_script("window.scrollBy(0,1000)","")
                pass
            time.sleep(1)

        i=1

        for i in range(1, noOfComments):
            try:
                xyz = driver.find_element_by_xpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer['+str(i)+']/ytd-comment-renderer/div[3]/div[2]/div[1]/div[2]/h3/a/span').text
                listOfCommenters.append(xyz)

                abc1 = driver.find_element_by_xpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer['+str(i)+']/ytd-comment-renderer/div[3]/div[2]/div[2]/ytd-expander/div/yt-formatted-string').text
                listOfComments.append(abc1)

            except Exception:
                pass

        print(listOfCommenters)
        print(listOfComments)
        print(noOfComments)
        uploadComments(listOfCommenters1=listOfCommenters, listOfComments1=listOfComments, link1=link)





def uploadComments(listOfCommenters1:list,listOfComments1:list,link1:str):
    conn=msq.connect(host="localhost",database="videoScrapperDB",user="root",passwd="Ashiv@0511")
    #cursor.execute("create database videoScrapperDB")
    #conn.execute("create table videoScrapperDB.CommentsTable(Links varchar(200),Commenter varchar(200),commentss varchar(MAX))")
    myc = conn.cursor()

    param = {}
    for j in range(0,len(listOfCommenters1)):
        param = {'Links':link1,'Commenter': listOfCommenters1[j],'Comments':listOfComments1[j]}
        sql = 'INSERT INTO CommentsTable(Links,Commenter,Comments) VALUES(%(Links)s,%(Commenter)s,%(Comments)s)'
        myc.execute(sql,param)
        conn.commit()


