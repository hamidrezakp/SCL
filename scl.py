#!/usr/bin/python3
#Written by Hamid reza kaveh pishghadam <hamidreza[at]hamidrezakp.ir>
#Date : Tue May 15 03:39 2018
#License : Apache v2
import datetime , pickle, getpass
from hashlib import md5
from sys import argv

#Settings
#manage-mode password
_Pass = b'q\xe3l\x8d^\x90\xe1\xe5\x07(]G\x08eLi'
#limit of attemps in a cycle in seconds
_Limit = 5
#limit time must be between attemps in seconds
_Tbe = 5
#duration of a cycle
_Tbl = 60
#where is db file
_Settings_File = 'DB.pkl'

#global array
array = []


#save data in db file
def save(array):
    f = open(_Settings_File, 'wb')
    pickle.dump(array, f)

#load data from db file
def load():
    try:
        f = open(_Settings_File, 'rb')
        return pickle.load(f)
    except:
        print("There is not any previous DB file saved.make a DB in manage-mode.")
        exit(-1)
    

#return time to seconds
def gettime():
    time = datetime.datetime.now()
    return (time.toordinal() * 86400) + (time.hour * 3600) + (time.minute * 60) + time.second

#user class defination
class user:
    name = ''
    access = False
    last = 0
    fic = 0
    do = 0

    def deactive(self):
        self.access = False

    def active(self):
        self.access = True

    def auth(self):
        
        #store time in t
        t = gettime()

        #return 0 if user have not access to execute
        if self.access == False:
            return 0
        
        #return 1 if there is no last execution
        elif self.fic == 0 and self.last == 0:
            self.fic = self.last = t
            self.do = self.do + 1
            return 1

        #return 0 if had reach the maximum execuation time
        elif self.do >= _Limit:
            if (t - self.fic) > _Tbl:
                self.fic = self.last = t
                self.do = 1
                return 1
            else:
                return 0
        
        #return 0 if attemp in less than 5 seconds from last time        
        elif (t - self.last) < _Tbe:
            return 0
        
        #return 1 if it be allowd
        else:
            self.last = t
            self.do = self.do + 1
            return 1
    
    #construction method for class user
    def __init__(self, n, acs=False):
        self.name = n 
        self.access = acs


##Print array in manage mode
def aprint():
    x = 0
    print("\n\nID - Name - Access\n" + 20*'=')
    for i in array:
        print(str(x) + ' - ' + i.name + ' - ' + str(i.access))
        x = x+1

##Login to manage mode
def login():
    upass = getpass.getpass()
    passmd5 = md5(upass.encode("utf-8")).digest()
    if passmd5 != _Pass:
        return 0
    return 1

##Manage DB function
def mandb():
    global array
    if not login():
        print("Wrong password!")
        exit(-1)

    print("####### Welcome to Manage-Mode #######\n *\'rX\' to remove user with id X,\n *\'aX\' to deactive permession of user with id X ,\n *\'dX\' to deactive permession of user with id X ,\n *\'i\' to enter new user ,\n *\'ls\' to print list of users and\n *\'wq\' for save and exit\n")
    while True:

        op = input("(manage-mode):")
        
        if op == '':
            continue
        elif op == 'wq':
            save(array)
            exit(0)
        elif op == 'i':
            uname = input("Enter name of new user : ")
            newUser = user(uname)
            array.append(newUser)
        elif op == 'ls':
            aprint()
        elif op[0] == 'r':
            del array[int(op[1:])]
        elif op[0] == 'd':
            array[int(op[1:])].deactive()
        elif op[0] == 'a':
            array[int(op[1:])].active()
        else:
            print('Wrong command!')

#check that user have permession or not
def check():
    uname = getpass.getuser()
    for i in array:
        if i.name == uname:
            print(i.auth())
            return
    print("You have not permession to execute command.")
    exit(-1)

#Main menu of program
def mainMenu():
    global array
    arg = argv[1:]
    
    if len(arg) < 1:
        array = load()
        check()
    elif arg[0] == '-mm':
        mandb()
    else:
        print("Wrong argument, just use without argument.") 
    save(array)


mainMenu()
