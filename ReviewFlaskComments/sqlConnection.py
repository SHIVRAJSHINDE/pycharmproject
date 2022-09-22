import mysql.connector as msq

mylist = ["a", "b", "c"]
statelist = ["x", "y", "z"]

def insertFirstDatatoSql(listOfHeader,listOfLinks):

    conn=msq.connect(host="localhost",database="videoScrapperDB",user="root",passwd="Ashiv@0511")

    #cursor.execute("create database videoScrapperDB")
    #cursor.execute("create table videoScrapperDB.FruitTable(Fruits varchar(50),State varchar(80))")
    myc = conn.cursor()

    param = {}
    for i in range(0,10):
        param = {'Fruits':listOfHeader[i],'State': listOfLinks[i]}
        sql = 'INSERT INTO FruitTable(Fruits,State) VALUES(%(Fruits)s,%(State)s)'
        myc.execute(sql,param)
        conn.commit()
