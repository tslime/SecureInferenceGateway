import os
import sys

from pydantic import BaseModel

class RStructure(BaseModel):
    model: str
    request: str