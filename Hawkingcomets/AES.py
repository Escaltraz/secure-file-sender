#import modules
from Cryptodome.Cipher import AES
import base64
import random

#importing local custom modules
import GUI,database,fileoperation

#function to implement AES type encryption
def Aes(i,text):
    L=["encrypt()","decrypt()","encrypt_network()"]

    #call respective functions
    value=eval(L[i])

    #return value
    return value    

#function to perform normal encryption
def encrypt():

    i=1152921504606846976
    f=18446744073709551616
    GUI.root.key=bytes(hex(random.randint(i,f)).replace('0x',''),'utf-8')
    GUI.root.iv=bytes(hex(random.randint(i,f)).replace('0x',''),'utf-8')

    #create object
    aes = AES.new(GUI.root.key, AES.MODE_CFB, GUI.root.iv)

    #encrypting
    encd=""
    text=bytes(GUI.root.text,'utf-8')
    encd = aes.encrypt(text)
    encd=base64.b64encode(encd)
    ciphertext=encd.decode('utf-8')

    #write to file
    fileoperation.write(ciphertext)

#function to decrypt   
def decrypt():

    #Assigning variables default value
    GUI.root.iv=""
    GUI.root.key=""

    #read from database
    database.read_database()

    #convert ciphertext
    ciphertext=bytes(GUI.root.text,'utf-8')

    #creating object
    aes = AES.new(GUI.root.key, AES.MODE_CFB, GUI.root.iv)
    
    #decrypting
    data=ciphertext
    decd=base64.b64decode(data)
    decd=aes.decrypt(decd)
    decd=decd.decode('utf-8')
    return decd

#function to encrypt a file to share it across a network
def encrypt_network():

    #create object
    aes = AES.new(GUI.root.key, AES.MODE_CFB, GUI.root.iv)
    
    #encrypting
    encd=""
    text=bytes(GUI.root.text,'utf-8')
    encd = aes.encrypt(text)
    encd=base64.b64encode(encd)
    ciphertext=encd.decode('utf-8')

    #write ciphertext to file
    fileoperation.write(ciphertext)

    