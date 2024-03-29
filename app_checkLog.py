import sys

user = sys.argv[1]

current_dir= '1.txt'
while(1):
        
    with open(current_dir, 'r') as file:
        lines = file.readlines()

    # 跳過頭兩行（前一區塊的哈希值和下一個區塊的指向）
        for line in lines[2:]:
            transaction = line.strip().split(',')
            sender, reciver, money = transaction
 
            if reciver == user:
                information = f"{sender},{reciver},{money}\n"
                print(information,end='')
            if sender == user:
                information = f"{sender},{reciver},{money}\n"
                print(information,end='')
                
        
        # 移動到下一個區塊，如果沒有下一個區塊，結束循環
        current_dir = lines[1].split(':')[1].strip()
        
    if(current_dir == "x"):
        break

        