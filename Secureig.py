import os
import sys
import uvicorn

from fastapi import FastAPI, Request
from pydantic import BaseModel


connection_point = FastAPI()

def launch_http_server(connection_point,ip,p):    
    uvicorn.run(connection_point,host=ip,port=p)

@connection_point.post("/request")
def send_response():
    return {"message": "Connection, OK!"}


launch_http_server(connection_point,"192.168.2.57",8085)