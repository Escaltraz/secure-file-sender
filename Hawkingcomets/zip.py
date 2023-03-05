
# importing required modules
import pyminizip
import warnings
import os
from zipfile import ZipFile

#import custom modules
import GUI
import var,GUI
from Producer import Producer

#function to zip a file
def zip(password):
        warnings.filterwarnings("ignore", category=DeprecationWarning) 
        
        
        
        #assign value to var.flag
        var.flag=False
        #produce GUI.saveas() to GUIqueue
        Producer.produce(var.GUIqueue,['GUI.saveas()'])
        #wait until above function completes execution
        while not var.flag:
            pass
        
        inpt = GUI.root.filename
        
        # compress level
        com_lvl = 5
        
        # compressing file
        pyminizip.compress(inpt, None, GUI.root.file,password, com_lvl)
        os.remove(GUI.root.filename)

        #produce GUI.confirmation() to GUIqueue
        Producer.produce(var.GUIqueue,['GUI.confirmation()'])

#function to extract a file
def extract(password):  
        #create global variable
        global z

        # specifying the zip file name
        file_name = GUI.root.filename
        files=[]

        # opening the zip file in READ mode
        z=ZipFile(file_name, 'r')
                
        #extracting all the files
        z.extractall(path='./',pwd=bytes(password,'utf-8'))
        
        files=z.namelist()
        z.close()
        
        GUI.root.archive=GUI.root.filename
        GUI.root.filename=GUI.os.path.join('./',files[0])
        GUI.root.filename=os.path.abspath(GUI.root.filename).replace('\\','/')
