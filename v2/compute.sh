#!/usr/bin/python3

# -*- coding: UTF-8 -*-

import sys
import httpx
import asyncio
from ollama import Client
from scrapegraphai.graphs import SearchGraph
'''
    model part
'''
class Model:
    def __init__(self):
        self.client = Client(host='http://localhost:11434')
        self.graph_config = {
            "llm": {
                "model": "ollama/llama3",  # Specifies the large language model to use
                "temperature": 0,  # Temperature controls randomness; 0 makes it deterministic
                "format": "json",  # Output format is set to JSON
                "base_url": "http://localhost:11434",  # Base URL where the Ollama server is running
            },
            "embeddings": {
                "model": "ollama/nomic-embed-text",  # Specifies the embedding model to use
                "temperature": 0,  # Keeps the generation deterministic
                "base_url": "http://localhost:11434",  # Base URL for the embeddings model server
            },
            "verbose": False,  # Enables verbose output for more detailed log information
        }

    def inference(self, content):

        # Create an instance of SmartScraperGraph with specific instructions
        search_graph = SearchGraph(
            prompt=content,
            config=self.graph_config
        )

        # Execute the scraping process
        result = search_graph.run()

        response = self.client.chat(model='gemma:2b', messages=[
            {
                'role': 'user',
                'content': f"This result:{result} is response for prompt :{content} . Output beatiful format for prompt, so remove json format. Only output the result content" 
            },

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
    asyncio.run(send_message(id))
