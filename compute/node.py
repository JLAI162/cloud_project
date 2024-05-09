# pip install ollama flask
# app.py

import time
import threading
import subprocess
from ollama import Client
from flask import Flask, request, jsonify, render_template



def _update_status():

    time.sleep(3)
    # 執行 top 命令並捕獲輸出
    process = subprocess.Popen(['top', '-bn', '1', '-i', '-c'], stdout=subprocess.PIPE)
    # 讀取輸出
    output = process.communicate()[0]
    # 解碼輸出
    output = output.decode('utf-8')

    # 寫入輸出檔
    with open("/share/node/" + node_no + ".txt", "w", encoding="utf-8") as f:
        f.write(output)

'''
    model part
'''
class Model:
    def __init__(self):
        self.client = Client(host='http://localhost:11434')

    def inference(self, content):
        # call model
        response = self.client.generate(model='gemma:2b', prompt=content)
        
        return f"{response['response']}"


'''
    server part
'''
app = Flask(__name__)

@app.route('/llm', methods=['POST'])
def inference():

    work_address = "/share/work/"

    if request.is_json:
        data = request.get_json()
        work_id = data.get('id', '')

        with open(work_address + work_id + "/input.txt", "r", encoding="utf-8") as f:
            user_message = f.read()

        # Debug print
        print(f"prompt: {user_message}")
        
        if user_message:
            
            results = model.inference(user_message)

            # 寫入輸出檔
            with open(work_address + work_id + "/output.txt", "w", encoding="utf-8") as f:
                f.write(results)

            return jsonify("success")
        else:
            return jsonify({"response": "沒有接收到消息！"}), 400
    return jsonify({"response": "請求不包含 JSON 數據"}), 400


if __name__ == '__main__':
    node_no = "node1"
    model = Model()
    threading.Thread(target=_update_status).start()
    app.run(host='172.17.0.3', port=8081, debug=True)
