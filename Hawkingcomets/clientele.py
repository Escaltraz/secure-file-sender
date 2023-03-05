#method to share a zip file
def share():
    #import required modules
    import http.server,socketserver,os
    #import local custom module
    import GUI

    #save current working directory to a variable curdir
    curdir=os.getcwd()
    #change cuurrent directory
    os.chdir('c:/')
    
    #class QuietHandler
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            global my_server,close_connection   
            log=("%s - -{%s} %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))
            
            if GUI.root.ip not in log:
                close_connection=True
                self.handle()
            else:
                close_connection=False
                
        def do_GET(self):
            if self.path == '/':
                self.path = GUI.root.file.replace('\\','/')
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

        def handle(self):
            
            global close_connection
            self.handle_one_request()
            if not close_connection:
                #raise KeyboardInterrupt to shutdown server
                raise KeyboardInterrupt
        
    #create global variables
    global my_server,close_connection
    close_connection=True

    #assigning a fixed port number
    PORT = 5000


    my_server = socketserver.TCPServer(("", PORT), QuietHandler)
    #import local custom module
    import server

    #try block to catch KeyboardInterrupt
    try:
       my_server.serve_forever()
    except KeyboardInterrupt:
        #shutodown server
        my_server.shutdown()
        my_server.server_close()
        
        #remove file from system
        os.remove(GUI.root.file)

    #change directory back to curdir
    os.chdir(server.curdir)
