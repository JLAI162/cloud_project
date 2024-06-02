#!/usr/bin/python3

# -*- coding: UTF-8 -*-

import sys
import httpx
import asyncio
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


    

async def send_message(id):

    url = 'http://192.168.10.2:80/response'

    async with httpx.AsyncClient() as client:
        try:
            await asyncio.wait_for(client.post(url, json={'id': id}), timeout=1)  # Adjust the timeout value as needed
        except asyncio.TimeoutError:
            # Ignore timeout errors
            pass


if __name__ == '__main__':
    model = Model()

    id = sys.argv[1]
    prompt = sys.argv[2]

    print(model.inference(prompt))
    print(id)
    asyncio.run(send_message(id))
