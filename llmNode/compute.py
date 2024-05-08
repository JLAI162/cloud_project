# app.py
from ollama import Client
from flask import Flask, request, jsonify, render_template

'''
    model part
'''
class Model:
    def __init__(self):
        self.client = Client(host='http://localhost:11434')

    def inference(self, content):
        # call model
        response = self.client.generate(model='gemma:2b', prompt=content)

        return f"{response['message']['content']}"


'''
    server part
'''
app = Flask(__name__)

@app.route('/', methods=['POST'])
def inference():
    if request.is_json:
        data = request.get_json()
        user_message = data.get('message', '')
        if user_message:
            
            results = model.inference(user_message)

            return jsonify({"response": results})
        else:
            return jsonify({"response": "沒有接收到消息！"}), 400
    return jsonify({"response": "請求不包含 JSON 數據"}), 400



if __name__ == '__main__':
    model = Model()
    app.run(host='0.0.0.0', port=8081, debug=True)
