#import required modules
import os
import requests
import threading
import time
import socket
import random

#import local custom modules
from Producer import Producer
import var,database,GUI
import GUI


#create global variable
global curdir

#function functions that performs functions like rename files
#add checks if it already exists
def functions(i):
        
        global u,ip
        global curdir
        global Down
        curdir=os.getcwd()
        ip=i
        u=os.path.join(curdir,'download.zip')

        #function rename_file that renames a file
        def rename_file():
            global u
            path=os.path.split(u)
            name=path[1].replace('.zip','(1).zip')
            u=os.path.join(path[0],name)
            check()
            
        #function check that checks if a file already exists in a location
        def check():
            global u
            if os.path.isfile(u):
               rename_file()
            else:
               GUI.root.archive=u
            
        #call check function
        check()

        #call download function
        download(ip)
        return

#function download to download a zip file
def download(ip):

    url='http://'+ip+':5000/'
    r = requests.get(url)

    with open(GUI.root.archive, "wb") as zip:
        zip.write(r.content)
    
    #update database
    database.update_database(GUI.root.archive.replace('\\','/'))

    #produce GUI.msgbox to GUIqueue
    Producer.produce(var.GUIqueue,['GUI.msgbox(title,message)',"title='Download manager'","message='Downloaded in path: "+GUI.root.archive.replace('\\','/')+"'"])

#function to create a server that accepts files
def Server():
        global flag,ip

        HOST = ''
        PORT = 12345

        #Private key 
        P=random.randint(5000000000000000000,9999999999999999999)
        P2=random.randint(5000000000000000000,9999999999999999999)

        #public key 2
        G=random.randint(100000,999999)
        G2=random.randint(100000,999999)

        a=random.randint(100000,999999)
        send=(G**a)%P
        send2=(G2**a)%P2


        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
        
            #accept a connection
            conn, addr = s.accept()
            ip=addr[0]
            with conn:
                conn.sendall(str(G).encode())
                time.sleep(0.1)
                conn.sendall(str(P).encode())
                time.sleep(0.1)
                conn.sendall(str(send).encode())
                rec=int(conn.recv(1024))
                key=(rec**a)%P
                digi=len(str(key))
                key=int(key*10**(19-digi))
                key=hex(key).replace('0x','')
                time.sleep(0.1)
                
                conn.sendall(str(G2).encode())
                time.sleep(0.1)
                conn.sendall(str(P2).encode())
                time.sleep(0.1)
                conn.sendall(str(send2).encode())
                rec=int(conn.recv(1024))
                iv=(rec**a)%P2
                digi=len(str(iv))
                iv=int(iv*10**(19-digi))
                iv=hex(iv).replace('0x','')
                
                #get permission
                permission=bool(conn.recv(1024))
        
        
        GUI.root.key=bytes(key,'utf-8')
        GUI.root.iv=bytes(iv,'utf-8')

        #call function functions
        functions(ip)

        #keeps the thread going
        threading.Thread(target=Server).start()
