#importing tkinter packages
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog, messagebox, StringVar, font
from PIL import Image,ImageTk
import mysql.connector
import socket			
import random
import time
from PIL import Image,ImageTk
import zip  
from tkinter.filedialog import asksaveasfile
from PIL import Image, ImageTk
import os

#importing custom modules
import database
import var,fileoperation,AES
from Producer import Producer

#creating global variables
global root,p

#setting root to empty string
root=''

#setting background image to variable
bg='./bg.jpg'

#creating a class GUI
class GUI:
    #function accept to accept a file from the user
    def accept():
        text=root.text        
        canvas.destroy()
        window.destroy()
        window.quit()
        if text=="Encrypt a file":
            root.filename=filedialog.askopenfilename(initialdir=".../",title="Select a File",filetypes=
                (("text files","*.txt"),("python files","*.py"),("zip files","*.zip")))
        if text=="View" or text=="Share":
            root.filename=filedialog.askopenfilename(initialdir=".../",title="Select a File",filetypes=(("zip files","*.zip"),))
            Producer.produce(var.queue,['check.check()'])
        else:            
            #add check_database to q
            Producer.produce(var.queue,['database.check_database()'])
            #add Aes to q
            AES.Aes(0,fileoperation.read())
            
            GUI.setpassword()

    #function asking user to choose a file
    def acceptfile(text):
        
        root.text=text
        if text=="Exit":
                os._exit(1)
        elif text=="Factory Reset":
                
                conn=mysql.connector.connect(user='root',password='12345',host='localhost',database='hawking_comets')
                c=conn.cursor()
                c.execute('delete from decryption_keys')
                messagebox.showinfo(title='data reset',message='All data has been reset!')
                conn.commit()
                conn.close()
                return

        global window,canvas
        window=Toplevel(root)
        window.config(bg='black')
        window.geometry('200x200+580+280')
        window.resizable(width=False, height=False)
        helv36 = font.Font(family='times new roman', size=14,weight=font.BOLD)
        im=Image.open(bg)
        im = im.resize((200, 200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(im)
        canvas=Canvas(window,width=400,height=400)
        canvas.pack(fill="both",expand=False)
        canvas.create_image(0,0,image=photo,anchor="nw")
        
        button=Button(window,text="Choose a file!",command=lambda:GUI.accept())
        button.config(font=helv36)
        button.place(x=30,y=70)
        window.mainloop()

    #function that displays information using messagebox from tkinter
    def msgbox(t,m):
        messagebox.showinfo(title=t,message=m)

    #function to start a connection with the server of the same or another computer
    def connect():

        def connect2():
            with socket.socket() as s:
                # Define the port on which you want to connect
                port = 12345
                root.ip=entry.get()
                ip=root.ip
                # connect to the server on local computer
                s.connect((ip, port))
                #my private key
                b=random.randint(100000,999999)
                b=5
                G=int(s.recv(1024).decode())
                P=int(s.recv(1024).decode())
                rec=int(s.recv(1024).decode())
                send=(G**b)%P
                s.sendall(str(send).encode())
                G=int(s.recv(1024).decode())
                P=int(s.recv(1024).decode())
                rec=int(s.recv(1024).decode())
                send=(G**b)%P
                s.sendall(str(send).encode())

                key=(rec**b)%P
                digi=len(str(key))
                key=int(key*10**(19-digi))
                key=hex(key).replace('0x','')
                
                iv=(rec**b)%P
                digi=len(str(iv))
                iv=int(iv*10**(19-digi))
                iv=hex(iv).replace('0x','')

                root.key=bytes(key,'utf-8')
                root.iv=bytes(iv,'utf-8')
                
                time.sleep(0.1)
                #give permission
                s.sendall("True".encode())
                window.quit()
        window=Toplevel(root)
        window.geometry('200x200+580+280')
        window.attributes("-topmost", True)
        window.resizable(width=False, height=False)
        im=Image.open(bg)
        im = im.resize((200, 200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(im)
        canvas=Canvas(window,width=200,height=200)
        canvas.pack(fill="both",expand=True)
        canvas.create_image(0,0,image=photo,anchor="nw")
        Label(canvas,text="Enter a private IPV4 address:").place(x=15,y=55)
        entry=Entry(canvas)
        entry.place(x=40,y=80)
        hostname=socket.gethostname()   
        IPAddr=socket.gethostbyname(hostname) 
        entry.insert(0,IPAddr)
        try:
            Button(canvas,text="submit!",command=connect2).place(x=75,y=110)
        except Exception:
            Label(canvas,"Try again:(").place(x=0,y=0)
        window.mainloop()
        window.destroy()
        
    #function to display page 1 of extra information
    def page1():
        window=Toplevel(root)
        window.config(bg='black')
        window.geometry('800x400+270+180')
        im=Image.open(bg)
        im = im.resize((800, 400), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(im)
        canvas=Canvas(window,width=800,height=400)
        canvas.pack(fill="both",expand=True)
        canvas.create_image(0,0,image=photo,anchor="nw")
        
        helv36 = font.Font(family='times new roman', size=15,weight=font.BOLD)
        Label(canvas,text='Hawking comet is a software that uses encryption system called',bg='black',fg='white',font=helv36).place(x=120,y=60)
        Label(canvas,text='AES to encrypt and decrypt files which',bg='black',fg='white',font=helv36).place(x=200,y=100)
        Label(canvas,text='are locked using a zip file , providing extremely strong levels of ',bg='black',fg='white',font=helv36).place(x=130,y=140)
        Label(canvas,text='security, ideal for sensitive files. It also gives the user the',bg='black',fg='white',font=helv36).place(x=150,y=180)
        Label(canvas,text='option to share files, view and edit their files.',bg='black',fg='white',font=helv36).place(x=200,y=220)

        b=Button(canvas,text='next page?',font=helv36,command=GUI.page2)
        b.place(x=260,y=260)
        b=Button(canvas,text='Exit!',font=helv36,command=lambda: window.quit())
        b.place(x=460,y=260)
        window.mainloop()
        window.destroy()

    #function to display page2 of extra information
    def page2():
        window=Toplevel(root)
        window.config(bg='black')
        window.geometry('800x400+270+180')
        im=Image.open(bg)
        im = im.resize((800, 400), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(im)
        canvas=Canvas(window,width=800,height=400)
        canvas.pack(fill="both",expand=True)
        canvas.create_image(0,0,image=photo,anchor="nw")

        helv36 = font.Font(family='times new roman', size=15,weight=font.BOLD)
        Label(canvas,text='Encrypt: Encodes and locks a particular text file',bg='black',fg='white',font=helv36).place(x=120,y=60)
        Label(canvas,text='View: Allows yoou to check/make changes to an already encrypted file.',bg='black',fg='white',font=helv36).place(x=120,y=100)
        Label(canvas,text='Share: Allows you to share an encrypted file in your private Network.',bg='black',fg='white',font=helv36).place(x=120,y=140)
        Label(canvas,text='Exit: Exits the app',bg='black',fg='white',font=helv36).place(x=120,y=180)
        Label(canvas,text='Factory reset: Resets all data stored',bg='black',fg='white',font=helv36).place(x=120,y=220)


        b=Button(canvas,text='Previous page?',font=helv36,command=lambda: window.quit())
        b.place(x=300,y=260)
        window.mainloop()
        window.destroy()

    #function to display the main screen of the program
    def main_screen():

        global label,root,q

        root=Tk()
        root.title("Hawcking Comets")
        root.geometry('1370x950+-7+0')
        root.resizable(width=False, height=False)
        label = tk.Label(root)
        label.place(x=-200,y=-200)

        #adding to queue
        Producer.produce(var.queue,['database.test_database()'])
        #C:\Users\Tarun\OneDrive\Desktop\Hawkingcomets\mainscreen_image.jpg
        im=Image.open('./mainscreen_image.jpg')
        im = im.resize((1800, 950), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(im)
        label.configure(image=photo)
        label.image=photo
        label1=Label(root,text="Welcome to Hawking Comets",font=("times new roman",35,"bold","italic"),bg="black",fg="white").place(x=425,y=55)
        
        helv36 = font.Font(family='times new roman', size=15,weight=font.BOLD)
        clicked=StringVar()
        clicked.set('Choose an option.')
        l=["Encrypt a file","View","Share","Exit","Factory Reset"]
        drop=OptionMenu(root,clicked,*l,command=GUI.acceptfile)
        helv36 = font.Font(family='times new roman', size=20,weight=font.BOLD)
        drop.config(bg = "black", fg= "white",font=helv36)
        menu = root.nametowidget(drop.menuname)
        helv36 = font.Font(family='times new roman', size=15,weight=font.BOLD)
        menu.config(font=helv36)
        drop.place(x=550,y=400)
        button=Button(root,text="Click here to know more!",bg='black',fg='white',font=helv36,command=GUI.page1)
        button.place(x=560,y=500)

        #function to process GUIqueue and execute them accordingly
        def processGUIQ():
            if var.GUIqueue.empty():
                root.after(1,processGUIQ)
            else:
                f=var.GUIqueue.get()
                fname=f[0]
                i=1
                while i<len(f):
                    exec(f[i])
                    i=i+1
                    
                exec(fname)
                var.flag=True
                root.after(1,processGUIQ)
            
        processGUIQ()
        root.mainloop()
        os._exit(1)

    #function to ask user to enter a password for an encrypted zipfile.
    def password():
        def submit():
                global p
                p=pwd.get()
                try:
                    zip.extract(p)
                    window.destroy()
                    window.quit()
                except:
                    Label(canvas,text="Try again:( ", font = ('calibre',10,'bold')).place(x=25,y=166)
            
        window=Toplevel(root)
        window.config(bg='black')
        window.geometry('400x300+460+220')
        im=Image.open(bg)
        im = im.resize((400, 300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(im)
        canvas=Canvas(window,width=300,height=300)
        canvas.pack(fill="both",expand=True)
        canvas.create_image(0,0,image=photo,anchor="nw")
        pwd=StringVar()
        label=Label(canvas,text="Filename: ", font = ('calibre',10,'bold')).place(x=25,y=113)
        label=Label(canvas,text=root.filename, font = ('calibre',10,'bold')).place(x=107,y=113)
        passw_label = Label(canvas, text = 'Password:', font = ('calibre',10,'bold')).place(x=25,y=138)
        pwd_entry=Entry(canvas, textvariable = pwd, font = ('calibre',10,'normal'), show = '*').place(x=107,y=138)
        subm=Button(canvas,text = 'Submit!',command=submit).place(x=110,y=166)
        window.mainloop()
        return

    #function to set a password for the encrypted zip file
    def setpassword():
        
        #function to accept password
        def submit():

            password=pwd.get()
            password2=pwd2.get()

            if password!='':
                if password==password2:
                    #Password accepted!
                   
                    #destroy window                   
                    window.destroy()

                    #produce zip.zip(password) to queue
                    Producer.produce(var.queue,['zip.zip(password)','password='+'"'+password+'"'])
                    window.quit()
                                
                else:
                    label=Label(canvas,text="Try Again:(").place(x=45,y=166)
            else:
                label=Label(canvas,text="Try Again:(").place(x=45,y=166)
        
        
        window=Toplevel(root)
        window.config(bg='black')
        window.geometry('300x300+540+220')
        window.resizable(width=False, height=False)
        
        im=Image.open(bg)
        im = im.resize((300, 300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(im)
        canvas=Canvas(window,width=300,height=300)
        canvas.pack(fill="both",expand=True)
        canvas.create_image(0,0,image=photo,anchor="nw")

        pwd=StringVar()
        pwd2=StringVar()
        passw_label = Label(canvas, text = 'Enter a Password', font = ('calibre',10,'bold')).place(x=15,y=113)
        passw_label2 = Label(canvas, text = 'ReEnter Password', font = ('calibre',10,'bold')).place(x=15,y=138)
        pwd_entry=Entry(canvas, textvariable = pwd, font = ('calibre',10,'normal'), show = '*').place(x=140,y=113)
        pwd_entry2=Entry(canvas, textvariable = pwd2, font = ('calibre',10,'normal'), show = '*').place(x=140,y=138)
        subm=Button(canvas,text = 'Submit!',command=submit).place(x=115,y=166)
        window.mainloop()

    #function that shows an error message 
    def showerror(t,m):
            messagebox.showerror(title=t,message=m)

    #function thats aks a yes or no message
    def askyesno(t,m):
            choice=messagebox.askyesno(title=t,message=m)
            return choice

    #function that makes the app wait while the user makes any required changes
    def wait():
        print(root.filename)
        
        window=Toplevel(root)
        window.geometry('200x200+580+280')
        window.resizable(width=True, height=False)
        im=Image.open(bg)
        im = im.resize((600, 200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(im)
        canvas=Canvas(window,width=600,height=200)
        canvas.pack(fill="both",expand=True)
        canvas.create_image(0,0,image=photo,anchor="nw")
        label=Label(canvas,text="EDIT YOUR FILE!")
        label.place(x=55,y=40)
        label=Label(canvas,text="YOUR FILE IS STORED IN: "+root.filename)
        label.place(x=30,y=85)
        close=Button(canvas,text='Click me when done!',command=lambda:window.quit())
        close.place(x=40,y=130)
        window.mainloop()
        window.destroy()
    #function that saves a zip file to the user's choice of destination
    def saveas():
        window=Toplevel(root)
        window.geometry('200x200+580+280')
        window.resizable(width=False, height=False)
        im=Image.open(bg)
        im = im.resize((200, 200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(im)
        canvas=Canvas(window,width=200,height=200)
        canvas.pack(fill="both",expand=True)
        canvas.create_image(0,0,image=photo,anchor="nw")
        
        #subfunction to save the file
        def save():            
            files = [("zip files","*.zip")]
            file = asksaveasfile(filetypes = files, defaultextension = files)
            root.file=file.name
            entry.delete(0,"end")
            entry.insert(0,file.name)
            window.lift()
            
        label=Label(canvas,text="Path:")
        label.place(x=15,y=65)
        entry=Entry(canvas)
        entry.place(x=55,y=65)
        oupt = Button(canvas, text = 'Browse', command = lambda : save())
        oupt.place(x=75,y=90)
        oupt = Button(canvas, text = 'Save', command = lambda: window.quit())
        oupt.place(x=83,y=125)
        window.mainloop()
        window.destroy()

    #A=function to display a confirmation window
    def confirmation():
        window=Toplevel(root)
        window.geometry('500x500+430+100')
        window.resizable(width=False, height=False)
        im=Image.open(bg)
        im = im.resize((500, 500), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(im)
        canvas=Canvas(window,width=200,height=200)
        canvas.pack(fill="both",expand=True)
        canvas.create_image(0,0,image=photo,anchor="nw")
        label1=Label(canvas,text='FILE ENCRYPTED AND STORED IN ', font = ('calibre',10,'bold'))
        label1.place(x=125,y=180)
        label1=Label(canvas,text=root.file, font = ('calibre',10,'bold'))
        label1.place(x=110,y=205)
        label2=Label(canvas,text='Thank you!', font = ('calibre',10,'bold'))
        label2.place(x=200,y=230)
        close=Button(canvas,text='Close', font = ('calibre',10,'bold'),command=lambda: window.quit())
        close.place(x=215,y=255)
        window.mainloop()
        window.destroy()
        #add to q
        Producer.produce(var.queue,['database.database()'])
