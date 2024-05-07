import socket
import threading
from ollama import Client

port = 8001 

class P2PNode:
    def __init__(self):
        self.client = Client(host='http://localhost:11434')
        self.port = 8001 
        self.peers = [('172.17.0.2', port)]  
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('172.17.0.3', self.port)) 

    def start(self):
        threading.Thread(target=self._say).start()

    def _say(self):
        while True:
            content = input("Say something: ")
            self.inference(content)
    
    def send_messages(self, message):
        for peer in self.peers:
            self.sock.sendto(message.encode('utf-8'), peer)

    def inference(self, content):
        response = self.client.chat(model='gemma:2b', messages=[
            {
            'role': 'user',
            'content': content,
            },
        ])

        message = f"{response['message']['content']}"
        self.send_messages(message)



if __name__ == "__main__":
    node = P2PNode()
    node.start()
