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

        item_list = enumerate(self.at.get_all()) #enumerate table items
        last_item = self.at.get_all()[-1] #take the last item
        #enumerate works, but working with createdTime could be more exact
        print(last_item)
        dateAirtable = last_item['fields']['Date'] #gets date value
        print(dateAirtable)
        self.toDate = datetime.strptime(dateAirtable, '%d/%m/%Y').strftime('%Y-%m-%d') #here it takes the string in Date and parse it as a date, then it convert it into a string with the format that will match the mySQL format for dates
        print(self.toDate)

    def mySqlCode(self):
        config = {
            'user': XXX,
            'password': XXX,
            'host': XXX,
            'database': XXX
        }

        cnx = cur = None
        try:
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()
            query = ("SELECT Id, WorkedFilePath, FileRowCount, DateCreation FROM mediaimportrequest WHERE DateCreation>%s") #%s is the variable
            dateLimit = self.toDate
            try: #try to catch the not updated items on Airtable based on dateLimit
                cursor.execute(query, (dateLimit,)) #assign dateLimit to the variable, COMMA IS IMPORTANT
                for (Id,FileRowCount,WorkedFilePath,DateCreation) in cursor:
                    print("Id: {}, Items:{}, File: {}, DateCreation: {}".format(Id,FileRowCount,WorkedFilePath,DateCreation))
                    self.date = DateCreation.isoformat() #the date format is converted to isoformat
                    self.date = datetime.strftime(DateCreation, '%d/%m/%Y') #and now the isoformat is converted into a string with the right format
                    self.num_risorse = WorkedFilePath
                    self.attachment = FileRowCount
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
            newFile = self.attachment.replace("E:\\adm", "http://url.it").replace("\\","/")
            print(newFile)
            s = requests.Session() #for Session() see http://docs.python-requests.org/en/master/user/advanced/
            download = s.get(newFile) #get the file from url
            decoded_content = download.content.decode('utf-8') #decode in utf-8

            csvFile = csv.DictReader(decoded_content.splitlines(), delimiter='\t')  #read the csv file and set delimiter, splitlines saves the day
            csvFile.fieldnames = [field.strip().lower() for field in csvFile.fieldnames]
            
            self.publisher = [] #create a list for each value we want
            self.tipologia = []
            self.nome_coll = []

            for row in csvFile:
                self.tipologia.append(row['type']) #this append the values from the right column to the list
                self.publisher.append(row["publisher"])
                self.nome_coll.append(row["nome_coll"])

            print(set(self.tipologia)) #set gets the unique values of a list
            print(set(self.publisher))
            print(set(self.nome_coll))

    def insertAirtable(self): #insert records from mySQL metadata
        records = self.at.insert({ 
            'Date': self.date,
            'Numero di risorse': self.num_risorse,
            'Attachments': self.attachment,
            'Tipologia': ';'.join(list(set(self.tipologia))), #';'.join convert the list into a string, with ; for multiple values
            'Publisher': ';'.join(list(set(self.publisher))),
            'Nome Collezione': ';'.join(list(set(self.nome_coll))),
            })
        print(records)
    
    def conditionToGo(self): #function that make the script stop or continue based on commandStop
        if self.commandStop == True:
            print('Airtable already updated!')
        else:
            s.searchCsv()
            s.insertAirtable()

s = myScript()
s.searchAirtable()
s.mySqlCode()
s.conditionToGo()


