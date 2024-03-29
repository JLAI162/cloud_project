import hashlib 
import os
import pandas as pd
import sys 
from app_transaction import create_block

#setting
file = os.path.join("0.txt")

sender = "angel"
reciver = sys.argv[1]
money = "10"
new_information = f"{sender},{reciver},{money}\n"

check = 1

# read super block
with open(file) as f:
    for line in f.readlines():
        lin = line.split(':')
        s = lin[1]
block_number = int(s.split('.')[0])

#checkChain
while block_number != 1:
    
    recent_block = f"{block_number}"
    last_block = f"{block_number-1}"
    
    recent_block_file = os.path.join(recent_block+".txt")
    test_block_file = os.path.join(last_block+".txt")
    
    with open(recent_block_file,"r") as f:
        with open(test_block_file,"r") as f2:
            
            text2 = f2.read()
            test_hsh_code = hashlib.sha3_256(text2.encode()).hexdigest()

            text = f.read().split('\n')
            hsh = text[0].split(': ')[1]
            
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
    
    try:
        # read super block for finding last block
        last_block = open(file, mode='r').readline().split(':')[1]
        
        # read last block
        f = open(os.path.join(last_block), 'r')
        last_block_content = f.readlines()
        f.close()

        # For check 0.txt
        if last_block_content[1][12] != 'x':
            raise

        # write information
        if len(last_block_content) >= 7 :
            # if have five transaction , create new block
            create_block(new_information)
        else:    
            # append information
            open(last_block, 'a').write(new_information)

    except:
        print("Danger, 0.txt error")
    
    
    