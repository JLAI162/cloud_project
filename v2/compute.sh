#!/usr/bin/python

# -*- coding: UTF-8 -*-

import sys
from ollama import Client
'''
    model part
'''
class Model:
    def __init__(self):
        self.client = Client(host='http://localhost:11434')

    def inference(self, content):

        response = self.client.chat(model='llama3', messages=[
            {
                'role': 'user',
                'content': content 
            }
        ])

        return f"{response['message']['content']}"

if __name__ == '__main__':
    model = Model()
    id = sys.argv[1]
    prompt = sys.argv[2]
    print(model.inference(prompt))