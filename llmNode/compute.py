import socket
import threading
from ollama import Client

# 約定port
port = 8001

local_ip = '172.17.0.3'
peers = [('172.17.0.2', port)] 

class P2PNode:
    def __init__(self):
        self.client = Client(host='http://localhost:11434')
        self.port = port 
        self.peers = peers
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((local_ip, self.port)) 

    def start(self):
        threading.Thread(target=self._listen).start()

    def _listen(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            message_info = data.decode('utf-8')
            response = self.inference(message_info)

        self.send_messages(response)    
    
    def send_messages(self, message):
        for peer in self.peers:
            self.sock.sendto(message.encode('utf-8'), peer)

    def inference(self, content):
        # call model
        response = self.client.generate(model='gemma:2b', prompt=content)

        return f"{response['message']['content']}"



if __name__ == "__main__":
    node = P2PNode()
    node.start()
