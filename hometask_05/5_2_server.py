import socket
import threading
import sys
import json

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.clients = {}
        self.total_data = []

    def listen(self):
        self.sock.listen(5)
        print('Server started on {}:{}'.format(self.host, self.port))
        while True:
            client, address = self.sock.accept()
            #client.settimeout(60)
            threading.Thread(target = self.listenToClient,
                             args = (client,address)).start()
            #add client to pull
            self.clients[client] = '' 

    def listenToClient(self, client, address):
        while True:
            try:
                data = str(client.recv(1024), 'utf-8')
            except:
                #print("Unexpected error:", sys.exc_info()[0])
                if client in self.clients:
                    client.close()
                    del self.clients[client]
                    break
            if data and client in self.clients:
                ##print("Received: " + data)
                self.data_handler(data, client)
            else:
                if client in self.clients:
                    client.close()
                    del self.clients[client]
                break
                

    def send_to_all(self, text):
        ##print("Server to all clients: {}".format(text))
        for cl in self.clients:
            cl.sendall(bytearray(text, "utf-8"))

    def send_to_all_except_one(self, text, client_to_exclude):
        ##print("Server to all clients: {}".format(text))
        for cl in self.clients:
            if cl == client_to_exclude:
                continue
            cl.sendall(bytearray(text, "utf-8"))

    def send_to_client(self, text, client):
        if client in self.clients:
            ##print("Server to client : {}".format( text))
            client.sendall(bytearray(text, "utf-8"))

    def send_to_client_by_name(self, text, name):
        
        client = ''
        for _client, _name in self.clients.items():
            if _name == name:
                client = _client
                break
        ##print("Server to client {}: {}".format(name, text))
        client.sendall(bytearray(text, "utf-8"))

    #    if json['to']:
     #       print('To -> ' + json['to'])
      #      self.send_to_client_by_name(text, json['to'])
      #  else:
       #     self.send_to_all(text)
            
    def load_json_message(self, text):
        _json = json.loads(text)
        ##print("JSON: {}".format(_json))
        return _json

    def dump_json_message(self, name="", message="", to = ""):
        result = {}
        result['Name'] = name
        result['Message'] = message
        if to:
            result['To'] = to
        return json.dumps(result)

    def get_name_from_text(self, text):
        _text = text[:text.find('<end>')]
        json1 = json.loads(_text)
        return json1['Name']
        


    def data_handler(self, data, client, delimiter='<end>'):
        #there is a delimiter of message in data
        if data.find(delimiter) >=0:

            messages = [x for x in data.split(delimiter) if x]
            #position for messages slicing
            start_msg = 0
            end_msg = len(messages)
            
            #total_data contain some data
            if len(self.total_data) > 0:
                self.total_data.append(messages[0]) 
                self.response_handler( ''.join(self.total_data), client )
                self.total_data.clear()
                start_msg = 1
                
            #data doesn't end with delimiter
            #need to save end in total_data
            if not data.endswith(delimiter):
                self.total_data.append(messages[len(messages)-1])
                end_msg = len(messages)-1
        
            for msg in messages[start_msg:end_msg]:
                ##self.send_to_all( (msg+'<end>')  )
                self.response_handler( msg, client )

        #data doesn't contain delimiter. Add data to total_data
        else:
            self.total_data.append(data)
            


    def response_handler(self, text, client):
        
        json_obj = self.load_json_message(text)
        #introduction message
        if not json_obj['Message']:
            #name is empty - cancel
            if not json_obj['Name']:
                message = "Need to introduce yourself"
                text_to_send = self.dump_json_message(name = 'Server', message = message ) + '<end>'
                self.send_to_client(text_to_send, client)
                if client in self.clients:
                    del self.clients[client]
                    client.close()
            #name exists in list - cancel   
            elif json_obj['Name'] in self.clients.values():
                message = 'Name {} is already taken. Choose another name'.format(json_obj['Name'])
                text_to_send = self.dump_json_message(name = 'Server', message = message ) + '<end>'
                self.send_to_client(text_to_send, client)
                if client in self.clients:
                    client.close()
                    del self.clients[client]
            #register name of client - OK
            else:
                self.clients[client] = json_obj['Name']
                #send new client invitation message
                message = 'Welcome to chat, {}'.format(json_obj['Name'])
                text_to_send = self.dump_json_message(name = 'Server', message = message ) + '<end>'
                self.send_to_client(text_to_send, client)
                print('Added new client: {}'.format(json_obj['Name']))
                #send other about new client
                msg_invitation_to_other = "{} entered chat.".format(json_obj['Name'])
                text_to_send = self.dump_json_message(name = 'Server',
                                                      message = msg_invitation_to_other ) + '<end>'
                self.send_to_all_except_one(text_to_send, client)
                print('Client <{0}> send to all: {0} entered chat!'.format(json_obj['Name']))
                
        #usual message
        else:
            #private message
            if 'To' in json_obj:
                text_to_send = self.dump_json_message(name = json_obj['Name'],
                                                      message = json_obj['Message'],
                                                      to = json_obj['To'] ) + '<end>'
                self.send_to_client_by_name(text_to_send, json_obj['To'])
            #message to all
            else:
                response = text + '<end>'
                self.send_to_all(response )
                print('Client <{}> send to all: {}'.format(json_obj['Name'], json_obj['Message']))




if __name__ == "__main__":
    ThreadedServer('localhost', 8881).listen()
