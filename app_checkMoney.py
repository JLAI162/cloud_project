import sys

balance = 0  # 初始化餘額

def calculate_balance(user):
    balance = 0  # 初始化餘額
    current_dir = '/dbdata/0.txt'  # 起始點為超級區塊文件
    
    with open('/dbdata/0.txt', mode='r') as head_block:
        current_block = head_block.readline().split(':')[1]

    # 循環遍歷所有區塊
    current_dir= '/dbdata/1.txt'
    i = 1
    while(1):
        
        with open(current_dir, 'r') as file:
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
        
        current_dir = '/dbdata/' + current_dir
        i -= 1
        
    return balance     
      
        
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 check_money.py 1")
    else:
        user = sys.argv[1]
        print(f"{user}的帳戶餘額是: {calculate_balance(user)}")
