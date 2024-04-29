import socket
import threading

port = 8001 

class P2PNode:
    def __init__(self):
        self.port = 8001 
        self.peers = [('172.17.0.2', port)]  
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('172.17.0.3', self.port)) 

    def start(self):
        threading.Thread(target=self._listen).start()

    def _listen(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            message_info = data.decode('utf-8')
            print(message_info)
    

if __name__ == "__main__":
    node = P2PNode()
    node.start()
