#!/usr/bin/env python3
from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
import os
import datetime
import os.path
from pathlib import Path

app = FastAPI()

file_not_found ="null"

filename = ""
@app.get('/screenshot/{domain}')
async def screenshot(domain : str, response_class=FileResponse):
    global filename
    
    current_time = datetime.datetime.now()
    used_time = f"-{current_time.hour}-{current_time.minute}-{current_time.second}"
    filename = f"{domain}{used_time}.jpg"
    os.system(f'wkhtmltoimage {domain} {filename}')
    
   # response = RedirectResponse(url=f"/getfile/{filename}")
    #return response
    return {"filename": filename}

@app.get('/getfile/{filename}')
async def getfile(filename: str, response_class=FileResponse):
    path_to_file = filename
    path = Path(path_to_file)
    
    if path.is_file():
        print(f'The file {path_to_file} exists')
        return FileResponse(f'{filename}')
        
    else:
        print(f'The file {path_to_file} does not exist')
        return {"filename": file_not_found}
        

