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
        mod = requests.get("http://IP_WHERE_OLLAMA_SERVES:11434/api/tags")

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

        reply = model_reply(m,p)

        if reply == "\n Unsupported model \n\n":
            print("test \n")
            return PlainTextResponse("Unsupported model \n",status_code=404)
        else:
            return PlainTextResponse(reply)
    except requests.exceptions.RequestException as e:
        print("Ollama server unreachable \n",e)
        return PlainTextResponse("Ollama server is unreachable \n",status_code=503)


def model_reply(m,prompt):
    if m not in models:
        return "\n Unsupported model \n\n"
    else:
        return model_selector(m,prompt)

def model_selector(m,p):
    
    reply = requests.post(
        "http://IP_WHERE_OLLAMA_SERVES:11434/api/generate",
        json={
                "model": m,
                "prompt": p
            }
        ) 

    result = ""
    for line in reply.iter_lines():
        result += json.loads(line.decode("utf-8")).get("response","")
    
    return "\n" + result + "\n\n"



launch_http_server(connection_point,"LOCALHOST_IP",NON_RESERVED_PORT_NUMBER)