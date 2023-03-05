#function to read data from a file
def read():
        #import local custom module
        import GUI
        data=""

        #read data from file
        with open(GUI.root.filename,'r') as file:
                data=file.read()
        GUI.root.text=data
        return

#function to write data from a file
def write(data):
        #import local custom file
        import GUI

        #write data into file
        with open(GUI.root.filename,'w') as file:
            file.write(data)