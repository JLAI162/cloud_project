import sys 
import os
import hashlib 
from app_transaction import transaction

volume_locate = "/dbdata/" # 區塊鏈儲存點

def app_checkChain():
    #setting
    file = "0.txt"
    check = 1

    # read super block for finding last block

    last_block = open(volume_locate + file, mode='r').readline().split(':')[1].strip()
    block_number = int(last_block.split('.')[0])

    #checkChain
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
                    print("block"+recent_block+"'s hash code : "+str(hsh))
                    print("block"+last_block+": "+str(test_hsh_code))
                    check = 0
                    
                else:
                    print("block"+last_block+" -> ok")
            
        block_number-=1
                    
    if(check == 1):
        print("OK")

        sender = "angel"
        reciver = sys.argv[1]
        money = "10"
        transaction(f"{sender},{reciver},{money}\n")
    
    
if __name__ == "__main__":
    user = sys.argv[1]
    app_checkChain(user)   
    
    
