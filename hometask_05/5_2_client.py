import socket
import json
import random
import threading
from threading import RLock, Lock, Semaphore
import time
import sys

class Client():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', 8881))
        self.name = ''
        self.total_data = []
        self.running = True

        #start thread to listen
        name_t = 'listener'
        t = threading.Thread(target=self.listener,
                             name=name_t, args=(self.sock, ))
        ##t.daemon = True
        t.start()
        #start thread to send
        name_t2 = 'sender'
        t2 = threading.Thread(target=self.sender,
                              name=name_t2, args=(self.sock, ))
        ##t2.daemon = True
        t2.start()
        
    def sender(self, conn):
        self.name = self.ask_name()
        conn.sendall( self.prepare_byte_msg_to_send(name=self.name, message='') )
        ##print ("Sent invitation: {}".format(self.name) )
        time.sleep(3)
        
        while self.running:      
            data = input("Please enter something (or Bye to close): ")
            if data == 'Bye':
                self.sock.close()
                
            msg, to = self.parse_imput_text(data)
            try:
                conn.sendall( self.prepare_byte_msg_to_send(name=self.name, message=msg, to=to) )
                ##print ("Sent: {}".format( data) )
                time.sleep(3)
            except (ConnectionAbortedError, ConnectionResetError, OSError) as e:
                ##print("Disconnected from chatroom. Press <enter> to exit.")
                self.running = False
                self.sock.close()
            

        
            
    def listener(self, conn, delimiter='<end>'):
        while self.running:
            try:
                data=str( conn.recv(1024), 'utf-8')    
            except (ConnectionAbortedError, ConnectionResetError, OSError) as e:
                self.running = False
                self.sock.close()
                self.enter_catcher()
            self.data_handler(data, delimiter=delimiter)

    def data_handler(self, data, delimiter='<end>'):
        #there is a delimiter of message in data
        if data.find(delimiter) >=0:

            messages = [x for x in data.split(delimiter) if x]
            #position for messages slicing
            start_msg = 0
            end_msg = len(messages)
            
            #total_data contain some data
            if len(self.total_data) > 0:
                self.total_data.append(messages[0])
                self.print_parsed_json( ''.join(self.total_data) )
                ##print(''.join(self.total_data))
                self.total_data.clear()
                start_msg = 1
                
            #data doesn't end with delimiter
            #need to save end in total_data
            if not data.endswith(delimiter):
                self.total_data.append(messages[len(messages)-1])
                end_msg = len(messages)-1
        
            for msg in messages[start_msg:end_msg]:
                ##print(msg)
                self.print_parsed_json( msg )

        #data doesn't contain delimiter. Add data to total_data
        else:
            self.total_data.append(data)
            


    def ask_name(self):
        name = input("Enter your name, please: ")
        return name

    def print_parsed_json(self, text):
        _json = json.loads(text)
        #print private message
        if 'To' in _json:
            print("{}: [private]: {}".format(_json['Name'], _json['Message']))
        #if message contains info about disconnection, close connection 
        elif _json['Message'] == "Need to introduce yourself" or\
            _json['Message'].find("is already taken. Choose another name") >= 1:
                print("{}: {}".format(_json['Name'], _json['Message']))
                self.running = False
                self.sock.close()
                self.enter_catcher()
                
        else:
            print("{}: {}".format(_json['Name'], _json['Message']))
        
        

    def dump_json_message(self, name="", message="", to = ""):
        result = {}
        result['Name'] = name
        result['Message'] = message
        if to:
            result['To'] = to
        return json.dumps(result)

    def prepare_byte_msg_to_send(self, name="", message="", to = ""):
        json_res = self.dump_json_message(name=name, message=message, to = to)
        return bytes( json_res+'<end>', 'utf-8')

    def parse_imput_text(self, data):
        to = ""
        msg = data
        if data.startswith("user:"):
            name_position_start = len("user:")
            name_position_end = data.find(" ", name_position_start)
            to = data[name_position_start:name_position_end]
            msg = data[name_position_end+1:]
        return (msg, to) 

    def enter_catcher(self,
                      text="Disconnected from chatroom. Press <enter> to exit."):
        while True:
            data = input(text)
            if not data:
                print("Enter is pressed. The program will be closed in 3 seconds")
                time.sleep(3)
                sys.exit(1)

if __name__ == '__main__':
    cl = Client()
