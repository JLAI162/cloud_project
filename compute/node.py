# pip install ollama flask
# app.py

import time
import threading
import subprocess
from ollama import Client
from flask import Flask, request, jsonify, render_template

from wiki import search_information_from_wiki



def _update_status():
    while True:
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
        keyword = self.client.chat(model='gemma:2b', messages=[
            {
                'role': 'user',
                'content': content + ". Please return only the key words or main topics of this content for me, for use in a web scraper on Wikipedia。"
            },
        ])
        
        # 爬蟲
        data_string = search_information_from_wiki(keyword['message']['content'])

        response = self.client.chat(model='gemma:2b', messages=[
            {
                'role': 'user',
                'content': content 
            },
            keyword['message'],
            {
                'role': 'user',
                'content': f"Please use following infomation tell me about this {content}:\n {data_string}"
            },

        ])

        return f"{response['message']['content']}"


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

        with open(work_address + work_id + "/status.txt", "w", encoding="utf-8") as f:
            f.write(node_no+",computing")

        with open(work_address + work_id + "/input.txt", "r", encoding="utf-8") as f:
            user_message = f.read()

        # Debug print
        print(f"prompt: {user_message}")
        
        if user_message:
            
            results = model.inference(user_message)

            # 寫入輸出檔
            with open(work_address + work_id + "/output.txt", "w", encoding="utf-8") as f:
                f.write(results)
            
            
            with open(work_address + work_id + "/status.txt", "w", encoding="utf-8") as f:
                f.write(node_no+",complete")

            return jsonify("success")
        else:
            return jsonify({"response": "沒有接收到消息！"}), 400
    return jsonify({"response": "請求不包含 JSON 數據"}), 400


if __name__ == '__main__':
    node_no = "node1"
    model = Model()
    threading.Thread(target=_update_status).start()
    app.run(host='0.0.0.0', port=8081, debug=True)
