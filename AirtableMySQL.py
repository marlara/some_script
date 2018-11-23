from datetime import datetime
import mysql.connector
from mysql.connector import errorcode
from airtable import airtable
import requests
import csv

#Mess with dates: Airtable has some issues on date format with various bugs reported, so the only solution is to pass the date as strings and change formats couple of times to match the mySQL date format

API_KEY = 'keyXXXX' #your API key
BASE_ID = 'appXXXX' #take the id from https://airtable.com/api 

class myScript:
    def __init__(self):
        self.commandStop = False #this set the command to Stop the script if Airtable is already updated
               
    def searchAirtable(self):
        self.at = airtable.Airtable(BASE_ID, 'tblXXX', api_key = API_KEY) #table id

        item_list = enumerate(self.at.get_all(sort='CreatedTime')) #enumerate table items and sort by CreatedTime column (there's a function for this: https://support.airtable.com/hc/en-us/articles/215646218-Formulas-and-date-fields)
        last_item = self.at.get_all(sort='CreatedTime')[-1] #take the last item
        print(last_item)
        fieldDate = last_item['fields']['Date'] #gets date value
        self.dateAirtable = datetime.strptime(fieldDate, '%d/%m/%Y').isoformat()
        print('Date Aitable: '+self.dateAirtable)
        self.toDate = datetime.strptime(fieldDate, '%d/%m/%Y').replace(hour=23, minute=59).strftime('%Y-%m-%d %H:%M:%S') #here it takes the string in Date and parse it as a date, then it convert it into a string with the format that will match the mySQL format for dates, replace hours because if I didn't do that it takes the same record from mysql db
        print(self.toDate)

    def mySqlCode(self):
        self.date = []
        self.num_risorse = []
        self.attachment = []
        config = {
            'user': XXX,
            'password': XXX,
            'host': XXX,
            'database': XXX
        }

        cnx = cur = None
        try:
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor(buffered=True) #buffered True is important for the condition of cursor.execute
            query = ("SELECT Id, WorkedFilePath, FileRowCount, DateCreation FROM mediaimportrequest WHERE DateCreation>%s") #%s is the variable
            dateLimit = self.toDate
            try: #try to catch the not updated items on Airtable based on dateLimit
                cursor.execute(query, (dateLimit,)) #assign dateLimit to the variable, COMMA IS IMPORTANT
                for (Id,FileRowCount,WorkedFilePath,DateCreation) in cursor:
                    print("Id: {}, Items:{}, File: {}, DateCreation: {}".format(Id,FileRowCount,WorkedFilePath,DateCreation))
                    self.date.append(datetime.strftime(DateCreation, '%d/%m/%Y')) #and now the isoformat is converted into a string with the right format
                    self.num_risorse.append(WorkedFilePath)
                    self.attachment.append(FileRowCount)
            except:
                self.commandStop = True #set the command to stop if the try fails
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Something is wrong with your user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        cursor.close()
        cnx.close()

    def searchCsv(self): #insert unique records from csv file (attachment) gotten before
            self.publisher = [] #create lists for each value we want
        self.tipologia = []
        self.nome_coll = []
        for rec in self.attachment:
            publisher = []
            tipologia = []
            nome_coll = []
            newFile = rec.replace("E:\\adm", "http://url").replace("\\","/").replace(" ", "%20") #compose url to download the csv, eventually whitespaces could be inserted into namefiles
            print("I'm searching in "+newFile)
            download = requests.get(newFile) #get the file from url
            decoded_content = download.content.decode('utf-8') #decode in utf-8

            csvFile = csv.DictReader(decoded_content.splitlines(), delimiter='\t')  #read the csv file and set delimiter, splitlines saves the day
            csvFile.fieldnames = [field.strip().lower() for field in csvFile.fieldnames]
            for row in csvFile:
                tipologia.append(row['type']) #this append the values from the right column to the list
                publisher.append(row["publisher"])
                nome_coll.append(row["nome_coll"])
            self.publisher.append(list(set(publisher)))
            self.tipologia.append(list(set(tipologia)))
            self.nome_coll.append(list(set(nome_coll)))
        print(self.publisher)
        print(self.tipologia)
        print(self.nome_coll)

    def insertAirtable(self): #insert records from mySQL metadata
        i = 0
        for item in self.attachment:
            tmpv = self.at.insert({ 
               'Date': self.date[i],
               'Numero di risorse': self.num_risorse[i],
               'Attachments': self.attachment[i],
               'Tipologia': self.tipologia[i],
               'Publisher':  ';'.join(self.publisher[i]), #join is needed to transform into string, if not Airtable will return an error
                'Nome Collezione': ''.join(self.nome_coll[i]),
                })
            print(tmpv)
            print(i)
            i+=1
        print("I've done!")
        
        def conditionToGo(self):
        if self.commandStop == True:
            print('Airtable already updated!')
        else:
            s.searchCsv()
            s.insertAirtable()

s = myScript()
s.searchAirtable()
s.mySqlCode()
s.conditionToGo()


