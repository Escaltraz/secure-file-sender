#from requests.models import parse_header_links
#import local custom modules
from Producer import Producer
import GUI,var
import mysql.connector
from base64 import b64encode, b64decode

#function to check if file is already encrypted
def check_database():
        
        conn=mysql.connector.connect(user='root',password='12345',host='localhost',database='hawking_comets')
        c=conn.cursor()
        c.execute('SELECT * from decryption_keys')
        l=c.fetchall()
        for i in l:
            if GUI.root.filename in i:
                    title='Invalid file'
                    message='File already Encrypted!! Choose another file.'
                    GUI.GUI.msgbox(title,message)

                    #add to queue
                    Producer.produce(var.GUIqueue,['GUI.acceptfile(gui.root.text)'])
                    
        conn.commit()
        conn.close()

#function to enter values into database
def database():
        
        key=b64encode(GUI.root.key).decode('utf-8')
        iv=b64encode(GUI.root.iv).decode('utf-8')

        conn=mysql.connector.connect(user='root',password='12345',host='localhost',database='hawking_comets')
        c=conn.cursor()
        try:
                c.execute('INSERT into decryption_keys values("'+GUI.root.file+'","AES","'+key+'","'+iv+'")')
        except mysql.connector.errors.IntegrityError:
                pass
        
        conn.commit()
        conn.close()

#function to read values from database
def read_database():
        
        conn=mysql.connector.connect(user='root',password='12345',host='localhost',database='hawking_comets')
        c=conn.cursor()
        c.execute('select* from decryption_keys where fsave='+'"'+GUI.root.archive+'"')
        l=c.fetchall()[0]
        GUI.root.key=b64decode(bytes(l[2],'utf-8'))
        GUI.root.iv=b64decode(bytes(l[3],'utf-8'))
        conn.commit()
        conn.close()

#function to check if any files have been misplaced
def test_database():
        #import modules
        import mysql.connector
        import os

        conn=mysql.connector.connect(user='root',password='12345',host='localhost',database='hawking_comets')
        c=conn.cursor()
        c.execute('SELECT * from decryption_keys')
        l=c.fetchall()
        if len(l)==0:
            return
        
        for i in l:
            j=i[0]
            flag=os.path.isfile(j)
            choice=''
            
            if flag==False:
                Producer.produce(var.GUIqueue,['GUI.showerror(title,message)',"title='File not found'","message='File not found!'"])
                Producer.produce(var.GUIqueue,['GUI.askyesno(title,message)',"title='File not found'","message='Delete records?'"])
                var.flag=False
                while True:
                    if var.flag:
                        break
                if choice==True:
                    c.execute('DELETE FROM decryption_keys WHERE fsave="'+j+'"')
                    conn.commit()
                    break
                elif choice==False:
                    Producer.produce(var.GUIqueue,['GUI.msgbox(title,message)',"title='Confirmation'","message='Replace file and Press OK to continue.'"])
                    break
                
        else:
            conn.commit()
            conn.close()
            return
        test_database()

#function to update values in a database
def update_database(file=1):
        #create/open database
        import GUI
        if file==1:
            file=GUI.root.file
        import mysql.connector
        from base64 import b64encode
        
        key=b64encode(GUI.root.key).decode('utf-8')
        iv=b64encode(GUI.root.iv).decode('utf-8')

        conn=mysql.connector.connect(user='root',password='12345',host='localhost',database='hawking_comets')
        c=conn.cursor()

        #check if root.file exists!!
        c.execute('select* from decryption_keys where fsave="'+file+'"')
        if len(c.fetchall())==0:
                c.execute('insert into decryption_keys values("'+file+'","AES","'+key+'","'+iv+'")')
                conn.commit()
                conn.close()
        else:
                c.execute('UPDATE decryption_keys set k="'+key+'",iv="'+iv+'" where fsave="'+file+'"')
                conn.commit()
                conn.close() 
        return
