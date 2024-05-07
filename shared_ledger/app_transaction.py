import sys 
import hashlib as ha

volume_locate = "/dbdata/" # 區塊鏈儲存點

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
        encode = ha.sha3_256()
        encode.update( ''.join(text[:]).encode(encoding='utf-8'))
        new_content = ["Sha256 of previous block:" + f" {encode.hexdigest()}\n", "Next block: x\n"]
        f.write(''.join(new_content[:]))
        f.write(new_information)

def transaction(new_information):

    file = '0.txt'

    try:
        # read super block for finding last block
        last_block = open(volume_locate + file, mode='r').readline().split(':')[1].strip()

        # read last block
        with open(volume_locate + last_block, 'r') as f:
            last_block_content = f.readlines()
        

        # For check 0.txt record is last block
        if last_block_content[1][12] != 'x':
            raise

        # write information
        if len(last_block_content) >= 7 :
            # if have five transaction , create new block
            create_block(new_information)
        else:    
            # append information
            open(volume_locate + last_block, 'a').write(new_information)
    except:
        print('Danger, 0.txt error')


if __name__ == "__main__":
    # transaction information
    sender = sys.argv[1]
    reciver = sys.argv[2]
    money = sys.argv[3]
    new_information = f"{sender},{reciver},{money}\n"

    transaction(new_information)
