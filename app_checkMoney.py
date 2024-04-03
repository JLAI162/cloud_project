import sys

volume_locate = "/dbdata/" # 區塊鏈儲存點

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



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 check_money.py 1")
    else:
        user = sys.argv[1]
        print(f"{user}的帳戶餘額是: {calculate_balance(user)}")
