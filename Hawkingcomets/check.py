#importing required module
import zipfile
import os
import pyminizip


#importing local custom modules
import zip
import database
import fileoperation,AES,GUI
from Producer import Producer

#function to check the validity of a zip file
#and perform required operations
def check():
    #try block
    try:
        #opening zip file and performing required operations
        with zipfile.ZipFile(GUI.root.filename) as zf:
            
            #going through zf.infolist one by one and checking if it is encrypted
            for zinfo in zf.infolist():
                is_encrypted = zinfo.flag_bits & 0x1
                
                #if it is encrypted, then perform required operations
                if is_encrypted:
                    #close zip file
                    zf.close()

                    #check for value of GUI.root.text
                    if GUI.root.text=='View':
                        #assign value to flag variable
                        import var
                        var.flag=False

                        #add GUI.password() to GUIqueue
                        Producer.produce(var.GUIqueue,['GUI.password()'])

                        #wait until GUI.password() has been executed
                        while not var.flag:
                            pass

                        #read from file
                        fileoperation.read()

                        #decrypt file
                        decd=AES.Aes(1,None)

                        #write to file
                        fileoperation.write(decd)

                        #assign value to flag variable
                        var.flag=False

                        #produce GUI.wait() to GUIqueue
                        Producer.produce(var.GUIqueue,['GUI.wait()'])
                        #wait until GUI.wait() has finished executing
                        while not var.flag:
                            pass
                        
                        #read from file
                        fileoperation.read()

                        #encrypt file
                        AES.Aes(0,None)
                        #zip the file
                        zip.zip(GUI.p)
                        #update database
                        database.update_database()
                                
                    else:
                        
                        #set value to var.flag
                        import var
                        var.flag=False
                        #produce GUI.password() to var.GUIqueue
                        Producer.produce(var.GUIqueue,['GUI.password()'])
                        #wait until above function has finished executing
                        while not var.flag:
                            pass

                        #read from file
                        fileoperation.read()
                        #decrypt file
                        decd=AES.Aes(1,None)
                        GUI.root.text=decd

                        #assign value to var.flag
                        var.flag=False
                        #produce GUI.connect() to var.GUIqueue
                        Producer.produce(var.GUIqueue,['GUI.connect()'])
                        #wait until above function has finished executing
                        while not var.flag:
                            pass
                    
                        #Encrypt file using key generated from connect method in file GUI
                        AES.Aes(2,None)
                        #create a temporary file to share
                        GUI.root.file=os.path.abspath('./temp.zip')
                        import warnings
                        warnings.filterwarnings("ignore", category=DeprecationWarning) 
                        
                        #compress file
                        pyminizip.compress(GUI.root.filename, None, GUI.root.file,GUI.p,5)
                        os.remove(GUI.root.filename)
                        import clientele,threading
                        threading.Thread(target=clientele.share).start()
                                
    except zipfile.BadZipFile:
        import var
        #produce GUI.msgbox() to GUIqueue
        Producer.produce(var.GUIqueue,['GUI.msgbox(title,message)',"title='Invalid file'","message='File Not Encrypted!! Choose another file.'"])