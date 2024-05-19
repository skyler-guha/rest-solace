from http.server import BaseHTTPRequestHandler, HTTPServer
from functools import partial
from datetime import datetime
from typing import Callable
from queue import Queue 
from threading import Thread 
import time



class SolaceConsumerServer(BaseHTTPRequestHandler):  

    def __init__(self, killer_queue, result_queue, callback_function:Callable= None, 
                 log:bool= False, auto_stop:bool= False, *args, **kwargs):
        self.callback_function= callback_function
        self.log= log
        self.auto_stop= auto_stop
        self.killer_queue= killer_queue
        self.result_queue= result_queue

        # BaseHTTPRequestHandler calls do_GET **inside** __init__ !!!
        # So we have to call super().__init__ after setting init attributes, and pass it *args and **kwargs
        super().__init__(*args, **kwargs)


    def do_POST(self):  
        
        path= self.path
        headers= self.headers
        content_length= int(self.headers['Content-Length'])
        content= self.rfile.read(content_length)  

        if self.log:
            print(f"==========(Message received on: {datetime.now().strftime('%d/%m/%Y at %r')})==========")
            print(f"Path:-\n{path}\n")
            print(f"Content:-\n{content}\n")
            print(f"Headers:-\n{headers}")
        
        self.send_response_only(200)
        self.send_header("Content-type", "text/plain")
        self.send_header('Solace-Delivery-Mode', 'direct')
        self.end_headers()

        response_message = "Message Received!!"
        
        event = {
                    "request_type": "POST",
                    "path": path,
                    "headers": dict(headers.items()),
                    "content": content
                }
        
        def kill_function(return_value):
            self.result_queue.get() #clear the queue
            self.result_queue.put(return_value)
            self.killer_queue.put(1)

        try:
            if self.callback_function is not None:

                output = self.callback_function(event= event, 
                                                kill_function= kill_function)

                if isinstance(output, str):
                    response_message = output 

        except Exception as e:
            if self.log:
                print(f"#Error encountered while running callback function:\n{str(e)}")
        
        self.wfile.write(bytes( response_message ,"utf-8")) 
        

        if self.auto_stop:
            kill_function(event)


class Consumer:

    def startConsumer(self, host:str, port:int, 
                      callback_function:Callable= None, 
                      log:bool= True, 
                      auto_stop:bool= False,
                      timeout:int= None)->dict:
        """Start a Consumer server with a given host and port value. 
        It will receive your messages if you register it as a consumer on your Rest Delivery Point.

        Args:
            host (str): IP address for your new consumer server.
            port (int): Port to assign your new server.
            callback_function (Callable, optional): A function to call when a event (like POST request) happens. 
                                                    When called, it will receive a dictionary with the request details 
                                                    [event_type, headers, content], and a function to kill the server and return an output.
                                                    If your callback function returns a string, that string will be used as message response, 
                                                    otherwise any other type object is ignored and a default message is returned.
                                                    Defaults to None.
            log (bool, optional): To print logging info about incoming requests. Defaults to True.
            auto_stop (bool, optional): Stop after receiving a single message. Defaults to False.
            timeout (int, optional): Timeout in seconds after which the consumer will automatically shutdown.
        """

        killer_queue = Queue(maxsize= 1)
        result_queue = Queue(maxsize= 1)
        result_queue.put(dict())

        server_address = (host, port)

        handler_class = partial(SolaceConsumerServer, killer_queue, result_queue, callback_function, log, auto_stop)
        httpd = HTTPServer(server_address, handler_class)


        if log: print("Running Consumer Server...\n")

        #Creating server thread
        server_thread = Thread(target = httpd.serve_forever) 
        server_thread.start()
         
        #Add these in a thread with sleep func in the future so that the while loops do not hog cpu.
        try:
            if timeout==None:
                while True:
                    if killer_queue.get() == 1:
                        if log: print("\nStopping server to return output...")
                        httpd.shutdown()
                        httpd.server_close()
                        if log: print("Server stopped.")
                        break
            
            else:
                timeout = time.time() + timeout
                while True:
                    if killer_queue.get() == 1 or time.time() > timeout:
                        if log: print("\nStopping server to return output...")
                        httpd.shutdown()
                        httpd.server_close()
                        if log: print("Server stopped.")
                        break

        except KeyboardInterrupt: #It is expected that the user might want to only use ctrl+c to close the server in some cases.
            if log: print("\nStopping server due to keyboard interrupt...")
            httpd.shutdown()
            httpd.server_close()
            if log: print("Server stopped.")
            
        
        return result_queue.get()


    



