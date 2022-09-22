# Download vide and Thumbnail
import mysql.connector as msq
from pytube import YouTube


def uploadVideosAndThumbNail(listOfThumbNail1:list,link1:list):
    conn=msq.connect(host="localhost",database="videoScrapperDB",user="root",passwd="Ashiv@0511")

    #cursor.execute("create database videoScrapperDB")
    #conn.execute("create table videoScrapperDB.CommentsTable(Links varchar(200),Commenter varchar(200),commentss varchar(MAX))")
    myc = conn.cursor()

    param = {}
    for j in range(0,len(listOfThumbNail1)):
        param = {'Links':link1[j],'ThumbNail': listOfThumbNail1[j]}
        sql = 'INSERT INTO videosAndThumbNail(Links,ThumbNail) VALUES(%(Links)s,%(ThumbNail)s)'
        myc.execute(sql,param)
        conn.commit()




def downloadVideosAndThumbNail(listOfLinks1: list):
    conn=msq.connect(host="localhost",database="videoScrapperDB",user="root",passwd="Ashiv@0511")
    myc = conn.cursor()
    myc.execute('Delete from videoScrapperDB.videosAndThumbNail')
    conn.commit()

    for i in listOfLinks1:
        #listOfLinks1 = 'https://www.youtube.com/watch?v=58RsdQXG0IA'
        listOfLinks2 = []
        listOfThumbNail = []
        #print(listOfLinks1)
        #link = i
        youtube_1 = YouTube(i)

        listOfLinks2.append(i)
        listOfThumbNail.append((youtube_1.thumbnail_url))

        videos = youtube_1.streams.all()
        vid = list(enumerate(videos))
        for i in range(0, len(vid)):
            if i == 0:
                print(vid[i])
                break

        print()
        # strm = int(input("enter: "))
        strm = 0
        videos[strm].download(r'C:\Users\shind\PycharmProjects\videoScrapperFinal2\Videos')
        print("Downloaded succesfully")

        print(listOfLinks2)
        print(listOfThumbNail)

        uploadVideosAndThumbNail(listOfThumbNail1=listOfThumbNail,link1=listOfLinks2)



