import sys 
import hashlib as ha

file = '/dbdata/0.txt'

def create_block(new_information):
    # read super block
    with open(file, mode='r') as super_block:
        # last block path
        last_block = super_block.readline().split(':')[1]

    # new block path
    new_block = str(int(last_block.split('.')[0]) + 1) + ".txt"   

    # update super block
    with open(file, mode='w') as super_block:
        super_block.write("block:" + new_block)

    # read last block content
    with open('/dbdata/'+last_block, mode='r') as f:
        text = f.readlines()

    # write last block's next block
    with open('/dbdata/'+last_block, mode='w') as f:
        text[1] = text[1][:12] + f"{new_block}\n"
        f.writelines(text)

    # create and write new block
    with open('/dbdata/'+new_block, mode='w') as f:
        encode = ha.sha3_256()
        encode.update( ''.join(text[:]).encode(encoding='utf-8'))
        new_content = ["Sha256 of previous block:" + f" {encode.hexdigest()}\n", "Next block: x\n"]
        f.write(''.join(new_content[:]))
        f.write(new_information)

        
def main():
    # trnsaction information
    sender = sys.argv[1]
    reciver = sys.argv[2]
    money = sys.argv[3]
    new_information = f"{sender},{reciver},{money}\n"

    try:
        # read super block for finding last block
        last_block = '/dbdata/' +open(file, mode='r').readline().split(':')[1]

        # read last block
        f = open(last_block, 'r')
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
        print('Danger, 0.txt error')




if __name__ == "__main__":
    main()