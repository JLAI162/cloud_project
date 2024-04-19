import os
import hashlib 
import socket
import threading

volume_locate = "./BChain/" # 區塊鏈儲存點

local_addr = '172.17.0.4'
port = 8001 #本節點的port 
peers = [('172.17.0.2', 8001), ('172.17.0.3', 8001)]  #跟另外二個IP:8001 節點通信

class P2PNode:
    def __init__(self, port, peers):
        self.port = port
        self.peers = peers
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((local_addr, self.port)) #這是本節點的 IP
        self.response_list = []

    def start(self):
        threading.Thread(target=self._listen).start()

    def _listen(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            message_info = data.decode('utf-8')

            tag = message_info.strip().split(',')[0]
            
            if tag == "transaction":
                transaction_info = message_info.strip().spilt(',',1)[1]
                print("===============")
                print(f"Received {transaction_info=} from {addr}")
                local_transaction(transaction_info)
                print("===============")

            elif tag == "request_checkAllChains":
                request_node = message_info.strip().spilt(',')[1]

                with open(volume_locate+'0.txt', mode = 'r') as super_block:
                    last_block = super_block.readline().split(':')[1].strip()

                with open(volume_locate+last_block,'r') as f:

                    text = f.read()
                    hsh_code = hashlib.sha3_256(text.encode()).hexdigest()
                
                message = f"response_checkAllChains,{local_addr},{hsh_code}"
                send_messages(request_node, message)

            elif tag == "response_checkAllChains":
                response_node = message_info.strip().spilt(',')[1]
                check_hsh = message_info.strip().spilt(',')[2]

                with open(volume_locate+'0.txt', mode = 'r') as super_block:
                    last_block = super_block.readline().split(':')[1].strip()

                with open(volume_locate+last_block,'r') as f:

                    text = f.read()
                    hsh_code = hashlib.sha3_256(text.encode()).hexdigest()

                if hsh_code != check_hsh:
                    print(f"{response_node} and {local_addr} lask block error")

                response_list.append(response_node)
            

            elif tag == "check_request":
                request_node = message_info.strip().spilt(',')[1]
                check_block = message_info.strip().spilt(',')[2]
                user = message_info.strip().spilt(',')[3] 

                with open(volume_locate+check_block,'r') as f:

                    text = f.read()
                    hsh_code = hashlib.sha3_256(text.encode()).hexdigest()

                message = f"check_response,{local_addr},{check_block},{hsh_code},{user}"
                send_messages(request_node, message)

            elif tag == "check_response":
                request_node = message_info.strip().spilt(',')[1]
                check_block = message_info.strip().spilt(',')[2]
                check_hsh = message_info.strip().spilt(',')[3]
                user = message_info.strip().spilt(',')[2]

                with open(volume_locate+check_block,'r') as f:

                    text = f.read()
                    hsh_code = hashlib.sha3_256(text.encode()).hexdigest()

                if hsh_code == check_hsh:
                    print(f"{check_block}: {request_node} and {local_addr} -> Yes")
                else:
                    print(f"{check_block}: {request_node} and {local_addr} -> NO")

                with open(volume_locate + file, mode='r') as super_block:
                    # last block file
                    last_block = super_block.readline().split(':')[1].strip()

                if check_block != last_block:
                    next_check = = str(int(last_block.split('.')[0]) + 1) + ".txt"
                    message = f"check_request,{local_addr},{next_check},{user}"
                    send_messages(request_node,message)
                else:
                    print("checkAllChain Done")
                    transaction_info = f"angel,{user},100\n"
                    transaction(self,)

            else:
                print("===============")
                print("can't recognize message's tag")
                print("===============")

    def send_messages_to_all(message):
            for peer in self.peers:
                self.sock.sendto(message.encode('utf-8'), peer)
    
    def send_messages(node, message):
        self.sock.sendto(message.encode('utf-8'), node)


    def checkAllChains(self, user):
        message = f"request_checkAllChains,{local_addr}" 
        send_messages_to_all(message)

        sleep(5)

        if len(response_list) < len(peers) + 1:
            print("reponse node < 50%")

        response_list.clear()

        message = f"check_request,{local_addr},{"1.txt"},{user}"
        send_messages_to_all(message)

    


def transaction(communicator, transaction_info):
    local_transaction(transaction_info)
    transaction_info = "transaction," + transaction_info
    communicator.send_messages_to_all(new_information)

def create_block(new_information):

    file = '0.txt' # super block

    # read super block
    with open(volume_locate + file, mode='r') as super_block:
        # last block file
        last_block = super_block.readline().split(':')[1].strip()
        # new block file
        new_block = str(int(last_block.split('.')[0]) + 1) + ".txt" 
    
    # update super block
    with open(volume_locate + file, mode='w') as super_block:
        super_block.write("block:" + new_block)

    # read last block content
    with open(volume_locate + last_block, mode='r') as f:
        text = f.readlines()

    # write last block's next block
    with open(volume_locate + last_block, mode='w') as f:
        text[1] = text[1][:12] + f"{new_block}\n"
        f.writelines(text)

    # create and write new block
    with open(volume_locate + new_block, mode='w') as f:
        encode = hashlib.sha3_256()
        encode.update( ''.join(text[:]).encode(encoding='utf-8'))
        new_content = ["Shashlib256 of previous block:" + f" {encode.hexdigest()}\n", "Next block: x\n"]
        f.write(''.join(new_content[:]))
        f.write(new_information)

def local_transaction(new_information):

    file = '0.txt'

    try:
        # read super block for finding last block
        last_block = open(volume_locate + file, mode='r').readline().split(':')[1].strip()

        # read last block
        with open(volume_locate + last_block, 'r') as f:
            last_block_content = f.readlines()
        
        class E(Exception):
            def __str__(self):
                return "0.txt record block that not last block"

        # For check 0.txt record is last block
        if last_block_content[1][12] != 'x':
            raise E

        # write information
        if len(last_block_content) >= 7 :
            # if hashlibve five transaction , create new block
            create_block(new_information)
        else:    
            # append information
            open(volume_locate + last_block, 'a').write(new_information)

        sender, reciver, money = new_information.strip().split(',')
        print(f"{sender}轉帳至{reciver}: ${money}")
    except Exception as ex:
        print(ex)

def calculate_balance(user):
    balance = 0  # 初始化餘額 

    # 循環遍歷所有區塊
    current_dir= '1.txt' # 起始點
    i = 1
    while(1):
        
        with open(volume_locate + current_dir, 'r') as file:
            lines = file.readlines()

        # 跳過頭兩行（前一區塊的哈希值和下一個區塊的指向）
        for line in lines[2:]:
            transaction = line.strip().split(',')
            sender, reciver, money = transaction
            
            # 根據交易更新餘額
            if reciver == user:
                balance += int(money)
            if sender == user:
                balance -= int(money)

        # 移動到下一個區塊，如果沒有下一個區塊，結束循環
        current_dir = lines[1].split(':')[1].strip()
        
        if(current_dir == "x"):
            break
        
        i -= 1
        
    return balance    

def checkMoney(user):
    print(f"{user}的帳戶餘額是: ${calculate_balance(user)}")

def checkChain(user):
    #setting
    file = "0.txt"
    check = 1

    # read super block for finding last block

    last_block = open(volume_locate + file, mode='r').readline().split(':')[1].strip()
    block_number = int(last_block.split('.')[0])

    #checkChashlibin
    while block_number != 1:
        
        recent_block = f"{block_number}"
        last_block = f"{block_number-1}"
        
        recent_block_file = os.path.join(recent_block+".txt")
        test_block_file = os.path.join(last_block+".txt")
        
        with open(volume_locate + recent_block_file,"r") as f:
            with open(volume_locate + test_block_file,"r") as f2:
                
                text2 = f2.read()
                test_hsh_code = hashlib.sha3_256(text2.encode()).hexdigest()

                text = f.read().split('\n')
                hsh = text[0].split(': ')[1].strip()
                
                if(test_hsh_code != hsh):
                    
                    print("block"+last_block+" -> error")             
                    print("block"+recent_block+"'s hashlibsh code : "+str(hsh))
                    print("block"+last_block+": "+str(test_hsh_code))
                    check = 0
                    
                else:
                    print("block"+last_block+" -> ok")
            
        block_number-=1
                    
    if(check == 1):
        print("OK")

        sender = "angel"
        reciver = user
        money = "10"
        transaction(node,f"{sender},{reciver},{money}\n")

def checkLog(user):
    current_dir= "1.txt" # 起始點

    while(1):
            
        with open(volume_locate + current_dir, 'r') as file:
            lines = file.readlines()

        # 跳過頭兩行（前一區塊的哈希值和下一個區塊的指向）
        for line in lines[2:]:
            transaction = line.strip().split(',')
            sender, reciver, money = transaction
            
            if reciver == user or sender == user:
                information = f"{sender},{reciver},{money}\n"
                print(information,end='')
                    
            
        # 移動到下一個區塊，如果沒有下一個區塊，結束循環
        current_dir = lines[1].split(':')[1].strip()
            
        if(current_dir == "x"):
            break



def checkAllChainsdd():
    # Create a dictionary to store the last block hash of each node
    last_block_hashes = {}
    
    # Send checkAllChains command to all peers and collect their responses
    for peer in node.peers:
        message = f"checkAllChains,{local_addr}"
        node.sock.sendto("checkAllChains".encode('utf-8'), peer)
        
        # Receive the response from the peer
        data, addr = node.sock.recvfrom(1024)
        peer_last_block_hash = data.decode('utf-8')
        
        # Store the last block hash of the peer
        last_block_hashes[addr] = peer_last_block_hash
    
    # Calculate the hash of the last block in the local chain
    local_last_block_hash = calculate_last_block_hash()
    
    # Compare the last block hash from each peer with the local last block hash
    all_hashes_equal = True
    for peer, peer_last_block_hash in last_block_hashes.items():
        if peer_last_block_hash != local_last_block_hash:
            print(f"No - Last block hash does not match with peer {peer}")
            all_hashes_equal = False
        else:
            print(f"Yes - Last block hash matches with peer {peer}")
    
    # If all hashes match, reward the user
    if all_hashes_equal:
        print("All hashes match. User receives 100 reward.")
        reward_user()  # Implement this function to give reward to the user

if __name__ == "__main__":
    
    node = P2PNode(port, peers)
    node.start()

    while True:
        print("===============")
        command = input("Enter a command {transaction,  checkChain, checkLog, checkMoney, checkAllChains, exit} : \n")
        commands = command.strip('\n').split()

        print("===============")
        if commands[0] == "transaction":
            new_information = f"{commands[1]},{commands[2]},{commands[3]}\n"
            transaction(node, new_information)

        elif commands[0] == "checkChain":
            checkChain(commands[1])

        elif commands[0] == "checkLog":
            checkLog(commands[1])

        elif commands[0] == "checkMoney":
            checkMoney(commands[1])
        
        elif commands[0] == "checkAllChains":
            print(f"Command Error : {command} 未完成")

        elif commands[0] == "exit":
            break

        else: 
            print(f"Command Error : {command}")
            print(f"                {'^' * len(command)}")
