import random
import string

def rendom_dir_name(length):
    # 設定可用字元
    available_chars = string.ascii_letters + string.digits

    # 隨機生成資料夾名稱
    folder_name = ''.join(random.choice(available_chars) for _ in range(length))

    return folder_name