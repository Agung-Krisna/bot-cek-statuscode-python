#!/usr/bin/env python3
from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
import os
import datetime
app = FastAPI()

filename = ""
@app.get('/screenshot/{domain}')
async def screenshot(domain : str, response_class=FileResponse):
    global filename
    
    current_time = datetime.datetime.now()
    used_time = f"-{current_time.hour}-{current_time.minute}-{current_time.second}"
    filename = f"{domain}{used_time}.jpg"
    os.system(f'wkhtmltoimage {domain} {filename}')
    
    response = RedirectResponse(url=f"/getfile/{filename}")
    return response

@app.get('/getfile/{filename}')
async def getfile(filename: str, response_class=FileResponse):
    return FileResponse(f'{filename}')