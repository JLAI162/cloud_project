# pip install ollama 
import sys
from ollama import Client
'''
    model part
'''
class Model:
    def __init__(self):
        self.client = Client(host='http://localhost:11434')

    def inference(self, content):

        response = self.client.chat(model='gemma:2b', messages=[
            {
                'role': 'user',
                'content': content 
            }
        ])

        return f"{response['message']['content']}"

if __name__ == '__main__':
    model = Model()
    prompt = sys.argv[1]
    print(model.inference(prompt))