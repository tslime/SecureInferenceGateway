import os
import sys
import uvicorn
import requests
import json

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi import Header,HTTPException
from pydantic import BaseModel
from RStructure import RStructure


connection_point = FastAPI()
models = set()

def launch_http_server(connection_point,ip,p):
    global models
    models = get_models()
    print(models)
    print()    
    uvicorn.run(connection_point,host=ip,port=p)
    


def get_models():

    try:
        mod = requests.get("http://127.0.0.1:11434/api/tags")

        temp = []
        for m in mod.json()["models"]:
            temp.append(m["name"].split(":")[0])
    
        return set(temp)
    except requests.exceptions.RequestException as e:
        print("There are no models \n",e)
        return PlainTextResponse("There are no models \n",status_code=403)


@connection_point.post("/request")
async def parse_request(r: RStructure,api_key:str = Header(...,alias="X-API-KEY")):
    try:
        if api_key != "admin":
            return PlainTextResponse("Unauthorized access \n",status_code=403)
    
        m = r.model
        p = r.request
    
        return PlainTextResponse(model_reply(m,p))
    except requests.exceptions.RequestException as e:
        print("Ollama server unreachable",e)
        return PlainTextResponse("Ollama server is unreachable \n",status_code=503)


def model_reply(m,prompt):
    if m not in models:
        return "\n Unsupported model \n\n "
    else:
        return model_selector(m,prompt)

def model_selector(m,p):
    
    try:
        reply = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": m,
                "prompt": p
            }
        ) 

        result = ""
        for line in reply.iter_lines():
            result += json.loads(line.decode("utf-8")).get("response","")
    
        return "\n" + result + "\n\n"
    except requests.exceptions.RequestException as e:
        print("Model unavailable \n",e)
        return PlainTextResponse("Model unavailable",status_code=403)



launch_http_server(connection_point,"127.0.0.1",11434)